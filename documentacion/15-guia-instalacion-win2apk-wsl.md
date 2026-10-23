# 15. Guía reproducible para instalar y usar Win2APK en WSL2

- **Fecha:** 2026-09-30
- **Estado:** guía operativa para la implementación actual
- **Propósito:** preparar un equipo Windows con Ubuntu en WSL2 para compilar el
  CLI de Win2APK, instalar su toolchain administrado, empaquetar una carpeta
  Windows preparada y distribuirla a un dispositivo Android.
- **Alcance:** WSL2 sobre Windows en arquitectura `x86_64`.
- **Limitación:** el CLI comprueba explícitamente Linux `x86_64`; esta guía no
  cubre WSL1, Windows nativo, Linux ARM64 ni la ejecución del juego en Android.

## 1. Arquitectura del flujo

```text
Windows
  └─ WSL2 Ubuntu (Linux x86_64)
       ├─ Rust y cargo
       ├─ CLI Win2APK
       ├─ toolchain administrado: JDK, SDK, NDK, CMake, ADB y bundletool
       ├─ motor Winlator en winlator/app
       └─ carpeta Windows preparada
              ↓
       AAB + APKS + reportes
              ↓
       ADB mediante USBIPD o conexión inalámbrica
              ↓
       dispositivo Android
```

WSL2 se utiliza como entorno Linux para el empaquetado. El acceso USB no se
hereda automáticamente desde Windows y requiere `usbipd-win` o ADB inalámbrico.

## 2. Requisitos previos

Se necesita:

- Windows con WSL2 habilitado.
- Ubuntu instalado dentro de WSL2.
- Arquitectura del equipo `x86_64`.
- Conexión a internet durante la primera configuración.
- Espacio disponible para el repositorio, el motor Winlator, el juego, el
  staging y los artefactos de salida.
- Una carpeta Windows ya preparada, con su ejecutable, bibliotecas, recursos y
  dependencias.
- Un dispositivo Android con API 26 o posterior para las pruebas de instalación.

El CLI no ejecuta instaladores de Windows. Recibe una carpeta ya preparada.

## 3. Instalar y comprobar WSL2

Desde PowerShell como administrador:

```powershell
wsl --install -d Ubuntu
```

Reinicia Windows si el instalador lo solicita. Después comprueba la versión:

```powershell
wsl -l -v
```

Ubuntu debe mostrar `2` en la columna `VERSION`. Si muestra `1`:

```powershell
wsl --set-version Ubuntu 2
```

Para abrir la distribución:

```powershell
wsl -d Ubuntu
```

Dentro de Ubuntu, comprueba la arquitectura:

```bash
uname -m
```

El resultado esperado es:

```text
x86_64
```

## 4. Preparar dependencias de Ubuntu

Dentro de Ubuntu en WSL2:

```bash
sudo apt update

sudo apt install -y \
  git \
  curl \
  ca-certificates \
  build-essential \
  pkg-config \
  unzip \
  zip \
  usbutils
```

Estas dependencias permiten descargar el código, compilar Rust, procesar
artefactos y verificar dispositivos USB. Android Studio, Java y el SDK de
Android no son necesarios antes de ejecutar `win2apk setup`.

## 5. Instalar Rust

Instala Rust con `rustup` dentro de WSL2:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup default stable
rustup update stable
```

Comprueba las herramientas:

```bash
rustc --version
cargo --version
```

No ejecutes Rust, `cargo`, `setup` ni el build con `sudo`. El toolchain y las
claves de firma deben pertenecer al usuario que construirá el proyecto.

## 6. Elegir dónde guardar los repositorios

Para obtener mejor rendimiento, guarda los repositorios dentro del sistema de
archivos Linux de WSL:

```text
/home/<usuario>/proyectos/
```

Evita construir desde `/mnt/c/Users/...`. Las rutas de Windows son accesibles,
pero las operaciones sobre carpetas grandes suelen ser más lentas desde WSL.

El juego puede permanecer en una unidad Windows si no se quiere duplicar; en
ese caso se referencia desde el JSON con una ruta `/mnt`.

## 7. Descargar Win2APK y el motor Winlator

Desde Ubuntu:

```bash
mkdir -p "$HOME/proyectos"
cd "$HOME/proyectos"

git clone \
  --branch codex/no-duplicate-game-data \
  https://github.com/Julian-Florez/Win2APK.git

cd Win2APK

git clone \
  --branch agent/winlator-core-dynamic-package \
  --recurse-submodules \
  https://github.com/Julian-Florez/winlator.git \
  winlator
```

La opción `--recurse-submodules` obtiene también los componentes que necesita
el motor Android. Verifica la plantilla:

```bash
test -f winlator/app/gradlew && echo "gradlew encontrado"
test -f winlator/app/app/build.gradle && echo "plantilla Android encontrada"
```

Si los submódulos no están completos:

```bash
git -C winlator submodule update --init --recursive
```

## 8. Compilar el CLI

Desde `/home/<usuario>/proyectos/Win2APK`:

```bash
cargo build --release --package win2apk
```

Comprueba el ejecutable:

```bash
./target/release/win2apk --version
```

La ruta del binario será:

```text
target/release/win2apk
```

La prueba opcional del código es:

```bash
cargo test --package win2apk
```

## 9. Instalar el toolchain administrado

Ejecuta:

```bash
./target/release/win2apk setup
```

Durante este paso el CLI descarga y verifica:

- JDK 17 de Eclipse Temurin.
- Android command-line tools.
- Android SDK API 36.
- Build Tools 36.0.0.
- NDK 30.0.15729638.
- CMake 3.22.1.
- platform-tools, incluido ADB.
- bundletool 1.18.3.

El comando muestra las licencias de Android. Deben aceptarse para continuar.

El toolchain se guarda normalmente en:

```text
~/.config/win2apk/
~/.local/share/win2apk/
~/.cache/win2apk/
```

La ubicación exacta del SDK se muestra con `doctor`. Si `setup` se interrumpe,
vuelve a ejecutarlo como usuario normal.

## 10. Diagnosticar el entorno

```bash
./target/release/win2apk doctor \
  --engine "$PWD/winlator/app"
```

El diagnóstico debe comprobar correctamente:

- Linux `x86_64`.
- JDK.
- Android SDK.
- ADB.
- bundletool.
- `winlator/app/gradlew`.
- `winlator/app/app/build.gradle`.

El resultado esperado termina con:

```text
Diagnóstico aprobado.
```

## 11. Configurar el acceso USB desde Windows

WSL2 no siempre recibe directamente el teléfono conectado por USB. La opción
recomendada es `usbipd-win`.

### 11.1 Instalar usbipd-win

Desde PowerShell como administrador:

```powershell
winget install --exact --interactive dorssel.usbipd-win
```

Conecta el teléfono y lista los dispositivos USB:

```powershell
usbipd list
```

Identifica el `BUSID`, por ejemplo `4-4`.

### 11.2 Asociar el dispositivo con WSL

En PowerShell como administrador:

```powershell
usbipd bind --busid 4-4
usbipd attach --wsl --busid 4-4
```

El número `4-4` debe sustituirse por el `BUSID` real.

### 11.3 Preparar Android

En el dispositivo:

1. Activa las opciones de desarrollador.
2. Activa la depuración USB.
3. Desbloquea el dispositivo.
4. Acepta la clave RSA cuando Android la solicite.

### 11.4 Comprobar USB desde WSL

Dentro de Ubuntu:

```bash
lsusb
```

Obtén la ruta del ADB administrado:

```bash
WIN2APK_SDK="$HOME/.local/share/win2apk/toolchains/android36-ndk30-jdk17-v1/android-sdk"
```

Comprueba el dispositivo:

```bash
"$WIN2APK_SDK/platform-tools/adb" devices
```

El resultado esperado es:

```text
List of devices attached
SERIAL_DEL_DISPOSITIVO    device
```

Si aparece `unauthorized`, desbloquea Android y acepta la autorización. Si no
aparece nada:

```bash
"$WIN2APK_SDK/platform-tools/adb" kill-server
"$WIN2APK_SDK/platform-tools/adb" start-server
"$WIN2APK_SDK/platform-tools/adb" devices
```

Para desconectar el dispositivo de WSL desde Windows:

```powershell
usbipd detach --busid 4-4
```

## 12. Alternativa: ADB inalámbrico

Si `usbipd-win` no funciona, Android puede conectarse mediante depuración
inalámbrica. Desde el ADB administrado:

```bash
"$WIN2APK_SDK/platform-tools/adb" pair IP_DEL_DISPOSITIVO:PUERTO_DE_EMPAREJAMIENTO
"$WIN2APK_SDK/platform-tools/adb" connect IP_DEL_DISPOSITIVO:5555
"$WIN2APK_SDK/platform-tools/adb" devices
```

El serial usado en la instalación será parecido a:

```text
192.168.1.25:5555
```

El ADB de Windows y el ADB de WSL son servidores independientes. Siempre debes
comprobar el dispositivo usando el ADB administrado dentro de WSL.

## 13. Preparar el JSON de la aplicación

Copia el ejemplo:

```bash
cp config/win2apk.json config/mi-aplicacion.json
```

Edita el archivo:

```bash
nano config/mi-aplicacion.json
```

Como mínimo, adapta estos campos:

```json
{
  "project": {
    "name": "Mi Aplicacion",
    "sourceFolder": "/mnt/c/Games/MiAplicacion",
    "entrypoint": "MiAplicacion.exe",
    "installDirectory": "MiAplicacion"
  },
  "android": {
    "applicationId": "com.ejemplo.miaplicacion",
    "versionCode": 1,
    "versionName": "1.0.0",
    "icon": "/mnt/c/Users/Usuario/Downloads/icono.png",
    "iconBackgroundColor": "#202124"
  }
}
```

Consideraciones para las rutas:

- `/mnt/c/Games/...` representa una carpeta de Windows.
- No uses `C:\\Games\\...` dentro del JSON.
- Una ruta relativa se resuelve respecto a la carpeta que contiene el JSON.
- `entrypoint` debe existir dentro de `sourceFolder`.
- El `applicationId` debe ser único y válido para Android.
- El icono puede ser PNG, JPEG, WebP o SVG según el soporte del CLI.

El JSON también define el modo de distribución, los asset packs, la configuración
de Wine/Winlator, el arranque y la configuración del contenedor. El contrato
completo está en [`especificaciones/cli-empaquetado.md`](../especificaciones/cli-empaquetado.md).

## 14. Validar y planificar

Valida el archivo antes de compilar:

```bash
./target/release/win2apk validate \
  config/mi-aplicacion.json
```

Calcula el plan de asset packs:

```bash
./target/release/win2apk plan \
  config/mi-aplicacion.json \
  --output dist/mi-aplicacion-plan.json
```

La validación y la planificación no deben modificar la carpeta fuente.

## 15. Construir el AAB y el APKS

Construye desde la raíz del repositorio:

```bash
./target/release/win2apk \
  --engine "$PWD/winlator/app" \
  build config/mi-aplicacion.json \
  --output dist/mi-aplicacion
```

La salida esperada es similar a:

```text
dist/mi-aplicacion/
├── mi-aplicacion-1.0.0.aab
├── mi-aplicacion-1.0.0.apks
├── build-report.json
├── checksums.sha256
├── payload-manifest.json
└── resolved-config.json
```

Para conservar el staging con fines de depuración:

```bash
./target/release/win2apk \
  --engine "$PWD/winlator/app" \
  build config/mi-aplicacion.json \
  --output dist/mi-aplicacion \
  --keep-staging
```

En una construcción normal se recomienda omitir `--keep-staging`, porque los
archivos intermedios consumen espacio adicional.

## 16. Instalar el APKS en Android

Obtén el serial con el ADB de WSL:

```bash
"$WIN2APK_SDK/platform-tools/adb" devices
```

Instala sin borrar una instalación existente:

```bash
./target/release/win2apk install \
  dist/mi-aplicacion/mi-aplicacion-1.0.0.apks \
  --device SERIAL_DEL_DISPOSITIVO
```

Para una instalación desde cero:

```bash
./target/release/win2apk install \
  dist/mi-aplicacion/mi-aplicacion-1.0.0.apks \
  --device SERIAL_DEL_DISPOSITIVO \
  --fresh
```

`--fresh` desinstala el `applicationId` detectado en `build-report.json` y elimina
los datos anteriores. No lo uses para una actualización que deba conservar datos.

## 17. Instalar el binario como comando global

Esta opción evita escribir la ruta completa del binario:

```bash
sudo install -m 0755 \
  target/release/win2apk \
  /usr/local/bin/win2apk
```

Comprueba:

```bash
win2apk --version
```

Aunque el binario esté en `/usr/local/bin`, `setup`, `build` e `install` deben
ejecutarse sin `sudo`.

## 18. Limpieza segura

Para borrar únicamente el staging regenerable:

```bash
./target/release/win2apk clean
```

Esta limpieza no sustituye la copia de seguridad de las claves de firma ni borra
el toolchain administrado. Antes de publicar actualizaciones, conserva la clave
de firma asociada al `applicationId`.

## 19. Flujo completo posterior a la primera instalación

```bash
cd "$HOME/proyectos/Win2APK"

./target/release/win2apk doctor \
  --engine "$PWD/winlator/app"

./target/release/win2apk validate \
  config/mi-aplicacion.json

./target/release/win2apk build \
  --engine "$PWD/winlator/app" \
  config/mi-aplicacion.json \
  --output dist/mi-aplicacion

./target/release/win2apk install \
  dist/mi-aplicacion/mi-aplicacion-1.0.0.apks \
  --device SERIAL_DEL_DISPOSITIVO
```

## 20. Solución de problemas

| Problema | Diagnóstico o solución |
|---|---|
| `Win2APK CLI sólo admite Linux x86_64` | Comprueba `uname -m`; WSL debe ser WSL2 sobre un equipo x86_64. |
| `JDK no encontrado` | Ejecuta `win2apk setup` como usuario normal. |
| `Android SDK no encontrado` | Repite `win2apk setup` y revisa la conexión a internet. |
| `ADB ausente` | Ejecuta `doctor` y verifica que el toolchain administrado esté completo. |
| El dispositivo aparece en Windows pero no en WSL | Ejecuta `usbipd attach --wsl`, comprueba `lsusb` y reinicia el servidor ADB. |
| `unauthorized` en ADB | Desbloquea el teléfono y acepta la clave RSA. |
| La instalación informa que la app ya existe | Usa otro `applicationId`, desinstala manualmente o usa `--fresh`. |
| `Missing generated asset-pack module` | Ejecuta el build desde la raíz de Win2APK y usa `--engine "$PWD/winlator/app"`. |
| `Missing Win2APK configuration` | Comprueba que el JSON y el comando se ejecutan desde el repositorio correcto. |
| Gradle no encuentra componentes del motor | Ejecuta `git -C winlator submodule update --init --recursive`. |
| El build es muy lento | Mueve el repositorio a `/home`, evitando `/mnt/c` para la compilación. |
| Falta espacio durante el build | Omite `--keep-staging`, elimina caché con `win2apk clean` y conserva una sola copia del payload. |

## 21. Evidencia y referencias del proyecto

- [README del proyecto](../README.md)
- [Especificación del CLI](../especificaciones/cli-empaquetado.md)
- [Versiones fijadas del toolchain](../toolchain.lock.json)
- [Decisión sobre el CLI Linux](./13-decision-cli-linux-configuracion-v2.md)

## Decisiones pendientes

- Probar formalmente el flujo completo en una instalación limpia de Ubuntu sobre
  WSL2 y registrar una ejecución reproducible.
- Decidir si se publicará un binario Linux precompilado para evitar la instalación
  de Rust en equipos usuarios.
- Documentar una ruta oficial de distribución para el motor Winlator y sus
  submódulos.
