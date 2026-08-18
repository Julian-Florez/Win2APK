# Ejecución 07: Winlator Core desde instalación limpia

- **ID:** `EXEC-007`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** compilación, instalación limpia y arranque automático mediante ADB
- **Resultado general:** aprobado para el flujo Core con `applicationId` estable `com.winlator`
- **Método:** `gradlew assembleDebug`, `adb uninstall`, `adb install`, `monkey`, `logcat` y `dumpsys`

## Objetivo

Verificar que una instalación limpia prepare el rootfs, cree el contenedor, copie la aplicación Windows, genere el shortcut y abra el ejecutable sin mostrar la interfaz general de Winlator.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| APK | `app-debug.apk` | Salida de `assembleDebug` |
| Tamaño | 203 MB | Sistema de archivos local |
| SHA-256 | `a95c77cffaa859ff9adcf863770479c507ab2621b6b54c5cfbaf83f74cde86dd` | `sha256sum` |
| Paquete | `com.winlator` | `aapt dump badging` |
| Etiqueta | `TestApp` | `aapt dump badging` |
| Versión | `11.1-core`, código `28` | `aapt dump badging` |
| Dispositivo | Lenovo TB-J606F, serial `HA1QXMW2` | ADB |
| Android/API | N/R | No se volvió a registrar en este intento |
| ABI | `arm64-v8a` | Configuración Gradle |
| Instalación limpia | `adb uninstall` y `adb install` devolvieron `Success` | ADB |

## Matriz de criterios

| ID | Criterio | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | Compilar el APK Core | Aprobado | `BUILD SUCCESSFUL` | Se usó JDK 17 y SDK Android local |
| M-02 | Iniciar desde instalación limpia | Aprobado | `monkey -p com.winlator 1` | Requirió únicamente el toque simulado por ADB |
| M-03 | Ocultar la interfaz general | Aprobado | `dumpsys activity` | La actividad superior fue `XServerDisplayActivity`; `MainActivity` quedó finalizada |
| M-04 | Crear el filesystem y contenedor | Aprobado | `run-as` encontró el rootfs y la carpeta de aplicación | Preparación sin selector visible |
| M-05 | Copiar `Win2APKTest.exe` | Aprobado | `files/rootfs/home/xuser-1/.wine/drive_c/Win2APKTest/Win2APKTest.exe` | El archivo existió después del primer arranque |
| M-06 | Crear el shortcut | Aprobado | `Win2APKTest.desktop` y contenido leído por `run-as` | `Exec=wine C:\\Win2APKTest\\Win2APKTest.exe` |
| M-07 | Abrir automáticamente la aplicación | Aprobado | Procesos `winhandler.exe` y `Win2APKTest.exe` | `logcat` registró `esync: up and running` |
| M-08 | Cerrar Core al terminar | Implementado; prueba de cierre natural N/R | Callback Core en código | El proceso permaneció activo durante la ventana de observación |
| M-09 | Mantener ejecución sin root | Aprobado en este dispositivo | No se usó root | Resultado limitado al dispositivo probado |

## Observación

El archivo JSON controla el arranque oculto, la configuración del contenedor, la aplicación, el shortcut y las preferencias runtime. En esta publicación se mantiene `android.applicationId` como `com.winlator` porque el rootfs y sus binarios contienen rutas compiladas con ese identificador.

## Pendientes

- Recompilar o transformar todo el rootfs para habilitar de forma segura un `applicationId` derivado distinto.
- Repetir la prueba de salida natural cerrando `Win2APKTest.exe` desde su ventana.
