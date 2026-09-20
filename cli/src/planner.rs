use std::cmp::Reverse;
use std::fs::{self, File};
use std::io::{Read, Seek, SeekFrom, Write};
use std::os::unix::fs::symlink;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, bail, ensure};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use walkdir::WalkDir;

use crate::config::LoadedConfig;
use crate::paths::write_atomic;

const PLAY_ON_DEMAND_LIMIT: u64 = 30_000_000_000;
const PLAY_PACK_LIMIT: usize = 100;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct PayloadPlan {
    pub schema_version: u32,
    pub file_count: u64,
    pub directory_count: u64,
    pub total_bytes: u64,
    pub target_pack_bytes: u64,
    pub play_compatible: bool,
    pub play_incompatibilities: Vec<String>,
    pub directories: Vec<String>,
    pub files: Vec<PayloadFile>,
    pub packs: Vec<AssetPack>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct PayloadFile {
    pub path: String,
    pub size: u64,
    pub sha256: String,
    pub segments: Vec<PayloadSegment>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct PayloadSegment {
    pub pack: String,
    pub asset_path: String,
    pub offset: u64,
    pub size: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AssetPack {
    pub name: String,
    pub bytes: u64,
    pub segment_count: u64,
}

#[derive(Debug)]
struct Item {
    file_index: usize,
    segment_index: usize,
    size: u64,
}

pub fn plan(loaded: &LoadedConfig) -> Result<PayloadPlan> {
    let mut files = Vec::new();
    let mut directories = Vec::new();
    let root = loaded.source.canonicalize()?;

    for entry in WalkDir::new(&root).follow_links(false).sort_by_file_name() {
        let entry = entry.with_context(|| format!("no se pudo recorrer {}", root.display()))?;
        if entry.path() == root {
            continue;
        }
        if entry.file_type().is_symlink() {
            bail!(
                "la carpeta contiene un enlace simbólico no portable: {}",
                entry.path().display()
            );
        }
        let relative = entry.path().strip_prefix(&root)?;
        let path = portable_path(relative)?;
        if entry.file_type().is_dir() {
            directories.push(path);
            continue;
        }
        ensure!(
            entry.file_type().is_file(),
            "tipo de entrada no admitido: {}",
            entry.path().display()
        );
        let size = entry.metadata()?.len();
        let sha256 = hash_file(entry.path())?;
        files.push(PayloadFile {
            path,
            size,
            sha256,
            segments: Vec::new(),
        });
    }

    ensure!(!files.is_empty(), "sourceFolder no contiene archivos");
    files.sort_by(|left, right| left.path.cmp(&right.path));
    directories.sort();
    let target = loaded.config.packaging.target_pack_bytes;
    let mut items = Vec::new();

    for (file_index, file) in files.iter_mut().enumerate() {
        if file.size <= target {
            file.segments.push(PayloadSegment {
                pack: String::new(),
                asset_path: file.path.clone(),
                offset: 0,
                size: file.size,
            });
            items.push(Item {
                file_index,
                segment_index: 0,
                size: file.size,
            });
            continue;
        }

        let identity = &file.sha256[..16];
        let mut offset = 0;
        let mut index = 0usize;
        while offset < file.size {
            let size = target.min(file.size - offset);
            file.segments.push(PayloadSegment {
                pack: String::new(),
                asset_path: format!(".win2apk-chunks/{identity}/{index:06}.part"),
                offset,
                size,
            });
            items.push(Item {
                file_index,
                segment_index: index,
                size,
            });
            offset += size;
            index += 1;
        }
    }

    items.sort_by_key(|item| {
        (
            Reverse(item.size),
            files[item.file_index].path.clone(),
            item.segment_index,
        )
    });

    let mut pack_bytes: Vec<u64> = Vec::new();
    let mut pack_segments: Vec<u64> = Vec::new();
    for item in items {
        let candidate = pack_bytes
            .iter()
            .enumerate()
            .filter(|(_, bytes)| **bytes + item.size <= target)
            .min_by_key(|(index, bytes)| (**bytes, *index))
            .map(|(index, _)| index);
        let pack_index = candidate.unwrap_or_else(|| {
            pack_bytes.push(0);
            pack_segments.push(0);
            pack_bytes.len() - 1
        });
        pack_bytes[pack_index] += item.size;
        pack_segments[pack_index] += 1;
        files[item.file_index].segments[item.segment_index].pack = pack_name(pack_index);
    }

    let packs = pack_bytes
        .into_iter()
        .zip(pack_segments)
        .enumerate()
        .map(|(index, (bytes, segment_count))| AssetPack {
            name: pack_name(index),
            bytes,
            segment_count,
        })
        .collect::<Vec<_>>();
    let total_bytes = files.iter().map(|file| file.size).sum();
    let mut play_incompatibilities = Vec::new();
    if total_bytes > PLAY_ON_DEMAND_LIMIT {
        play_incompatibilities.push(format!(
            "payload de {total_bytes} bytes supera el límite acumulado on-demand de {PLAY_ON_DEMAND_LIMIT} bytes"
        ));
    }
    if packs.len() > PLAY_PACK_LIMIT {
        play_incompatibilities.push(format!(
            "{} asset packs superan el máximo de {PLAY_PACK_LIMIT}",
            packs.len()
        ));
    }

    Ok(PayloadPlan {
        schema_version: 1,
        file_count: files.len() as u64,
        directory_count: directories.len() as u64,
        total_bytes,
        target_pack_bytes: target,
        play_compatible: play_incompatibilities.is_empty(),
        play_incompatibilities,
        directories,
        files,
        packs,
    })
}

pub fn stage(loaded: &LoadedConfig, plan: &PayloadPlan, root: &Path) -> Result<PathBuf> {
    let packs_root = root.join("asset-packs");
    if packs_root.exists() {
        fs::remove_dir_all(&packs_root)?;
    }
    fs::create_dir_all(&packs_root)?;

    for pack in &plan.packs {
        let module = packs_root.join(&pack.name);
        fs::create_dir_all(module.join("src/main/assets"))?;
        let build_gradle = format!(
            "plugins {{\n    id 'com.android.asset-pack'\n}}\n\nassetPack {{\n    packName = '{}'\n    dynamicDelivery {{\n        deliveryType = 'on-demand'\n    }}\n}}\n",
            pack.name
        );
        write_atomic(&module.join("build.gradle"), build_gradle.as_bytes())?;
    }

    for file in &plan.files {
        let source = loaded.source.join(Path::new(&file.path));
        for segment in &file.segments {
            let destination = packs_root
                .join(&segment.pack)
                .join("src/main/assets")
                .join(Path::new(&segment.asset_path));
            if let Some(parent) = destination.parent() {
                fs::create_dir_all(parent)?;
            }
            if file.segments.len() == 1 && segment.offset == 0 && segment.size == file.size {
                symlink(&source, &destination).with_context(|| {
                    format!(
                        "no se pudo enlazar {} -> {}",
                        destination.display(),
                        source.display()
                    )
                })?;
            } else {
                write_segment(&source, &destination, segment.offset, segment.size)?;
            }
        }
    }

    let manifest_path = root.join("payload-manifest.json");
    write_atomic(
        &manifest_path,
        serde_json::to_string_pretty(plan)?.as_bytes(),
    )?;
    Ok(packs_root)
}

fn write_segment(source: &Path, destination: &Path, offset: u64, size: u64) -> Result<()> {
    let mut input = File::open(source)?;
    input.seek(SeekFrom::Start(offset))?;
    let mut limited = input.take(size);
    let mut output = File::create(destination)?;
    let copied = std::io::copy(&mut limited, &mut output)?;
    ensure!(
        copied == size,
        "lectura incompleta al dividir {}",
        source.display()
    );
    output.flush()?;
    Ok(())
}

fn pack_name(index: usize) -> String {
    format!("win2apk_payload_{:03}", index + 1)
}

fn portable_path(path: &Path) -> Result<String> {
    let value = path
        .to_str()
        .with_context(|| format!("ruta no UTF-8: {}", path.display()))?
        .replace('\\', "/");
    ensure!(
        !value.starts_with('/') && !value.contains("../"),
        "ruta no portable: {value}"
    );
    Ok(value)
}

fn hash_file(path: &Path) -> Result<String> {
    let mut input = File::open(path)?;
    let mut digest = Sha256::new();
    let mut buffer = vec![0u8; 1024 * 1024];
    loop {
        let read = input.read(&mut buffer)?;
        if read == 0 {
            break;
        }
        digest.update(&buffer[..read]);
    }
    Ok(hex::encode(digest.finalize()))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::LoadedConfig;

    #[test]
    fn name_is_stable() {
        assert_eq!(pack_name(0), "win2apk_payload_001");
        assert_eq!(pack_name(99), "win2apk_payload_100");
    }

    #[test]
    fn plan_splits_an_oversized_file() {
        let temp = tempfile::tempdir().unwrap();
        let source = temp.path().join("payload");
        fs::create_dir(&source).unwrap();
        File::create(source.join("app.exe"))
            .unwrap()
            .set_len(67_108_865)
            .unwrap();
        fs::write(temp.path().join("icon.png"), tiny_png()).unwrap();
        fs::write(
            temp.path().join("app.json"),
            r##"{
              "schemaVersion": 2,
              "project": {"name":"Test","sourceFolder":"payload","entrypoint":"app.exe","installDirectory":"Test"},
              "android": {"applicationId":"org.test.app","versionCode":1,"versionName":"1","icon":"icon.png"},
              "packaging": {"targetPackBytes":67108864}
            }"##,
        ).unwrap();
        let loaded = LoadedConfig::load(&temp.path().join("app.json")).unwrap();
        let result = plan(&loaded).unwrap();
        assert_eq!(result.files.len(), 1);
        assert_eq!(result.files[0].segments.len(), 2);
    }

    fn tiny_png() -> &'static [u8] {
        &[
            137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 0, 1, 0, 0, 0, 1,
            8, 6, 0, 0, 0, 31, 21, 196, 137, 0, 0, 0, 13, 73, 68, 65, 84, 8, 215, 99, 248, 207,
            192, 240, 31, 0, 5, 0, 1, 255, 137, 153, 61, 29, 0, 0, 0, 0, 73, 69, 78, 68, 174, 66,
            96, 130,
        ]
    }
}
