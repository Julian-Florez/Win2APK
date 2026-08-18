# Ejecución 06: depuración del shortcut de Win2APKTest

- **ID:** `EXEC-006`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** reproducción de crash, corrección, compilación y prueba mediante ADB
- **Resultado general:** aprobado después de corregir el parseo de rutas DOS
- **Método:** interacción mediante UI Automator/ADB y captura de `logcat`

## Objetivo

Reproducir el crash al ejecutar `Win2APKTest` desde la pantalla `Shortcuts`, identificar la causa y verificar la corrección sin afectar la ejecución directa desde el administrador de archivos del contenedor.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| APK | `app-debug.apk` | Salida de `assembleDebug` |
| Paquete | `com.winlator` | Instalación mediante ADB |
| Dispositivo | Lenovo TB-J606F | ADB, serial `HA1QXMW2` |
| Instalación de corrección | Aprobada | `adb install -r` devolvió `Success` |
| Shortcut | `Win2APKTest.desktop` | `users/xuser/Desktop/Win2APKTest.desktop` |
| Ejecutable observado | `Win2APKTest.exe` | Etiqueta de proceso en `logcat` |

## Matriz de criterios

| ID | Criterio | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | Reproducir el crash original | Aprobado | `logcat` con `FATAL EXCEPTION` | El proceso terminó al pulsar el shortcut antes de la corrección |
| M-02 | Identificar la excepción | Aprobado | `StringIndexOutOfBoundsException` | Ocurrió en `FileUtils.getDirname` con índice final `-1` |
| M-03 | Compilar la corrección | Aprobado | `BUILD SUCCESSFUL` | Gradle terminó sin errores |
| M-04 | Mostrar `Win2APKTest` en Shortcuts | Aprobado | UI Automator encontró `text="Win2APKTest"` | El shortcut fue cargado por `ShortcutsFragment` |
| M-05 | Ejecutar el shortcut corregido | Aprobado | Actividad mostrada y proceso activo | `pidof com.winlator` devolvió `12728` después del lanzamiento |
| M-06 | Iniciar el ejecutable Windows | Aprobado | Etiquetas `start.exe`, `winhandler.exe` y `Win2APKTest.exe` en `logcat` | No apareció un nuevo `FATAL EXCEPTION` |

## Observación del fallo

Antes de la corrección, `logcat` conservó este mensaje:

```text
FATAL EXCEPTION: pool-4-thread-1
java.lang.StringIndexOutOfBoundsException: begin 0, end -1, length 28
    at com.winlator.core.FileUtils.getDirname(FileUtils.java:258)
    at com.winlator.XServerDisplayActivity.getWineStartCommand(XServerDisplayActivity.java:963)
    at com.winlator.XServerDisplayActivity.setupXEnvironment(XServerDisplayActivity.java:498)
```

La ejecución directa no pasaba por la lectura del `.desktop`; el shortcut sí pasaba por `Shortcut` y entregaba una ruta sin separadores válidos a `getDirname`.

## Corrección aplicada

Se actualizó [`StringUtils.unescapeDOSPath`](../../winlator/app/app/src/main/java/com/winlator/core/StringUtils.java) para invertir el escape de `escapeDOSPath` conservando las barras de las rutas Windows y desescapando los espacios por separado.

## Resultado posterior

Después de instalar la APK corregida, `Win2APKTest` apareció en `Shortcuts`, `XServerDisplayActivity` se mostró correctamente y `logcat` registró el inicio de `Win2APKTest.exe` sin repetir la excepción fatal.
