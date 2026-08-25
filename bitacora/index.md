# Bitácora de fallos y limitaciones

Este índice reúne los fallos y restricciones técnicas detectados durante el desarrollo de Win2APK. Los detalles se conservan en `../limitaciones/` y las pruebas asociadas en `../ejecuciones/`.

| Nº | Limitación | Fecha | Estado | Ejecución relacionada | Informe detallado |
|---:|---|---|---|---|---|
| 01 | Inicialización de CoreCLR/GC en Winlator | 2026-08-07 | Resuelta experimentalmente | [EXEC-001](../ejecuciones/01-linea-base-manual-winlator-tb-j606f/matriz.md) | [01-error-coreclr-gc-winlator.md](../limitaciones/01-error-coreclr-gc-winlator.md) |
| 02 | Entorno incompleto para compilar Winlator | 2026-08-18 | resuelta experimentalmente | [EXEC-002](../ejecuciones/02-compilacion-winlator/matriz.md), [EXEC-003](../ejecuciones/03-build-apk-winlator/matriz.md) | [02-entorno-compilacion-winlator.md](../limitaciones/02-entorno-compilacion-winlator.md) |
| 03 | Duplicación de bibliotecas nativas durante el empaquetado | 2026-08-18 | resuelta experimentalmente | [EXEC-003](../ejecuciones/03-build-apk-winlator/matriz.md) | [03-duplicacion-bibliotecas-nativas.md](../limitaciones/03-duplicacion-bibliotecas-nativas.md) |
| 04 | Crash al ejecutar Win2APKTest desde un shortcut | 2026-08-18 | resuelta experimentalmente | [EXEC-006](../ejecuciones/06-debug-shortcut-win2apktest-lenovo/matriz.md) | [04-crash-shortcut-win2apktest.md](../limitaciones/04-crash-shortcut-win2apktest.md) |
| 05 | Primer toque requerido en APK normal sin root | 2026-08-18 | aceptada para el diseño | N/R | [05-inicio-winlator-core-sin-root.md](../limitaciones/05-inicio-winlator-core-sin-root.md) |
| 06 | `applicationId` dinámico incompatible con rutas compiladas del rootfs publicado | 2026-08-18 | resuelta experimentalmente sin límite artificial de longitud | [EXEC-007](../ejecuciones/07-winlator-core-limpio-lenovo/matriz.md), [EXEC-008](../ejecuciones/08-winlator-core-paquete-dinamico-lenovo/matriz.md), [EXEC-009](../ejecuciones/09-winlator-core-paquete-variable-fd-lenovo/matriz.md) | [06-applicationid-dinamico-y-rutas-rootfs.md](../limitaciones/06-applicationid-dinamico-y-rutas-rootfs.md) |
| 07 | Instalador de Cuphead sin progreso en Wine | 2026-08-24 | detectada | [EXEC-010](../ejecuciones/10-instalacion-cuphead-wine/matriz.md) | [07-instalador-cuphead-no-avanza-en-wine.md](../limitaciones/07-instalador-cuphead-no-avanza-en-wine.md) |
| 08 | Asset de Cuphead excede la capacidad del empaquetado APK | 2026-08-24 | reproducida | [EXEC-012](../ejecuciones/12-build-cuphead-apk/matriz.md) | [08-asset-cuphead-excede-empaquetado-apk.md](../limitaciones/08-asset-cuphead-excede-empaquetado-apk.md) |
| 09 | Bundletool no firma el asset pack ZIP de más de 4 GiB | 2026-08-24 | detectada | [EXEC-013](../ejecuciones/13-bundletool-cuphead-aab/matriz.md) | [09-bundletool-zip64-asset-pack-cuphead.md](../limitaciones/09-bundletool-zip64-asset-pack-cuphead.md) |
| 10 | Referencia obsoleta durante la transición a asset packs segmentados | 2026-08-24 | resuelta experimentalmente | [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md) | [10-variable-obsoleta-build-segmentado.md](../limitaciones/10-variable-obsoleta-build-segmentado.md) |
| 11 | Asset packs APK assets sin ruta directa para Wine | 2026-08-24 | reproducida; acceso directo no viable en bundletool local | [EXEC-015](../ejecuciones/15-diagnostico-acceso-directo-assetpack/matriz.md) | [11-assetpack-apk-assets-sin-ruta-directa.md](../limitaciones/11-assetpack-apk-assets-sin-ruta-directa.md) |

## Criterio de lectura

El informe 01 documenta el fallo de la publicación inicial y la corrección experimental. La ejecución `EXEC-001` documenta la prueba manual de la publicación por carpeta posterior a la corrección; no debe interpretarse como una repetición del fallo original.
