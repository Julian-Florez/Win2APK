# EXEC-038: Instalación fría de la compilación API 36 con empaquetado PAGE_ALIGNMENT_16K y observación del primer inicio

- **Run de métricas:** `RUN-20260919-006`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** pendiente de clasificación visual
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v46-modern-api36-16k-local-testing.apks` | Archivo medido |
| SHA-256 | `f0529d375c1a1a4b1211586362ea0492a37a954ea0db5f1ec1d092e6bc9bd616` | Calculado antes de instalar |
| Escenario | `modern-api36-16k-pixel-cold-install` | Instalación fría de la compilación API 36 con empaquetado PAGE_ALIGNMENT_16K y observación del primer inicio |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 60 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 644.589 s | N/R s | 955 ms | N/R ms | N/R | 172833.000 | pending | pending_classification |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

Revisar `resumen.csv`, los logs y la clasificación visual antes de aceptar o
descartar una configuración para otra familia de dispositivos.

## Evidencias

- `pixel-9a`: [captura y CSV](../../metricas/runs/RUN-20260919-006); descripción: N/R.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-006)
