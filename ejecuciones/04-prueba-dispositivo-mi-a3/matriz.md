# Ejecución 04: verificación del contenedor predeterminado en Xiaomi Mi A3

- **ID:** `EXEC-004`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** instalación y prueba de primer inicio
- **Resultado general:** aprobado para la creación e idempotencia del contenedor
- **Método:** instalación mediante ADB y lectura del almacenamiento privado de la aplicación

## Objetivo

Comprobar en un dispositivo Android que el APK generado instala Winlator, completa la instalación del `rootfs`, crea `Container-1` automáticamente y no crea contenedores adicionales al abrir la aplicación nuevamente.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| APK | `app-debug.apk` | Artefacto de EXEC-003 |
| Paquete | `com.winlator` | `aapt dump badging` y dispositivo |
| Dispositivo | Xiaomi Mi A3 | `adb shell getprop ro.product.model` |
| Android/API | Android 16 / API 36 | Propiedades del dispositivo |
| ABI | `arm64-v8a`, `armeabi-v7a`, `armeabi` | `ro.product.cpu.abilist` |
| Resolución lógica | 720×1560 | `wm size` |
| Instalación | Aprobada | `adb install -r` devolvió `Success` |
| RootFS | Versión 19 | `files/rootfs/.winlator/.rfs_version` |
| Winlator en ejecución | Sí | `pidof com.winlator` |

## Matriz de criterios

| ID | Criterio | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | Instalar el APK | Aprobado | `Success` de ADB | Se usó instalación de actualización con conservación de datos |
| M-02 | Iniciar la aplicación | Aprobado | Actividad `com.winlator/.MainActivity` y proceso activo | No se observó crash de la aplicación |
| M-03 | Instalar el `rootfs` | Aprobado | Versión `19` | El sistema de archivos quedó disponible dentro de `files/rootfs` |
| M-04 | Crear el contenedor automáticamente | Aprobado | `files/rootfs/home/xuser-1/.container` | Configuración contiene `name: Container-1` |
| M-05 | Conservar configuración predeterminada | Aprobado | Archivo `.container` | `graphicsDriver: turnip,gladio`; `box64Preset: INTERMEDIATE` |
| M-06 | No duplicar el contenedor en una segunda apertura | Aprobado | Solo `xuser-1` después del segundo inicio | No apareció `xuser-2` |
| M-07 | Ejecutar `Win2APKTest.exe` | N/R | N/A | Esta ejecución verificó Winlator y el contenedor, no la aplicación Windows |

## Observación

El primer inicio creó automáticamente el contenedor y dejó disponible su archivo de configuración. En la segunda apertura el almacenamiento mantuvo únicamente:

```text
xuser
xuser-1
```

El proceso permaneció activo después de ambas aperturas.

## Pendientes

- [ ] Ejecutar `Win2APKTest.exe` dentro de `Container-1`.
- [ ] Confirmar visualmente la ventana y la interacción del botón.
- [ ] Repetir la prueba en los demás dispositivos objetivo.

