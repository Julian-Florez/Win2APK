# EXEC-008: Winlator Core con paquete dinámico

- **Fecha:** 2026-08-18
- **Tipo:** instalación limpia y ejecución en dispositivo
- **Dispositivo:** Lenovo TB-J606F, serial `HA1QXMW2`
- **Android:** 16 / API 36
- **ABI:** `arm64-v8a`
- **Resolución reportada:** `1200x2000`
- **Configuración:** [`config/win2apk.json`](../../config/win2apk.json)
- **APK:** [`app-debug.apk`](../../winlator/app/app/build/outputs/apk/debug/app-debug.apk)
- **SHA-256 del APK:** `fc10b3f48b6accbb0fc04b0edcde9ad182f9c3aa417df071adbdf18809abbeb1`
- **Tamaño del APK:** `260852702` bytes

## Objetivo

Comprobar que el `applicationId` derivado de `TestApp` sea funcional y que el rootfs, Box64, los drivers sensibles a rutas y el shortcut usen el nuevo paquete.

## Condiciones

| Campo | Valor |
|---|---|
| `app.folderName` | `TestApp` |
| `android.applicationIdBase` | `com` |
| `android.deriveApplicationIdFromFolder` | `true` |
| `android.applicationId` resultante | `com.testappx` |
| `startup.coreMode` | `true` |
| `startup.autoLaunch` | `true` |
| `startup.closeCoreWhenApplicationExits` | `true` |

## Procedimiento

1. Compilar `:app:assembleDebug` con Java 17 y el SDK Android local.
2. Desinstalar la publicación estática `com.winlator` del dispositivo.
3. Instalar el APK mediante `adb install`.
4. Abrir `com.testappx` con `monkey`.
5. Esperar la preparación del rootfs y verificar actividad, procesos y archivos.

## Observaciones

- Gradle generó el paquete `com.testappx`.
- `prepareCoreAssets` registró 447 reemplazos en `rootfs.tzst`, además de reemplazos en `rootfs_patches.tzst`, `container_pattern.tzst`, Box64 y los drivers Gladio, Turnip, VirGL y Vortek.
- El log de ejecución inició Box64 con la ruta dinámica:

  ```text
  Starting: /data/user/0/com.testappx/files/rootfs/usr/local/bin/box64 wine explorer /desktop=nogui,1280x720 C:\windows\winhandler.exe /dir C:\\Win2APKTest "Win2APKTest.exe"
  esync: up and running.
  ```

- El proceso `Win2APKTest.exe` quedó activo junto con `wineserver`, `winedevice.exe` y `winhandler.exe`.
- La actividad superior fue `com.testappx/com.winlator.XServerDisplayActivity`.
- El ejecutable quedó en `files/rootfs/home/xuser-1/.wine/drive_c/Win2APKTest/Win2APKTest.exe`.
- El shortcut quedó en `files/rootfs/home/xuser-1/.wine/drive_c/users/xuser/Desktop/Win2APKTest.desktop`.
- La comprobación de los assets transformados no encontró el texto `com.winlator`.

## Interpretación

El paquete dinámico es funcional en la publicación probada: Android instala `com.testappx`, la preparación oculta termina, Box64 usa el intérprete ubicado dentro del rootfs dinámico y la aplicación Windows se abre automáticamente.

## Resultado

**Aprobado para la publicación `TestApp` en Lenovo TB-J606F.** La compatibilidad con otros dispositivos, versiones de rootfs o nombres de carpeta no fue medida en esta ejecución.

## Limitaciones observadas

- El sufijo derivado se mantiene en ocho caracteres para conservar la longitud de las rutas compiladas; nombres largos se reducen mediante prefijo y hash corto.
- Si se agregan assets `.tzst` con rutas absolutas nuevas, deben añadirse a `android.pathRewriteAssets` antes de compilar.
- Las advertencias SELinux de `ioctl` pertenecen a la ejecución del rootfs en este dispositivo y no impidieron el arranque del ejecutable.
