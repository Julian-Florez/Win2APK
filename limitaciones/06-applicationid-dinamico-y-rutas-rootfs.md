# Limitación 06: `applicationId` dinámico y rutas compiladas del rootfs

- **Proyecto:** Win2APK
- **Estado:** resuelta experimentalmente para `TestApp` sin límite artificial de longitud; conserva auditoría de assets y validación por dispositivo
- **Fecha de registro:** 2026-08-18
adb install -r /home/julian/Tesis/Win2APK/winlator/app/app/build/outputs/apk/debug/app-debug.apk
## Descripción

El `applicationId` de Android puede cambiarse durante la compilación, pero la publicación actual de Winlator contiene rutas absolutas compiladas con `/data/data/com.winlator`. Cambiar el paquete permite instalar la APK, pero no basta para que el rootfs funcione si esas rutas no se transforman.

## Contexto técnico

- Dispositivo: Lenovo TB-J606F, serial `HA1QXMW2`.
- APK probada: `11.1-core`, código `28`, ABI `arm64-v8a`.
- Configuración experimental: `applicationIdBase=com.winlator`, `deriveApplicationIdFromFolder=true`, carpeta `TestApp`.
- La aplicación no requiere root.

## Reproducción o evidencia

Con `com.winlator.testapp`, el filesystem y el shortcut se crearon, pero el proceso inicial no pudo ejecutar Box64:

```text
java.io.IOException: Cannot run program "/data/user/0/com.winlator.testapp/files/rootfs/usr/local/bin/box64": error=13, Permission denied
```

Después de corregir el intérprete ELF del binario, Box64 inició, pero el rootfs continuó usando una ruta compilada del paquete anterior:

```text
wine: chdir to /data/data/com.winlator/files/rootfs/tmp/.wine-10396/server-fd2f-1084c : Permission denied
```

La inspección del rootfs identificó aproximadamente 165 archivos que contienen `/data/data/com.winlator`, incluidos binarios y bibliotecas. El número exacto corresponde a la publicación inspeccionada y no debe generalizarse a otras versiones.

## Impacto histórico

La derivación automática del paquete estaba implementada en Gradle, pero no podía habilitarse sin transformar el rootfs completo. Esta condición quedó resuelta para la publicación actual mediante una transformación de assets durante el build.

## Análisis técnico

El nombre del paquete se define en tiempo de compilación, mientras que el rootfs incluye binarios precompilados que conocen la ruta privada de la aplicación original. Cambiar solo el manifest, el `FileProvider` y el `applicationId` no actualiza esas rutas internas.

## Solución aplicada

La solución actual no restringe la longitud del nombre derivado. La configuración conserva la raíz original solo como referencia de transformación y define un alias de igual longitud:

```json
"applicationIdBase": "com",
"deriveApplicationIdFromFolder": true,
"rootfsPackageId": "com.winlator",
"rootfsPathAlias": "/proc/self/fd/3"
```

`prepareCoreAssets` reescribe `rootfs.tzst`, `rootfs_patches.tzst`, `container_pattern.tzst`, Box64 y los drivers que contienen rutas absolutas. Sustituye `/data/data/com.winlator` por `/proc/self/fd/3` con barras de relleno, manteniendo la longitud de los bytes embebidos y la validez de los binarios precompilados. Un launcher nativo abre la carpeta de datos de la aplicación como descriptor 3, conserva el descriptor durante `execve` y ejecuta Box64 directamente. CMake recibe las rutas del paquete dinámico para las librerías nativas de Winlator.

## Resultado

Con `com.winlator`, una instalación limpia preparó el entorno y ejecutó `Win2APKTest.exe` automáticamente. La ejecución histórica `EXEC-008` confirmó el enfoque anterior con `com.testappx`. La ejecución `EXEC-009` confirmó la solución actual con `com.testapp`, el launcher nativo y la ejecución automática en instalación limpia.

## Limitaciones pendientes

- N/R: validación en otra versión de Android o fabricante.
- Si se incorporan nuevos assets comprimidos con rutas absolutas, deben añadirse a `android.pathRewriteAssets`.
- Android sigue imponiendo la sintaxis de `applicationId`; no se pueden usar literalmente espacios, mayúsculas ni caracteres arbitrarios. La implementación normaliza el nombre, pero no limita artificialmente su longitud.
- La solución del descriptor fue verificada en Lenovo TB-J606F con Android 16/API 36; la compatibilidad con otros fabricantes o versiones queda N/R.

## Historial de fallos durante la eliminación del límite

Durante `EXEC-009` se registraron y corrigieron tres fallos intermedios: el shell heredaba `LD_LIBRARY_PATH` del rootfs, el descriptor podía no ocupar el número 3 y el descriptor apuntaba inicialmente a `files/rootfs` en lugar de a la carpeta de datos del paquete. La prueba final no mostró `bad ELF`, `No such file or directory` ni `Not a directory`, y dejó activos Box64, Wine y `Win2APKTest.exe`.

## Referencias

- [Plan de Winlator Core](../documentacion/02-plan-winlator-core.md)
- [Especificación de Winlator Core](../especificaciones/winlator-core.md)
- [Ejecución limpia del Core](../ejecuciones/07-winlator-core-limpio-lenovo/matriz.md)
- [Ejecución dinámica](../ejecuciones/08-winlator-core-paquete-dinamico-lenovo/matriz.md)
- [Ejecución variable con descriptor](../ejecuciones/09-winlator-core-paquete-variable-fd-lenovo/matriz.md)

## Ejecuciones asociadas

- [EXEC-007](../ejecuciones/07-winlator-core-limpio-lenovo/matriz.md)
- [EXEC-008](../ejecuciones/08-winlator-core-paquete-dinamico-lenovo/matriz.md)
- [EXEC-009](../ejecuciones/09-winlator-core-paquete-variable-fd-lenovo/matriz.md)
