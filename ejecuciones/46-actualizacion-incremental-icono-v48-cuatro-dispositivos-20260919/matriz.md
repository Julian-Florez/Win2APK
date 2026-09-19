# Ejecución 46: actualización incremental de la app con icono personalizado

- **ID:** `EXEC-046`
- **Fecha:** `2026-09-19`
- **Tipo:** distribución incremental y verificación ADB
- **Resultado general:** aprobado para actualización no destructiva
- **Método:** construir la APK debug con el certificado que ya tenían las instalaciones, aplicar `adb install -r` secuencialmente y comparar el tamaño de `files` antes y después.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead empaquetado mediante Win2APK | APK local |
| Versión | `versionCode=48`; `11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core` | `dumpsys package` y configuración de compilación |
| Ejecutable | N/R; no se lanzó el juego durante esta ejecución | Alcance limitado a actualización |
| Publicación/hash | APK debug; SHA-256 `ba3b03d3e1dd6d0b5901e0f394f06e8cf41d05887044daa2472bd9bfaec6660c` | APK compilada localmente |
| Tamaño de APK | 294743438 bytes | `stat` |
| Firma | SHA-256 del certificado `6dd429199ee34b21a52d219d2eeff6b4fc4669dece1b46a91fbfce54bc32b8bd` | APK verifier y `$HOME/.android/debug.keystore` |
| Método | `adb install -r` | No se usó `uninstall`, `pm clear` ni instalación fría |
| Entorno | Host Linux; cuatro dispositivos conectados por ADB, Pixel por red | Salida ADB |
| Versión de Winlator | N/R | No se abrió el entorno |
| Contenedor/configuración | Datos existentes de Cuphead; no se reemplazaron | Comparación de `files` |
| Fecha y hora de inicio | 2026-09-19; hora exacta de inicio N/R | La salida conservó solo el tiempo por dispositivo |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación incremental | Aprobado | 4/4 dispositivos | `adb install -r`, APK firmada con el certificado existente | [log de instalación](./logs/instalacion-incremental.log) | La primera APK fue rechazada por firma distinta; no se borró ninguna instalación. |
| M-02 | Primer inicio | N/R | N/R | El juego no se lanzó | N/A | No forma parte de esta actualización. |
| M-03 | Aperturas posteriores | N/R | N/R | El juego no se lanzó | N/A | No forma parte de esta actualización. |
| M-04 | Operación básica | N/R | N/R | No se ejecutó Cuphead | N/A | Requiere una ejecución de juego separada. |
| M-05 | Aislamiento de archivos | Aprobado experimentalmente | `files` sin cambio en los cuatro equipos | Medición con `run-as com.cuphead du -sk files` | [estado ADB](./evidencias/estado-final-20260919.txt) | No prueba compatibilidad universal. |
| M-06 | Persistencia de archivos | Aprobado experimentalmente | Delta `0 KiB` por dispositivo | Comparación antes/después de `adb install -r` | [estado ADB](./evidencias/estado-final-20260919.txt) | Los datos privados se conservaron durante esta actualización. |
| M-07 | Tamaño del APK | Registrado | 294743438 bytes | APK debug con icono generado | [metadatos APK](./evidencias/metadatos-apk-20260919.txt) | El tamaño no incluye los datos privados ya instalados. |
| M-08 | Tiempo de instalación | Registrado | Pixel 26 s; tablet 13 s; Redmi 12 s; Xiaomi 11 s | Transferencia e instalación secuencial por ADB | [log de instalación](./logs/instalacion-incremental.log) | Es tiempo del comando ADB, no tiempo de primer frame. |
| M-09 | Tiempo de primer inicio | N/A | N/R | No se lanzó el juego | N/A | Pendiente de una prueba de ejecución. |
| M-10 | Tiempo de aperturas posteriores | N/A | N/R | No se lanzó el juego | N/A | Pendiente de una prueba de ejecución. |
| M-11 | Tasa de éxito de actualización | Aprobado experimentalmente | 4/4 | Cuatro dispositivos concretos, misma APK y mismo certificado | [log de instalación](./logs/instalacion-incremental.log) | No representa todos los dispositivos Android. |
| M-12 | Pasos manuales en el dispositivo | Registrado | Dispositivos ya conectados; resto automatizado | El usuario no tuvo que borrar datos | [log de instalación](./logs/instalacion-incremental.log) | No se contó el trabajo previo de conexión ADB. |

## Dispositivos

| Dispositivo | Android/API | ABI | Resolución | Instalación | `files` antes → después (KiB) | Tiempo ADB | Resultado |
|---|---|---|---|---|---:|---:|---|
| Google Pixel 9a (`pixel-9a`) | 17/API 37 | arm64-v8a | 1080×2424 | `adb install -r` aprobado | 6713230 → 6713230 | 26 s | Datos conservados |
| Lenovo TB-J606F (`lenovo-tb-j606f`) | 16/API 36 | arm64-v8a, armeabi-v7a, armeabi | 1200×2000 | `adb install -r` aprobado | 6734746 → 6734746 | 13 s | Datos conservados |
| Xiaomi Redmi Note 8 (`redmi-note-8`) | 16/API 36 | arm64-v8a, armeabi-v7a, armeabi | 1080×2340 | `adb install -r` aprobado | 6734746 → 6734746 | 12 s | Datos conservados |
| Xiaomi Mi A3 (`mi-a3`) | 16/API 36 | arm64-v8a, armeabi-v7a, armeabi | 720×1560 | `adb install -r` aprobado | 6734778 → 6734778 | 11 s | Datos conservados |

## Fallos y decisiones

- **Limitación relacionada:** [firma incompatible durante la actualización](../../limitaciones/34-firma-incompatible-actualizacion-incremental.md).
- **Mensaje exacto:** `INSTALL_FAILED_UPDATE_INCOMPATIBLE: Existing package com.cuphead signatures do not match newer version; ignoring!`
- **Decisión:** no desinstalar ni limpiar datos; reconstruir la misma APK con el almacén de firma existente y repetir `adb install -r`.

## Evidencias

- [Log de transferencia e instalación](./logs/instalacion-incremental.log)
- [Estado de paquete y persistencia posterior](./evidencias/estado-final-20260919.txt)
- [Metadatos, hash y firma de la APK](./evidencias/metadatos-apk-20260919.txt)

## Repetibilidad y pendientes

- [x] Registrar la versión, hash, firma, dispositivos y tamaños antes/después.
- [x] Separar la actualización incremental de una instalación fría.
- [ ] Lanzar Cuphead y verificar operación gráfica en una ejecución posterior.
- [ ] Definir una firma de distribución persistente para publicaciones fuera del entorno de desarrollo.
