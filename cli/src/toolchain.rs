use std::fs::{self, File};
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

use anyhow::{Context, Result, bail, ensure};
use flate2::read::GzDecoder;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sha2::{Digest, Sha256};

use crate::paths::{AppPaths, write_atomic};

const LOCK_DATA: &str = include_str!("../../toolchain.lock.json");
const TOOLCHAIN_ID: &str = "android36-ndk30-jdk17-v1";
const ADOPTIUM_API: &str = "https://api.adoptium.net/v3/assets/latest/17/hotspot?architecture=x64&heap_size=normal&image_type=jdk&jvm_impl=hotspot&os=linux&project=jdk&vendor=eclipse";

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct LockFile {
    android_command_line_tools: Artifact,
    android_packages: Vec<String>,
    bundletool: BundletoolArtifact,
}

#[derive(Debug, Deserialize)]
struct Artifact {
    revision: String,
    url: String,
    sha256: String,
}

#[derive(Debug, Deserialize)]
struct BundletoolArtifact {
    version: String,
    url: String,
    sha256: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct InstalledToolchain {
    pub id: String,
    pub java_home: PathBuf,
    pub android_sdk: PathBuf,
    pub bundletool: PathBuf,
    pub jdk_version: String,
    pub jdk_sha256: String,
    pub command_line_tools_revision: String,
    pub command_line_tools_sha256: String,
    pub bundletool_version: String,
    pub bundletool_sha256: String,
}

#[derive(Debug, Clone)]
pub struct ResolvedToolchain {
    pub java: PathBuf,
    pub keytool: PathBuf,
    pub android_sdk: PathBuf,
    pub adb: PathBuf,
    pub bundletool: PathBuf,
}

pub fn setup(force: bool) -> Result<()> {
    supported_host()?;
    let lock: LockFile = serde_json::from_str(LOCK_DATA)?;
    ensure!(
        lock.android_command_line_tools.sha256 != "PENDING_LOCAL_VERIFICATION",
        "toolchain.lock.json aún no contiene el SHA-256 verificado de Android command-line tools"
    );
    let paths = AppPaths::discover()?;
    paths.ensure()?;
    let root = paths.data.join("toolchains").join(TOOLCHAIN_ID);
    let manifest_path = root.join("installed.json");
    if manifest_path.is_file() && !force {
        let installed: InstalledToolchain = serde_json::from_slice(&fs::read(&manifest_path)?)?;
        verify_installed(&installed)?;
        println!("Toolchain ya instalado: {}", root.display());
        return Ok(());
    }
    if force && root.exists() {
        fs::remove_dir_all(&root)?;
    }
    fs::create_dir_all(&root)?;

    println!("Descargando JDK 17 desde Eclipse Temurin...");
    let (jdk_url, jdk_checksum, jdk_version) = resolve_temurin()?;
    let jdk_archive = root.join("jdk.tar.gz");
    download(&jdk_url, &jdk_archive, &jdk_checksum)?;
    let jdk_parent = root.join("jdk");
    fs::create_dir_all(&jdk_parent)?;
    let archive = File::open(&jdk_archive)?;
    tar::Archive::new(GzDecoder::new(archive)).unpack(&jdk_parent)?;
    let java_home = find_parent_containing(&jdk_parent, "bin/java")?;
    fs::remove_file(&jdk_archive)?;

    println!(
        "Descargando Android command-line tools {}...",
        lock.android_command_line_tools.revision
    );
    let tools_archive = root.join("command-line-tools.zip");
    download(
        &lock.android_command_line_tools.url,
        &tools_archive,
        &lock.android_command_line_tools.sha256,
    )?;
    let android_sdk = root.join("android-sdk");
    let unpacked = root.join("command-line-tools-unpacked");
    extract_zip(&tools_archive, &unpacked)?;
    let latest = android_sdk.join("cmdline-tools/latest");
    fs::create_dir_all(latest.parent().unwrap())?;
    let extracted = unpacked.join("cmdline-tools");
    ensure!(
        extracted.join("bin/sdkmanager").is_file(),
        "archivo command-line tools inesperado"
    );
    fs::rename(&extracted, &latest)?;
    fs::remove_dir_all(&unpacked)?;
    fs::remove_file(&tools_archive)?;

    let sdkmanager = latest.join("bin/sdkmanager");
    println!("Android requiere aceptar sus licencias antes de instalar el SDK, NDK y CMake.");
    let license_status = Command::new(&sdkmanager)
        .arg("--licenses")
        .env("JAVA_HOME", &java_home)
        .env("ANDROID_SDK_ROOT", &android_sdk)
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()?;
    ensure!(
        license_status.success(),
        "no se aceptaron todas las licencias de Android"
    );
    let package_status = Command::new(&sdkmanager)
        .args(lock.android_packages.iter())
        .env("JAVA_HOME", &java_home)
        .env("ANDROID_SDK_ROOT", &android_sdk)
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()?;
    ensure!(
        package_status.success(),
        "sdkmanager no pudo instalar el toolchain fijado"
    );

    println!("Descargando bundletool {}...", lock.bundletool.version);
    let bundletool = root.join(format!("bundletool-{}.jar", lock.bundletool.version));
    download(&lock.bundletool.url, &bundletool, &lock.bundletool.sha256)?;

    let installed = InstalledToolchain {
        id: TOOLCHAIN_ID.to_owned(),
        java_home,
        android_sdk,
        bundletool,
        jdk_version,
        jdk_sha256: jdk_checksum,
        command_line_tools_revision: lock.android_command_line_tools.revision,
        command_line_tools_sha256: lock.android_command_line_tools.sha256,
        bundletool_version: lock.bundletool.version,
        bundletool_sha256: lock.bundletool.sha256,
    };
    write_atomic(
        &manifest_path,
        serde_json::to_string_pretty(&installed)?.as_bytes(),
    )?;
    verify_installed(&installed)?;
    println!("Toolchain instalado en {}", root.display());
    Ok(())
}

pub fn doctor(engine: Option<&Path>) -> Result<()> {
    supported_host()?;
    let resolved = resolve()?;
    let engine = resolve_engine(engine)?;
    println!("Host: Linux x86_64");
    println!("Java: {}", resolved.java.display());
    println!("Android SDK: {}", resolved.android_sdk.display());
    println!("ADB: {}", resolved.adb.display());
    println!("bundletool: {}", resolved.bundletool.display());
    println!("Motor Android: {}", engine.display());
    ensure!(
        engine.join("gradlew").is_file(),
        "el motor no contiene gradlew"
    );
    ensure!(
        engine.join("app/build.gradle").is_file(),
        "el motor no contiene app/build.gradle"
    );
    let status = Command::new(&resolved.java).arg("-version").status()?;
    ensure!(status.success(), "Java no se puede ejecutar");
    println!("Diagnóstico aprobado.");
    Ok(())
}

pub fn resolve() -> Result<ResolvedToolchain> {
    if let Some(managed) = load_managed()? {
        return resolved_from_installed(managed);
    }
    resolve_development()
}

pub fn resolve_engine(override_path: Option<&Path>) -> Result<PathBuf> {
    if let Some(path) = override_path {
        return canonical_directory(path, "motor Android");
    }
    if let Ok(path) = std::env::var("WIN2APK_ENGINE_DIR") {
        return canonical_directory(Path::new(&path), "WIN2APK_ENGINE_DIR");
    }
    let development = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../winlator/app");
    if development.is_dir() {
        return development
            .canonicalize()
            .context("no se pudo resolver el motor de desarrollo");
    }
    let paths = AppPaths::discover()?;
    canonical_directory(&paths.data.join("engine/current"), "motor instalado")
}

fn resolve_development() -> Result<ResolvedToolchain> {
    let java = which::which("java").context("Java no encontrado; ejecute `win2apk setup`")?;
    let keytool =
        which::which("keytool").context("keytool no encontrado; ejecute `win2apk setup`")?;
    let android_sdk = ["ANDROID_SDK_ROOT", "ANDROID_HOME"]
        .iter()
        .find_map(|name| std::env::var_os(name).map(PathBuf::from))
        .or_else(|| {
            directories::BaseDirs::new()
                .map(|dirs| dirs.home_dir().join("Android/Sdk"))
                .filter(|candidate| candidate.is_dir())
        })
        .context("Android SDK no encontrado; ejecute `win2apk setup`")?;
    let adb = android_sdk.join("platform-tools/adb");
    ensure!(adb.is_file(), "ADB ausente en {}", android_sdk.display());
    let bundletool = std::env::var_os("WIN2APK_BUNDLETOOL")
        .map(PathBuf::from)
        .context("bundletool no encontrado; ejecute `win2apk setup` o defina WIN2APK_BUNDLETOOL")?;
    Ok(ResolvedToolchain {
        java,
        keytool,
        android_sdk,
        adb,
        bundletool,
    })
}

fn load_managed() -> Result<Option<InstalledToolchain>> {
    let paths = AppPaths::discover()?;
    let manifest = paths
        .data
        .join("toolchains")
        .join(TOOLCHAIN_ID)
        .join("installed.json");
    if !manifest.is_file() {
        return Ok(None);
    }
    Ok(Some(serde_json::from_slice(&fs::read(manifest)?)?))
}

fn resolved_from_installed(installed: InstalledToolchain) -> Result<ResolvedToolchain> {
    verify_installed(&installed)?;
    Ok(ResolvedToolchain {
        java: installed.java_home.join("bin/java"),
        keytool: installed.java_home.join("bin/keytool"),
        adb: installed.android_sdk.join("platform-tools/adb"),
        android_sdk: installed.android_sdk,
        bundletool: installed.bundletool,
    })
}

fn verify_installed(installed: &InstalledToolchain) -> Result<()> {
    for path in [
        installed.java_home.join("bin/java"),
        installed.java_home.join("bin/keytool"),
        installed.java_home.join("bin/jarsigner"),
        installed.android_sdk.join("platform-tools/adb"),
        installed
            .android_sdk
            .join("platforms/android-36/android.jar"),
        installed.android_sdk.join("ndk/30.0.15729638"),
        installed.android_sdk.join("cmake/3.22.1"),
        installed.bundletool.clone(),
    ] {
        ensure!(path.exists(), "toolchain incompleto: {}", path.display());
    }
    Ok(())
}

fn resolve_temurin() -> Result<(String, String, String)> {
    let response: Value = reqwest::blocking::Client::builder()
        .user_agent("win2apk/0.1")
        .build()?
        .get(ADOPTIUM_API)
        .send()?
        .error_for_status()?
        .json()?;
    let asset = response
        .as_array()
        .and_then(|items| items.first())
        .context("Adoptium no devolvió un JDK 17")?;
    let package = &asset["binary"]["package"];
    let link = package["link"]
        .as_str()
        .context("Adoptium no devolvió el enlace del JDK")?;
    let checksum = package["checksum"]
        .as_str()
        .context("Adoptium no devolvió el checksum del JDK")?;
    let version = asset["version"]["semver"].as_str().unwrap_or("17");
    Ok((link.to_owned(), checksum.to_owned(), version.to_owned()))
}

fn download(url: &str, destination: &Path, expected_sha256: &str) -> Result<()> {
    let client = reqwest::blocking::Client::builder()
        .user_agent("win2apk/0.1")
        .redirect(reqwest::redirect::Policy::limited(10))
        .build()?;
    let mut response = client.get(url).send()?.error_for_status()?;
    let temporary = destination.with_extension("download");
    let mut output = File::create(&temporary)?;
    let mut digest = Sha256::new();
    let mut buffer = vec![0u8; 1024 * 1024];
    loop {
        let read = response.read(&mut buffer)?;
        if read == 0 {
            break;
        }
        output.write_all(&buffer[..read])?;
        digest.update(&buffer[..read]);
    }
    output.sync_all()?;
    let actual = hex::encode(digest.finalize());
    if actual != expected_sha256.to_ascii_lowercase() {
        fs::remove_file(&temporary).ok();
        bail!("checksum inválido para {url}: esperado {expected_sha256}, obtenido {actual}");
    }
    fs::rename(temporary, destination)?;
    Ok(())
}

fn extract_zip(archive: &Path, destination: &Path) -> Result<()> {
    if destination.exists() {
        fs::remove_dir_all(destination)?;
    }
    fs::create_dir_all(destination)?;
    let mut zip = zip::ZipArchive::new(File::open(archive)?)?;
    for index in 0..zip.len() {
        let mut entry = zip.by_index(index)?;
        let relative = entry
            .enclosed_name()
            .context("ZIP contiene una ruta no segura")?;
        let target = destination.join(relative);
        if entry.is_dir() {
            fs::create_dir_all(&target)?;
        } else {
            if let Some(parent) = target.parent() {
                fs::create_dir_all(parent)?;
            }
            let mut output = File::create(&target)?;
            io::copy(&mut entry, &mut output)?;
            #[cfg(unix)]
            if let Some(mode) = entry.unix_mode() {
                use std::os::unix::fs::PermissionsExt;
                fs::set_permissions(&target, fs::Permissions::from_mode(mode))?;
            }
        }
    }
    Ok(())
}

fn find_parent_containing(root: &Path, relative: &str) -> Result<PathBuf> {
    for entry in fs::read_dir(root)? {
        let path = entry?.path();
        if path.join(relative).is_file() {
            return Ok(path);
        }
    }
    bail!("no se encontró {relative} dentro de {}", root.display())
}

fn canonical_directory(path: &Path, label: &str) -> Result<PathBuf> {
    ensure!(
        path.is_dir(),
        "{label} no es una carpeta: {}",
        path.display()
    );
    path.canonicalize()
        .with_context(|| format!("no se pudo resolver {}", path.display()))
}

fn supported_host() -> Result<()> {
    ensure!(cfg!(target_os = "linux"), "Win2APK CLI sólo admite Linux");
    ensure!(
        std::env::consts::ARCH == "x86_64",
        "Win2APK CLI v0.1 sólo admite Linux x86_64"
    );
    Ok(())
}
