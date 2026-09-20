use std::fs::{self, File};
use std::path::Path;
use std::process::{Command, Stdio};

use anyhow::{Context, Result, bail, ensure};
use serde_json::Value;

use crate::toolchain;

pub fn install(apks: &Path, device: Option<&str>, fresh: bool, code_update: bool) -> Result<()> {
    ensure!(apks.is_file(), "APK set no encontrado: {}", apks.display());
    let tools = toolchain::resolve()?;
    let report_path = apks
        .parent()
        .unwrap_or(Path::new("."))
        .join("build-report.json");
    ensure!(
        report_path.is_file(),
        "falta build-report.json junto al APKS"
    );
    let report: Value = serde_json::from_slice(&fs::read(&report_path)?)?;
    let package = report["applicationId"]
        .as_str()
        .context("build-report.json no contiene applicationId")?;

    let installed = package_installed(&tools.adb, device, package)?;
    if installed && !fresh && !code_update {
        bail!(
            "{package} ya está instalado; use --fresh para una reinstalación destructiva o --code-update para conservar los datos"
        );
    }
    if code_update {
        ensure!(
            installed,
            "--code-update requiere que {package} ya esté instalado"
        );
        return install_code_only(apks, &tools.adb, device);
    }
    if fresh && installed {
        println!("Desinstalando {package} por solicitud explícita --fresh...");
        ensure!(
            adb_success(&tools.adb, device, ["uninstall", package])?,
            "ADB no pudo desinstalar {package}"
        );
    }

    let mut command = Command::new(&tools.java);
    command
        .args(["-jar"])
        .arg(&tools.bundletool)
        .arg("install-apks")
        .arg(format!("--apks={}", apks.display()))
        .arg(format!("--adb={}", tools.adb.display()));
    if let Some(device) = device {
        command.arg(format!("--device-id={device}"));
    }
    let status = command
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()?;
    ensure!(status.success(), "bundletool no pudo instalar el APK set");
    println!("Instalación enviada correctamente a Android.");
    Ok(())
}

fn install_code_only(apks: &Path, adb: &Path, device: Option<&str>) -> Result<()> {
    let temporary = tempfile::tempdir()?;
    let mut archive = zip::ZipArchive::new(File::open(apks)?)?;
    let mut base_apks = Vec::new();
    for index in 0..archive.len() {
        let mut entry = archive.by_index(index)?;
        let Some(relative) = entry.enclosed_name() else {
            continue;
        };
        let Some(name) = relative.file_name().and_then(|value| value.to_str()) else {
            continue;
        };
        if !name.starts_with("base-") || !name.ends_with(".apk") {
            continue;
        }
        let target = temporary.path().join(name);
        let mut output = File::create(&target)?;
        std::io::copy(&mut entry, &mut output)?;
        base_apks.push(target);
    }
    ensure!(
        !base_apks.is_empty(),
        "el APKS no contiene splits del módulo base"
    );
    let mut command = adb_command(adb, device);
    command.args(["install-multiple", "-r"]);
    command.args(&base_apks);
    let status = command
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()?;
    ensure!(
        status.success(),
        "ADB no pudo actualizar el módulo base; los datos instalados no se eliminaron"
    );
    println!("Código base actualizado sin reinstalar los asset packs.");
    Ok(())
}

fn adb_success<const N: usize>(adb: &Path, device: Option<&str>, args: [&str; N]) -> Result<bool> {
    Ok(adb_command(adb, device)
        .args(args)
        .output()?
        .status
        .success())
}

fn package_installed(adb: &Path, device: Option<&str>, package: &str) -> Result<bool> {
    let output = adb_command(adb, device)
        .args(["shell", "pm", "path", package])
        .output()?;
    Ok(output.status.success() && !String::from_utf8_lossy(&output.stdout).trim().is_empty())
}

fn adb_command(adb: &Path, device: Option<&str>) -> Command {
    let mut command = Command::new(adb);
    if let Some(device) = device {
        command.args(["-s", device]);
    }
    command
}
