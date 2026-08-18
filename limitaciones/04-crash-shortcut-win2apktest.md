# Limitación 04: crash al ejecutar Win2APKTest desde un shortcut

- **Proyecto:** Win2APK
- **Aplicación:** Winlator 11.1 modificada
- **Estado:** resuelta experimentalmente
- **Fecha de registro:** 2026-08-18

## Descripción

La aplicación Windows funcionaba cuando se abría directamente desde el administrador de archivos del contenedor, pero Winlator se cerraba al ejecutar el shortcut automático `Win2APKTest.desktop`.

## Evidencia exacta

El mensaje registrado por `logcat` fue:

```text
FATAL EXCEPTION: pool-4-thread-1
java.lang.StringIndexOutOfBoundsException: begin 0, end -1, length 28
    at com.winlator.core.FileUtils.getDirname(FileUtils.java:258)
    at com.winlator.XServerDisplayActivity.getWineStartCommand(XServerDisplayActivity.java:963)
    at com.winlator.XServerDisplayActivity.setupXEnvironment(XServerDisplayActivity.java:498)
    at com.winlator.XServerDisplayActivity.lambda$onCreate$2(XServerDisplayActivity.java:274)
```

## Análisis técnico

El shortcut contenía una ruta DOS escapada:

```text
Exec=wine C:\\Win2APKTest\\Win2APKTest.exe
```

`Shortcut` enviaba esa ruta a `StringUtils.unescapeDOSPath`. La implementación anterior eliminaba también las barras que separan directorios. Como resultado, `FileUtils.getDirname` no encontraba `/` ni `\\` y recibía un índice `-1`.

## Solución aplicada

Se reemplazó el desescape basado en expresiones regulares por una inversión explícita de `escapeDOSPath`:

- `\\\\` se convierte en `\\`.
- `\\ ` se convierte en un espacio.
- Las barras simples existentes se conservan.

## Resultado

La APK recompiló con `BUILD SUCCESSFUL`. En el Lenovo TB-J606F, después de instalar la corrección, el shortcut se mostró en `Shortcuts`, `XServerDisplayActivity` inició y `logcat` registró `Win2APKTest.exe` sin un nuevo `FATAL EXCEPTION`.

## Referencias

- [Parser de shortcuts](../winlator/app/app/src/main/java/com/winlator/container/Shortcut.java)
- [Desescape corregido](../winlator/app/app/src/main/java/com/winlator/core/StringUtils.java)
- [Ejecución de depuración](../ejecuciones/06-debug-shortcut-win2apktest-lenovo/matriz.md)
