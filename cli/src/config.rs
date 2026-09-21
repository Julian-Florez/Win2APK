use std::fs;
use std::path::{Component, Path, PathBuf};

use anyhow::{Context, Result, bail, ensure};
use serde::{Deserialize, Serialize};
use serde_json::Value;

const DEFAULT_PACK_BYTES: u64 = 1_350_000_000;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Config {
    #[serde(rename = "$schema")]
    pub schema: Option<String>,
    pub schema_version: u32,
    pub project: Project,
    pub android: Android,
    #[serde(default)]
    pub packaging: Packaging,
    #[serde(default)]
    pub distribution: Distribution,
    #[serde(default)]
    pub signing: Signing,
    #[serde(default)]
    pub startup: Startup,
    #[serde(default)]
    pub runtime: Value,
    #[serde(default)]
    pub shortcut: Shortcut,
    #[serde(default)]
    pub container: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Project {
    pub name: String,
    pub source_folder: PathBuf,
    pub entrypoint: PathBuf,
    pub install_directory: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Android {
    pub application_id: String,
    pub version_code: u32,
    pub version_name: String,
    pub icon: PathBuf,
    #[serde(default = "default_icon_background")]
    pub icon_background_color: String,
    #[serde(default = "default_rootfs_package")]
    pub rootfs_package_id: String,
    #[serde(default = "default_rootfs_alias")]
    pub rootfs_path_alias: String,
    #[serde(default = "default_path_rewrite_assets")]
    pub path_rewrite_assets: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Packaging {
    #[serde(default = "default_delivery")]
    pub delivery: String,
    #[serde(default = "default_storage_mode")]
    pub storage_mode: String,
    #[serde(default = "default_pack_bytes")]
    pub target_pack_bytes: u64,
    #[serde(default = "default_oversized")]
    pub oversized_files: String,
}

impl Default for Packaging {
    fn default() -> Self {
        Self {
            delivery: default_delivery(),
            storage_mode: default_storage_mode(),
            target_pack_bytes: default_pack_bytes(),
            oversized_files: default_oversized(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Distribution {
    #[serde(default = "default_true")]
    pub aab: bool,
    #[serde(default = "default_true")]
    pub apks: bool,
    #[serde(default = "default_true")]
    pub local_testing: bool,
}

impl Default for Distribution {
    fn default() -> Self {
        Self {
            aab: true,
            apks: true,
            local_testing: true,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Signing {
    #[serde(default = "default_signing_profile")]
    pub profile: String,
    pub keystore: Option<PathBuf>,
    pub alias: Option<String>,
    pub store_password_env: Option<String>,
    pub key_password_env: Option<String>,
}

impl Default for Signing {
    fn default() -> Self {
        Self {
            profile: default_signing_profile(),
            keystore: None,
            alias: None,
            store_password_env: None,
            key_password_env: None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Startup {
    #[serde(default = "default_true")]
    pub core_mode: bool,
    #[serde(default = "default_true")]
    pub auto_launch: bool,
    #[serde(default = "default_true")]
    pub close_core_when_application_exits: bool,
    #[serde(default)]
    pub request_storage_permission: bool,
    #[serde(default)]
    pub show_general_interface: bool,
    #[serde(default = "default_true")]
    pub minimal_loading: bool,
    #[serde(default = "default_error_mode")]
    pub error_mode: String,
    #[serde(default = "default_loading_text")]
    pub loading_text: String,
}

impl Default for Startup {
    fn default() -> Self {
        Self {
            core_mode: true,
            auto_launch: true,
            close_core_when_application_exits: true,
            request_storage_permission: false,
            show_general_interface: false,
            minimal_loading: true,
            error_mode: default_error_mode(),
            loading_text: default_loading_text(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Shortcut {
    pub name: Option<String>,
    #[serde(default)]
    pub exec_arguments: String,
    #[serde(default)]
    pub force_fullscreen: bool,
    #[serde(default)]
    pub input_controls: InputControls,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct InputControls {
    #[serde(default = "default_input_controls_mode")]
    pub mode: String,
    #[serde(default)]
    pub profile: String,
}

impl Default for InputControls {
    fn default() -> Self {
        Self {
            mode: default_input_controls_mode(),
            profile: String::new(),
        }
    }
}

#[derive(Debug, Clone)]
pub struct LoadedConfig {
    pub path: PathBuf,
    pub base: PathBuf,
    pub config: Config,
    pub source: PathBuf,
    pub icon: PathBuf,
}

impl LoadedConfig {
    pub fn load(path: &Path) -> Result<Self> {
        ensure!(cfg!(target_os = "linux"), "Win2APK CLI sólo admite Linux");
        ensure!(
            std::env::consts::ARCH == "x86_64",
            "Win2APK CLI v0.1 sólo admite Linux x86_64"
        );
        let path = path
            .canonicalize()
            .with_context(|| format!("no se pudo abrir {}", path.display()))?;
        let base = path
            .parent()
            .context("el JSON no tiene directorio padre")?
            .to_path_buf();
        let data = fs::read(&path)?;
        let config: Config = serde_json::from_slice(&data)
            .with_context(|| format!("JSON v2 inválido en {}", path.display()))?;
        config.validate()?;
        let source = resolve(&base, &config.project.source_folder);
        let icon = resolve(&base, &config.android.icon);
        ensure!(
            source.is_dir(),
            "sourceFolder no es una carpeta: {}",
            source.display()
        );
        ensure!(icon.is_file(), "icon no es un archivo: {}", icon.display());
        let entrypoint = source.join(&config.project.entrypoint);
        ensure!(
            entrypoint.is_file(),
            "entrypoint no existe dentro de sourceFolder: {}",
            entrypoint.display()
        );
        Ok(Self {
            path,
            base,
            config,
            source,
            icon,
        })
    }
}

impl Config {
    fn validate(&self) -> Result<()> {
        ensure!(self.schema_version == 2, "schemaVersion debe ser 2");
        ensure!(
            !self.project.name.trim().is_empty(),
            "project.name es obligatorio"
        );
        ensure!(
            !self.project.install_directory.trim().is_empty()
                && !self.project.install_directory.contains(['/', '\\']),
            "project.installDirectory debe ser un nombre de carpeta de Windows"
        );
        validate_relative(&self.project.entrypoint, "project.entrypoint")?;
        validate_application_id(&self.android.application_id)?;
        ensure!(
            self.android.version_code > 0,
            "android.versionCode debe ser mayor que cero"
        );
        ensure!(
            !self.android.version_name.trim().is_empty(),
            "android.versionName es obligatorio"
        );
        ensure!(
            is_color(&self.android.icon_background_color),
            "android.iconBackgroundColor debe tener formato #RRGGBB o #RRGGBBAA"
        );
        ensure!(
            self.packaging.delivery == "on-demand",
            "sólo se admite delivery=on-demand"
        );
        ensure!(
            self.packaging.storage_mode == "move",
            "sólo se admite storageMode=move"
        );
        ensure!(
            self.packaging.oversized_files == "chunk",
            "oversizedFiles debe ser chunk"
        );
        ensure!(
            (64 * 1024 * 1024..=1_400_000_000).contains(&self.packaging.target_pack_bytes),
            "targetPackBytes debe estar entre 64 MiB y 1.400.000.000 bytes"
        );
        ensure!(
            self.distribution.aab || self.distribution.apks,
            "se debe solicitar AAB, APKS o ambos"
        );
        ensure!(
            matches!(
                self.shortcut.input_controls.mode.as_str(),
                "always" | "when_no_physical_controller" | "never"
            ),
            "shortcut.inputControls.mode no admitido"
        );
        ensure!(
            !self.shortcut.input_controls.profile.contains(['\n', '\r']),
            "shortcut.inputControls.profile no puede contener saltos de línea"
        );
        match self.signing.profile.as_str() {
            "auto" => ensure!(
                self.signing.keystore.is_none()
                    && self.signing.alias.is_none()
                    && self.signing.store_password_env.is_none()
                    && self.signing.key_password_env.is_none(),
                "signing.profile=auto no acepta propiedades de un keystore externo"
            ),
            "custom" => {
                ensure!(
                    self.signing.keystore.is_some(),
                    "signing.keystore es obligatorio para custom"
                );
                ensure!(
                    self.signing.alias.as_deref().is_some_and(|v| !v.is_empty()),
                    "signing.alias es obligatorio para custom"
                );
                ensure!(
                    self.signing
                        .store_password_env
                        .as_deref()
                        .is_some_and(|v| !v.is_empty()),
                    "signing.storePasswordEnv es obligatorio para custom"
                );
                ensure!(
                    self.signing
                        .key_password_env
                        .as_deref()
                        .is_some_and(|v| !v.is_empty()),
                    "signing.keyPasswordEnv es obligatorio para custom"
                );
            }
            other => bail!("signing.profile no admitido: {other}"),
        }
        Ok(())
    }
}

fn resolve(base: &Path, value: &Path) -> PathBuf {
    if value.is_absolute() {
        value.to_path_buf()
    } else {
        base.join(value)
    }
}

fn validate_relative(path: &Path, name: &str) -> Result<()> {
    ensure!(!path.as_os_str().is_empty(), "{name} es obligatorio");
    ensure!(
        !path.is_absolute(),
        "{name} debe ser relativo a sourceFolder"
    );
    for component in path.components() {
        if matches!(
            component,
            Component::ParentDir | Component::RootDir | Component::Prefix(_)
        ) {
            bail!("{name} no puede salir de sourceFolder");
        }
    }
    Ok(())
}

fn validate_application_id(value: &str) -> Result<()> {
    let parts: Vec<_> = value.split('.').collect();
    ensure!(
        parts.len() >= 2,
        "android.applicationId debe contener al menos dos segmentos"
    );
    for part in parts {
        let mut chars = part.chars();
        ensure!(
            chars.next().is_some_and(|c| c.is_ascii_lowercase()),
            "segmento inválido en applicationId: {part}"
        );
        ensure!(
            chars.all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '_'),
            "segmento inválido en applicationId: {part}"
        );
    }
    Ok(())
}

fn is_color(value: &str) -> bool {
    matches!(value.len(), 7 | 9)
        && value.starts_with('#')
        && value[1..]
            .chars()
            .all(|character| character.is_ascii_hexdigit())
}

fn default_true() -> bool {
    true
}
fn default_delivery() -> String {
    "on-demand".to_owned()
}
fn default_storage_mode() -> String {
    "move".to_owned()
}
fn default_pack_bytes() -> u64 {
    DEFAULT_PACK_BYTES
}
fn default_oversized() -> String {
    "chunk".to_owned()
}
fn default_signing_profile() -> String {
    "auto".to_owned()
}
fn default_icon_background() -> String {
    "#000000".to_owned()
}
fn default_rootfs_package() -> String {
    "com.winlator".to_owned()
}
fn default_rootfs_alias() -> String {
    "/proc/self/fd/3".to_owned()
}
fn default_loading_text() -> String {
    "Preparing application...".to_owned()
}
fn default_input_controls_mode() -> String {
    "always".to_owned()
}
fn default_error_mode() -> String {
    "technical_dialog".to_owned()
}
fn default_path_rewrite_assets() -> Vec<String> {
    [
        "rootfs.tzst",
        "rootfs_patches.tzst",
        "container_pattern.tzst",
        "box64/box64-0.4.0.tzst",
        "graphics_driver/gladio-1.0.tzst",
        "graphics_driver/turnip-26.1.0.tzst",
        "graphics_driver/virgl-23.1.9.tzst",
        "graphics_driver/vortek-2.1.tzst",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect()
}
