use std::fs;
use std::io::{Read, Write};
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

use anyhow::{Context, Result, ensure};
use chrono::Utc;
use serde::Serialize;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};

use crate::config::LoadedConfig;
use crate::icon;
use crate::paths::{AppPaths, sanitize_component, write_atomic};
use crate::planner::{self, PayloadPlan};
use crate::signing;
use crate::toolchain;

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct BuildReport {
    schema_version: u32,
    created_at: String,
    application_id: String,
    version_code: u32,
    version_name: String,
    config_file: PathBuf,
    source_folder: PathBuf,
    entrypoint: PathBuf,
    file_count: u64,
    total_bytes: u64,
    pack_count: usize,
    play_compatible: bool,
    play_incompatibilities: Vec<String>,
    aab: Option<Artifact>,
    apks: Option<Artifact>,
}

#[derive(Debug, Serialize)]
struct Artifact {
    file: String,
    bytes: u64,
    sha256: String,
}

pub fn build(
    config_path: &Path,
    output_override: Option<&Path>,
    engine_override: Option<&Path>,
    keep_staging: bool,
) -> Result<()> {
    let loaded = LoadedConfig::load(config_path)?;
    let plan = planner::plan(&loaded)?;
    let tools = toolchain::resolve()?;
    let engine = toolchain::resolve_engine(engine_override)?;
    let signing = signing::resolve(&loaded, &tools.keytool)?;
    let paths = AppPaths::discover()?;
    paths.ensure()?;

    let slug = sanitize_component(&loaded.config.project.name);
    ensure!(
        !slug.is_empty(),
        "project.name no produce un nombre de archivo válido"
    );
    let plan_json = serde_json::to_vec(&plan)?;
    let identity = hex::encode(Sha256::digest(&plan_json));
    let staging = paths.cache.join("builds").join(format!(
        "{}-{}-{}",
        slug,
        loaded.config.android.version_code,
        &identity[..12]
    ));
    if staging.exists() {
        fs::remove_dir_all(&staging)?;
    }
    fs::create_dir_all(&staging)?;
    let packs = planner::stage(&loaded, &plan, &staging)?;
    let icons = staging.join("icon-res");
    icon::generate(
        &loaded.icon,
        &loaded.config.android.icon_background_color,
        &icons,
    )?;
    let runtime_config = runtime_config(&loaded, &plan);
    let resolved_config = staging.join("win2apk.json");
    write_atomic(
        &resolved_config,
        serde_json::to_string_pretty(&runtime_config)?.as_bytes(),
    )?;

    println!(
        "Empaquetando {} archivos ({} bytes) en {} asset packs...",
        plan.file_count,
        plan.total_bytes,
        plan.packs.len()
    );
    if !plan.play_compatible {
        for reason in &plan.play_incompatibilities {
            eprintln!("advertencia Google Play: {reason}");
        }
    }

    let gradle_status = Command::new("bash")
        .arg(engine.join("gradlew"))
        .args([":app:clean", ":app:bundleRelease"])
        .args(["--no-daemon", "--console=plain"])
        .current_dir(&engine)
        .env(
            "JAVA_HOME",
            tools.java.parent().and_then(Path::parent).unwrap(),
        )
        .env("ANDROID_HOME", &tools.android_sdk)
        .env("ANDROID_SDK_ROOT", &tools.android_sdk)
        .env("WIN2APK_CONFIG", &resolved_config)
        .env("WIN2APK_ASSET_PACKS_DIR", &packs)
        .env("WIN2APK_ICON_RES_DIR", &icons)
        .env(
            "WIN2APK_PAYLOAD_MANIFEST",
            staging.join("payload-manifest.json"),
        )
        .env("WIN2APK_SIGN_WITH_GRADLE", "false")
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()
        .context("no se pudo ejecutar Gradle")?;
    ensure!(
        gradle_status.success(),
        "Gradle no pudo generar el Android App Bundle"
    );

    let built_aab = engine.join(
        "app/build/intermediates/intermediary_bundle/release/packageReleaseBundle/intermediary-bundle.aab",
    );
    ensure!(
        built_aab.is_file(),
        "Gradle terminó sin producir {}",
        built_aab.display()
    );
    sign_aab(&built_aab, &signing, &tools.java, &staging)?;
    let output = output_override
        .map(Path::to_path_buf)
        .unwrap_or_else(|| loaded.base.join("dist"));
    fs::create_dir_all(&output)?;
    let artifact_base = format!("{}-{}", slug, loaded.config.android.version_name);
    let aab_path = output.join(format!("{artifact_base}.aab"));
    fs::copy(&built_aab, &aab_path)?;

    let apks_path = output.join(format!("{artifact_base}.apks"));
    if loaded.config.distribution.apks {
        if apks_path.exists() {
            fs::remove_file(&apks_path)?;
        }
        let mut store_password_file = tempfile::NamedTempFile::new_in(&staging)?;
        store_password_file.write_all(signing.store_password.as_bytes())?;
        fs::set_permissions(
            store_password_file.path(),
            fs::Permissions::from_mode(0o600),
        )?;
        let mut key_password_file = tempfile::NamedTempFile::new_in(&staging)?;
        key_password_file.write_all(signing.key_password.as_bytes())?;
        fs::set_permissions(key_password_file.path(), fs::Permissions::from_mode(0o600))?;
        let mut command = Command::new(&tools.java);
        command
            .args(["-jar"])
            .arg(&tools.bundletool)
            .arg("build-apks")
            .arg(format!("--bundle={}", aab_path.display()))
            .arg(format!("--output={}", apks_path.display()))
            .arg(format!("--ks={}", signing.keystore.display()))
            .arg(format!("--ks-key-alias={}", signing.alias))
            .arg(format!(
                "--ks-pass=file:{}",
                store_password_file.path().display()
            ))
            .arg(format!(
                "--key-pass=file:{}",
                key_password_file.path().display()
            ))
            .stdout(Stdio::inherit())
            .stderr(Stdio::inherit());
        if loaded.config.distribution.local_testing {
            command.arg("--local-testing");
        }
        let status = command.status().context("no se pudo ejecutar bundletool")?;
        ensure!(status.success(), "bundletool no pudo generar el APK set");
    }

    write_atomic(
        &output.join("payload-manifest.json"),
        serde_json::to_string_pretty(&plan)?.as_bytes(),
    )?;
    write_atomic(
        &output.join("resolved-config.json"),
        serde_json::to_string_pretty(&runtime_config)?.as_bytes(),
    )?;

    let aab_artifact = loaded
        .config
        .distribution
        .aab
        .then(|| describe(&aab_path))
        .transpose()?;
    let apks_artifact = loaded
        .config
        .distribution
        .apks
        .then(|| describe(&apks_path))
        .transpose()?;
    let report = BuildReport {
        schema_version: 1,
        created_at: Utc::now().to_rfc3339(),
        application_id: loaded.config.android.application_id.clone(),
        version_code: loaded.config.android.version_code,
        version_name: loaded.config.android.version_name.clone(),
        config_file: loaded.path.clone(),
        source_folder: loaded.source.clone(),
        entrypoint: loaded.config.project.entrypoint.clone(),
        file_count: plan.file_count,
        total_bytes: plan.total_bytes,
        pack_count: plan.packs.len(),
        play_compatible: plan.play_compatible,
        play_incompatibilities: plan.play_incompatibilities.clone(),
        aab: aab_artifact,
        apks: apks_artifact,
    };
    write_atomic(
        &output.join("build-report.json"),
        serde_json::to_string_pretty(&report)?.as_bytes(),
    )?;
    write_checksums(&output, &report)?;

    if !loaded.config.distribution.aab {
        fs::remove_file(&aab_path)?;
    }
    if !keep_staging {
        fs::remove_dir_all(&staging)?;
    } else {
        println!("Staging conservado en {}", staging.display());
    }
    println!("Empaquetado terminado: {}", output.display());
    Ok(())
}

fn runtime_config(loaded: &LoadedConfig, plan: &PayloadPlan) -> Value {
    let shortcut_name = loaded
        .config
        .shortcut
        .name
        .as_deref()
        .unwrap_or(&loaded.config.project.name);
    json!({
        "schemaVersion": 2,
        "project": {
            "name": loaded.config.project.name,
            "entrypoint": loaded.config.project.entrypoint,
            "installDirectory": loaded.config.project.install_directory
        },
        "android": {
            "applicationId": loaded.config.android.application_id,
            "versionCode": loaded.config.android.version_code,
            "versionName": loaded.config.android.version_name,
            "rootfsPackageId": loaded.config.android.rootfs_package_id,
            "rootfsPathAlias": loaded.config.android.rootfs_path_alias,
            "pathRewriteAssets": loaded.config.android.path_rewrite_assets
        },
        "payload": {
            "mode": "move",
            "manifestAsset": "payload-manifest.json",
            "assetPackNames": plan.packs.iter().map(|pack| &pack.name).collect::<Vec<_>>(),
            "expectedFileCount": plan.file_count,
            "expectedBytes": plan.total_bytes
        },
        "startup": loaded.config.startup,
        "runtime": loaded.config.runtime,
        "shortcut": {
            "name": shortcut_name,
            "desktopFile": "Win2APK.desktop",
            "execArguments": loaded.config.shortcut.exec_arguments,
            "forceFullscreen": loaded.config.shortcut.force_fullscreen
        },
        "container": loaded.config.container
    })
}

fn describe(path: &Path) -> Result<Artifact> {
    let mut input = fs::File::open(path)
        .with_context(|| format!("no se pudo abrir el artefacto {}", path.display()))?;
    let bytes = input.metadata()?.len();
    let mut hasher = Sha256::new();
    let mut buffer = [0_u8; 1024 * 1024];
    loop {
        let read = input.read(&mut buffer)?;
        if read == 0 {
            break;
        }
        hasher.update(&buffer[..read]);
    }
    Ok(Artifact {
        file: path.file_name().unwrap().to_string_lossy().into_owned(),
        bytes,
        sha256: hex::encode(hasher.finalize()),
    })
}

fn write_checksums(output: &Path, report: &BuildReport) -> Result<()> {
    let mut lines = Vec::new();
    for artifact in [report.aab.as_ref(), report.apks.as_ref()]
        .into_iter()
        .flatten()
    {
        lines.push(format!("{}  {}", artifact.sha256, artifact.file));
    }
    write_atomic(
        &output.join("checksums.sha256"),
        format!("{}\n", lines.join("\n")).as_bytes(),
    )
}

fn sign_aab(
    input: &Path,
    signing: &signing::SigningMaterial,
    java: &Path,
    staging: &Path,
) -> Result<()> {
    let signed = staging.join("signed-output.aab");
    let mut arguments = tempfile::NamedTempFile::new_in(staging)?;
    fs::set_permissions(arguments.path(), fs::Permissions::from_mode(0o600))?;
    for argument in [
        "-m".to_owned(),
        "jdk.jartool/sun.security.tools.jarsigner.Main".to_owned(),
        "-keystore".to_owned(),
        signing.keystore.display().to_string(),
        "-storetype".to_owned(),
        "PKCS12".to_owned(),
        "-storepass".to_owned(),
        signing.store_password.clone(),
        "-keypass".to_owned(),
        signing.key_password.clone(),
        "-digestalg".to_owned(),
        "SHA-256".to_owned(),
        "-sigalg".to_owned(),
        "SHA256withRSA".to_owned(),
        "-signedjar".to_owned(),
        signed.display().to_string(),
        input.display().to_string(),
        signing.alias.clone(),
    ] {
        writeln!(arguments, "{}", jarsigner_argument(&argument))?;
    }
    arguments.flush()?;
    let status = Command::new(java)
        .arg(format!("@{}", arguments.path().display()))
        .status()
        .context("no se pudo ejecutar jarsigner")?;
    ensure!(status.success(), "jarsigner no pudo firmar el AAB");
    fs::rename(&signed, input).context("no se pudo publicar el AAB firmado")?;
    Ok(())
}

fn jarsigner_argument(argument: &str) -> String {
    if argument
        .chars()
        .all(|character| !character.is_whitespace() && character != '"' && character != '\\')
    {
        return argument.to_owned();
    }
    format!(
        "\"{}\"",
        argument.replace('\\', "\\\\").replace('"', "\\\"")
    )
}
