# Ejecuciones de Win2APK

Cada registro corresponde a un intento experimental independiente. Las matrices conservan las condiciones y las observaciones disponibles en ese momento.

| ID | Ejecución | Tipo | Dispositivo | Resultado general | Matriz | Evidencia |
|---|---|---|---|---|---|---|
| EXEC-001 | Línea base manual en Winlator | Manual | Lenovo TB-J606F | Parcial: operación básica comprobada | [matriz.md](./01-linea-base-manual-winlator-tb-j606f/matriz.md) | [captura](./01-linea-base-manual-winlator-tb-j606f/evidencias/01-win2apktest-winlator-tb-j606f.png) |
| EXEC-002 | Verificación de compilación de Winlator | Compilación | N/A | Parcial: Java aprobado, APK no generado | [matriz.md](./02-compilacion-winlator/matriz.md) | N/A |
| EXEC-003 | Generación del APK de Winlator con contenedor por defecto | Compilación | N/A | Aprobado: APK debug generado | [matriz.md](./03-build-apk-winlator/matriz.md) | APK local no versionado |
| EXEC-004 | Verificación del contenedor predeterminado en Xiaomi Mi A3 | Dispositivo | Xiaomi Mi A3 | Aprobado: instalación, creación e idempotencia | [matriz.md](./04-prueba-dispositivo-mi-a3/matriz.md) | N/A |
| EXEC-005 | Aplicación de pruebas y shortcut preinstalados en el contenedor | Dispositivo | Redmi Note 8 | Aprobado: copia de 463 archivos y shortcut automático | [matriz.md](./05-prueba-aplicacion-preinstalada-redmi-note-8/matriz.md) | N/A |
| EXEC-006 | Depuración del shortcut de Win2APKTest | Dispositivo | Lenovo TB-J606F | Aprobado: crash reproducido y corregido | [matriz.md](./06-debug-shortcut-win2apktest-lenovo/matriz.md) | N/A |
| EXEC-007 | Winlator Core desde instalación limpia | Dispositivo | Lenovo TB-J606F | Aprobado: arranque oculto y aplicación automática con `com.winlator` | [matriz.md](./07-winlator-core-limpio-lenovo/matriz.md) | N/A |
| EXEC-008 | Winlator Core con `applicationId` dinámico | Dispositivo | Lenovo TB-J606F | Aprobado: `com.testappx`, rootfs transformado y aplicación automática | [matriz.md](./08-winlator-core-paquete-dinamico-lenovo/matriz.md) | N/A |
| EXEC-009 | Winlator Core con paquete variable y descriptor de rootfs | Dispositivo | Lenovo TB-J606F | Aprobado: `com.testapp`, alias heredado y aplicación automática | [matriz.md](./09-winlator-core-paquete-variable-fd-lenovo/matriz.md) | N/A |
| EXEC-010 | Instalación controlada de Cuphead mediante Wine | Instalación controlada | N/A | No aprobado: el descompresor del instalador no avanzó en Wine 11.0 | [matriz.md](./10-instalacion-cuphead-wine/matriz.md) | [registro](./10-instalacion-cuphead-wine/logs/instalacion.md) |
| EXEC-011 | Instalación visible de Cuphead mediante Lutris | Instalación controlada | N/A | Aprobado: instalación y primer inicio visibles en GE-Proton11-5; Android pendiente | [matriz.md](./11-instalacion-cuphead-lutris/matriz.md) | [registro](./11-instalacion-cuphead-lutris/logs/instalacion.md) |
| EXEC-012 | Compilación de APK con asset de Cuphead | Compilación automatizada | N/A | Fallido: `compressDebugAssets` devolvió `Required array size too large` | [matriz.md](./12-build-cuphead-apk/matriz.md) | [registro](./12-build-cuphead-apk/logs/build.md) |
| EXEC-013 | Generación de APKs locales de AAB con bundletool | Distribución AAB/PAD | Lenovo TB-J606F | Fallido: bundletool no firmó el asset pack ZIP de más de 4 GiB | [matriz.md](./13-bundletool-cuphead-aab/matriz.md) | [registro](./13-bundletool-cuphead-aab/logs/bundletool.md) |
| EXEC-014 | AAB segmentado de Cuphead instalado con bundletool | Distribución AAB/PAD y dispositivo | Lenovo TB-J606F | Aprobado experimentalmente: instalación, extracción y arranque de Cuphead.exe | [matriz.md](./14-aab-segmentado-cuphead-lenovo/matriz.md) | [captura](./14-aab-segmentado-cuphead-lenovo/evidencias/cuphead-game-menu.png) |
| EXEC-015 | Diagnóstico de acceso directo a asset packs | Diagnóstico AAB/PAD y regresión | Lenovo TB-J606F | No-go: packs como APK assets; fallback de extracción aprobado | [matriz.md](./15-diagnostico-acceso-directo-assetpack/matriz.md) | [diagnóstico](./15-diagnostico-acceso-directo-assetpack/logs/diagnostico.md) |

## Plantilla

Usar [plantilla-metricas.md](./plantilla-metricas.md) para crear la matriz del siguiente intento. No completar campos con datos que no estén respaldados por la ejecución.
