# EXEC-009: Winlator Core con paquete variable y descriptor de rootfs

- **Fecha:** 2026-08-18
- **Tipo:** compilación, instalación limpia y ejecución en dispositivo
- **Dispositivo:** Lenovo TB-J606F, serial `HA1QXMW2`
- **Android:** 16 / API 36
- **ABI:** `arm64-v8a`
- **Resolución reportada:** `1200x2000`
- **Configuración:** [`config/win2apk.json`](../../config/win2apk.json)
- **APK:** [`app-debug.apk`](../../winlator/app/app/build/outputs/apk/debug/app-debug.apk)
- **SHA-256 del APK:** `fbd978c1fc51e8db927caae1524db6d85e6e19c1531fba444f6a045064ad365a`
- **Tamaño del APK:** `262719844` bytes

## Objetivo

Comprobar que el paquete derivado no dependa de una longitud fija y que las rutas embebidas del rootfs puedan resolverse mediante un descriptor heredado, sin root ni interfaz general.

## Condiciones

| Campo | Valor |
|---|---|
| `app.folderName` | `TestApp` |
| `android.applicationIdBase` | `com` |
| `android.deriveApplicationIdFromFolder` | `true` |
| `android.applicationId` resultante | `com.testapp` |
| `android.rootfsPathAlias` | `/proc/self/fd/3` |
| `startup.coreMode` | `true` |
| `startup.autoLaunch` | `true` |
| `startup.closeCoreWhenApplicationExits` | `true` |
| Root | No requerido |

## Procedimiento

1. Ejecutar `:app:assembleDebug` con Java 17 y el SDK Android local.
2. Verificar con `aapt` que el paquete del APK sea `com.testapp`.
3. Verificar que los assets generados no contengan `/data/data/com.winlator` y sí el alias `/proc/self/fd/3`.
4. Extraer una copia de `rootfs.tzst` y validar los encabezados ELF de `wine`, `wineserver`, `wine` Unix y `ntdll.so`.
5. Desinstalar `com.testapp`, instalar el APK mediante `adb install` y abrirlo con `monkey`.
6. Revisar actividad, procesos y logcat después de la preparación automática.

## Observaciones

- Gradle terminó con `BUILD SUCCESSFUL`.
- `aapt` reportó `package: name='com.testapp'`.
- Los assets transformados no conservaron el texto `/data/data/com.winlator`; los assets sensibles mostraron `/proc/self/fd/3/////////files/rootfs`.
- Los ELF principales extraídos del rootfs conservaron encabezados válidos.
- La actividad superior fue `com.testapp/com.winlator.XServerDisplayActivity`.
- Quedaron activos `wineserver`, dos procesos `winedevice.exe`, `winhandler.exe` y `Win2APKTest.exe`.
- El launcher inició Box64 desde `/data/user/0/com.testapp/files/rootfs/usr/local/bin/box64`.
- No apareció `bad ELF`, `No such file or directory`, `Not a directory`, `Unable to start` ni una excepción fatal de Android en la comprobación final.

## Interpretación

El alias de rootfs funciona con una aplicación cuyo paquete no tiene el sufijo fijo anterior. El puente nativo abre la carpeta de datos del paquete, fuerza el descriptor 3 y conserva ese descriptor durante `execve`; las rutas embebidas resuelven entonces el rootfs real y Box64 puede iniciar Wine.

## Resultado

**Aprobado para la publicación `TestApp` en Lenovo TB-J606F.** La prueba valida el flujo de instalación limpia y ejecución automática para `com.testapp`. La compatibilidad con otros dispositivos, versiones de Android y nombres con caracteres fuera de la sintaxis de `applicationId` queda N/R.

## Fallos intermedios corregidos

- El shell de Android heredaba `LD_LIBRARY_PATH` del rootfs y cargaba el `libc.so` equivocado.
- El descriptor abierto por el launcher no tenía necesariamente el número 3.
- El descriptor apuntaba inicialmente a `files/rootfs`, aunque el alias conserva ese sufijo y requiere la carpeta de datos del paquete.
