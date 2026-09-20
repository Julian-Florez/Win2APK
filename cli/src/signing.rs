use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{Context, Result, bail, ensure};
use rand::distr::{Alphanumeric, SampleString};
use serde::{Deserialize, Serialize};

use crate::config::LoadedConfig;
use crate::paths::{AppPaths, write_atomic};

#[derive(Debug, Clone)]
pub struct SigningMaterial {
    pub keystore: PathBuf,
    pub alias: String,
    pub store_password: String,
    pub key_password: String,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct StoredKey {
    application_id: String,
    alias: String,
    store_password: String,
    key_password: String,
    keystore_file: String,
}

pub fn resolve(loaded: &LoadedConfig, keytool: &Path) -> Result<SigningMaterial> {
    if loaded.config.signing.profile == "custom" {
        return custom(loaded);
    }
    automatic(&loaded.config.android.application_id, keytool)
}

pub fn backup(application_id: &str, destination: &Path) -> Result<()> {
    let paths = AppPaths::discover()?;
    let key_dir = paths.config.join("keys").join(application_id);
    ensure!(
        key_dir.is_dir(),
        "no existe una clave automática para {application_id}"
    );
    ensure!(
        !destination.exists(),
        "el destino ya existe: {}",
        destination.display()
    );
    fs::create_dir_all(destination)?;
    for name in ["key.p12", "key.json"] {
        fs::copy(key_dir.join(name), destination.join(name))?;
    }
    fs::set_permissions(destination, fs::Permissions::from_mode(0o700))?;
    fs::set_permissions(
        destination.join("key.p12"),
        fs::Permissions::from_mode(0o600),
    )?;
    fs::set_permissions(
        destination.join("key.json"),
        fs::Permissions::from_mode(0o600),
    )?;
    println!("Respaldo creado en {}", destination.display());
    Ok(())
}

fn automatic(application_id: &str, keytool: &Path) -> Result<SigningMaterial> {
    let paths = AppPaths::discover()?;
    paths.ensure()?;
    let key_dir = paths.config.join("keys").join(application_id);
    fs::create_dir_all(&key_dir)?;
    fs::set_permissions(&key_dir, fs::Permissions::from_mode(0o700))?;
    let metadata_path = key_dir.join("key.json");
    let keystore = key_dir.join("key.p12");

    if metadata_path.is_file() && keystore.is_file() {
        let stored: StoredKey = serde_json::from_slice(&fs::read(&metadata_path)?)?;
        ensure!(
            stored.application_id == application_id,
            "la clave persistente no pertenece a {application_id}"
        );
        return Ok(SigningMaterial {
            keystore,
            alias: stored.alias,
            store_password: stored.store_password,
            key_password: stored.key_password,
        });
    }
    ensure!(
        !metadata_path.exists() && !keystore.exists(),
        "clave automática incompleta en {}",
        key_dir.display()
    );

    let password = Alphanumeric.sample_string(&mut rand::rng(), 32);
    let alias = "win2apk".to_owned();
    let status = Command::new(keytool)
        .args(["-genkeypair", "-storetype", "PKCS12", "-keystore"])
        .arg(&keystore)
        .args([
            "-storepass",
            &password,
            "-keypass",
            &password,
            "-alias",
            &alias,
            "-keyalg",
            "RSA",
            "-keysize",
            "3072",
            "-validity",
            "10000",
            "-dname",
            &format!("CN={application_id}, O=Win2APK, C=CO"),
            "-noprompt",
        ])
        .status()
        .context("no se pudo ejecutar keytool")?;
    ensure!(status.success(), "keytool no pudo crear la clave de firma");

    let stored = StoredKey {
        application_id: application_id.to_owned(),
        alias: alias.clone(),
        store_password: password.clone(),
        key_password: password.clone(),
        keystore_file: "key.p12".to_owned(),
    };
    write_atomic(
        &metadata_path,
        serde_json::to_string_pretty(&stored)?.as_bytes(),
    )?;
    fs::set_permissions(&metadata_path, fs::Permissions::from_mode(0o600))?;
    fs::set_permissions(&keystore, fs::Permissions::from_mode(0o600))?;
    eprintln!(
        "Clave persistente creada para {application_id}. Ejecute `win2apk keys backup {application_id} <carpeta>` antes de publicar actualizaciones."
    );
    Ok(SigningMaterial {
        keystore,
        alias,
        store_password: password.clone(),
        key_password: password,
    })
}

fn custom(loaded: &LoadedConfig) -> Result<SigningMaterial> {
    let signing = &loaded.config.signing;
    let configured = signing
        .keystore
        .as_ref()
        .context("signing.keystore ausente")?;
    let keystore = if configured.is_absolute() {
        configured.clone()
    } else {
        loaded.base.join(configured)
    };
    ensure!(
        keystore.is_file(),
        "keystore no encontrado: {}",
        keystore.display()
    );
    let store_variable = signing.store_password_env.as_deref().unwrap();
    let key_variable = signing.key_password_env.as_deref().unwrap();
    let store_password = std::env::var(store_variable)
        .with_context(|| format!("variable de entorno ausente: {store_variable}"))?;
    let key_password = std::env::var(key_variable)
        .with_context(|| format!("variable de entorno ausente: {key_variable}"))?;
    if store_password.is_empty() || key_password.is_empty() {
        bail!("las contraseñas de firma no pueden estar vacías");
    }
    Ok(SigningMaterial {
        keystore,
        alias: signing.alias.clone().unwrap(),
        store_password,
        key_password,
    })
}
