use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, bail};
use directories::ProjectDirs;

pub struct AppPaths {
    pub config: PathBuf,
    pub data: PathBuf,
    pub cache: PathBuf,
}

impl AppPaths {
    pub fn discover() -> Result<Self> {
        let dirs = ProjectDirs::from("org", "Win2APK", "win2apk")
            .context("no se pudieron determinar los directorios XDG del usuario")?;
        Ok(Self {
            config: dirs.config_dir().to_path_buf(),
            data: dirs.data_dir().to_path_buf(),
            cache: dirs.cache_dir().to_path_buf(),
        })
    }

    pub fn ensure(&self) -> Result<()> {
        for directory in [&self.config, &self.data, &self.cache] {
            fs::create_dir_all(directory)
                .with_context(|| format!("no se pudo crear {}", directory.display()))?;
        }
        Ok(())
    }
}

pub fn write_atomic(path: &Path, contents: &[u8]) -> Result<()> {
    let parent = path
        .parent()
        .with_context(|| format!("{} no tiene directorio padre", path.display()))?;
    fs::create_dir_all(parent).with_context(|| format!("no se pudo crear {}", parent.display()))?;
    let mut temporary = tempfile::NamedTempFile::new_in(parent)
        .with_context(|| format!("no se pudo crear un temporal en {}", parent.display()))?;
    temporary.write_all(contents)?;
    temporary.as_file().sync_all()?;
    temporary
        .persist(path)
        .map_err(|error| error.error)
        .with_context(|| format!("no se pudo publicar {}", path.display()))?;
    Ok(())
}

pub fn clean_cache() -> Result<()> {
    let paths = AppPaths::discover()?;
    let builds = paths.cache.join("builds");
    if !builds.exists() {
        println!("No hay staging regenerable para eliminar.");
        return Ok(());
    }
    if builds.parent() != Some(paths.cache.as_path()) {
        bail!(
            "se rechazó una ruta de limpieza no segura: {}",
            builds.display()
        );
    }
    fs::remove_dir_all(&builds)
        .with_context(|| format!("no se pudo eliminar {}", builds.display()))?;
    println!("Staging eliminado: {}", builds.display());
    Ok(())
}

pub fn sanitize_component(value: &str) -> String {
    let mut result = String::new();
    let mut previous_separator = false;
    for character in value.chars().flat_map(char::to_lowercase) {
        if character.is_ascii_alphanumeric() {
            result.push(character);
            previous_separator = false;
        } else if !previous_separator && !result.is_empty() {
            result.push('-');
            previous_separator = true;
        }
    }
    result.trim_matches('-').to_owned()
}
