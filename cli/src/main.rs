mod build;
mod config;
mod icon;
mod install;
mod paths;
mod planner;
mod signing;
mod toolchain;

use std::path::PathBuf;

use anyhow::Result;
use clap::{Parser, Subcommand};

#[derive(Debug, Parser)]
#[command(
    name = "win2apk",
    version,
    about = "Empaqueta carpetas Windows preparadas para Android"
)]
struct Cli {
    /// Ruta a la plantilla Android de Win2APK.
    #[arg(long, global = true, env = "WIN2APK_ENGINE_DIR")]
    engine: Option<PathBuf>,

    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Instala o comprueba el toolchain aislado de Win2APK.
    Setup {
        #[arg(long)]
        force: bool,
    },
    /// Comprueba el host, el toolchain y la plantilla Android.
    Doctor,
    /// Valida la configuración y la carpeta de entrada.
    Validate { config: PathBuf },
    /// Calcula los asset packs sin modificar la carpeta original.
    Plan {
        config: PathBuf,
        #[arg(long)]
        output: Option<PathBuf>,
    },
    /// Genera AAB, APKS y los reportes reproducibles.
    Build {
        config: PathBuf,
        #[arg(long)]
        output: Option<PathBuf>,
        #[arg(long)]
        keep_staging: bool,
    },
    /// Instala un APKS mediante bundletool.
    Install {
        apks: PathBuf,
        #[arg(long)]
        device: Option<String>,
        #[arg(long, conflicts_with = "code_update")]
        fresh: bool,
        #[arg(long, conflicts_with = "fresh")]
        code_update: bool,
    },
    /// Administra las claves persistentes creadas por Win2APK.
    Keys {
        #[command(subcommand)]
        command: KeyCommand,
    },
    /// Elimina únicamente staging y cachés regenerables.
    Clean,
}

#[derive(Debug, Subcommand)]
enum KeyCommand {
    /// Copia el keystore y sus metadatos a una carpeta de respaldo.
    Backup {
        application_id: String,
        destination: PathBuf,
    },
}

fn main() {
    if let Err(error) = run() {
        eprintln!("error: {error:#}");
        std::process::exit(1);
    }
}

fn run() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Command::Setup { force } => toolchain::setup(force),
        Command::Doctor => toolchain::doctor(cli.engine.as_deref()),
        Command::Validate { config } => {
            let loaded = config::LoadedConfig::load(&config)?;
            let plan = planner::plan(&loaded)?;
            println!(
                "Configuración válida: {} archivos, {} bytes, {} asset packs",
                plan.file_count,
                plan.total_bytes,
                plan.packs.len()
            );
            Ok(())
        }
        Command::Plan { config, output } => {
            let loaded = config::LoadedConfig::load(&config)?;
            let plan = planner::plan(&loaded)?;
            let json = serde_json::to_string_pretty(&plan)?;
            if let Some(output) = output {
                paths::write_atomic(&output, json.as_bytes())?;
                println!("Plan escrito en {}", output.display());
            } else {
                println!("{json}");
            }
            Ok(())
        }
        Command::Build {
            config,
            output,
            keep_staging,
        } => build::build(
            &config,
            output.as_deref(),
            cli.engine.as_deref(),
            keep_staging,
        ),
        Command::Install {
            apks,
            device,
            fresh,
            code_update,
        } => install::install(&apks, device.as_deref(), fresh, code_update),
        Command::Keys { command } => match command {
            KeyCommand::Backup {
                application_id,
                destination,
            } => signing::backup(&application_id, &destination),
        },
        Command::Clean => paths::clean_cache(),
    }
}
