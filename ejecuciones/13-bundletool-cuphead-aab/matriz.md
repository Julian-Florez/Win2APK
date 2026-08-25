# Ejecución 13: generación de APKs locales desde AAB con bundletool

- **ID:** `EXEC-013`
- **Fecha:** 2026-08-24
- **Tipo:** prueba de distribución AAB/PAD
- **Resultado general:** Fallido al firmar el asset pack grande; no se generó un conjunto instalable
- **Método:** `bundletool 1.18.3 build-apks --local-testing --connected-device`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | `config/win2apk.json` |
| AAB | `winlator/app/app/build/outputs/bundle/debug/app-debug.aab` | Generado por `bundleDebug` con éxito |
| Tamaño del AAB | `5.043.467.729` bytes | Medición local |
| Asset pack | `cuphead_data` | Entrega `install-time` |
| Asset comprimido | `cuphead.tzst` | `4.782.573.186` bytes |
| Bundletool | `1.18.3` | JAR oficial descargado localmente |
| Dispositivo objetivo | Lenovo TB-J606F (`HA1QXMW2`) | API 36; aproximadamente 70 GB libres observados |
| Java | JDK 17 | Requerido por el Gradle del proyecto |
| Fecha y hora | 2026-08-24, aproximadamente 20:56 -0500 | Registro de terminal |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | AAB con módulo de asset pack | Aprobado | 1 AAB | `bundleDebug` | [log del build](../12-build-cuphead-apk/logs/build.md) | El build incluyó las tareas de manifest del asset pack |
| M-02 | Conversión AAB a APKs locales | Fallida | 0 conjuntos | `build-apks --local-testing --connected-device` | [log bundletool](./logs/bundletool.md) | Falló en la firma del APK generado |
| M-03 | Instalación mediante `install-apks` | N/A | N/A | No existe `.apks` válido | [log bundletool](./logs/bundletool.md) | No se ejecutó una instalación parcial |
| M-04 | Extracción del asset pack en Android | N/A | N/A | La conversión fue interrumpida | N/A | Pendiente de segmentar el asset |
| M-05 | Ejecución de `Cuphead.exe` en Android | N/A | N/A | No hubo instalación | N/A | No inferir compatibilidad |

## Observación y decisión

El AAB se construyó, pero bundletool devolvió `ApkFormatException`/`ZipFormatException` al firmar el asset pack. Los offsets reportados (`CD end: 8589934590` y `EoCD start: 4782574132`) son incompatibles con el paquete ZIP generado para este asset de más de 4 GiB.

Se decide segmentar el stream comprimido en tres asset packs install-time, reconstruyéndolo mediante un `SequenceInputStream` antes de pasarlo al extractor TAR/Zstandard. Esta ejecución no demuestra un fallo de la instalación de Cuphead ni del dispositivo.

## Evidencias

- AAB: `winlator/app/app/build/outputs/bundle/debug/app-debug.aab`.
- Asset original: `winlator/app/cuphead_data/src/main/assets/cuphead.tzst`.
- Log: [salida exacta de bundletool](./logs/bundletool.md).
- Herramienta: `tools/bundletool-all-1.18.3.jar`.
