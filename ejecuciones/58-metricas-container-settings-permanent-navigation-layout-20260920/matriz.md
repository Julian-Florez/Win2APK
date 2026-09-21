# EXEC-058: Cold install of side-by-side tablet navigation layout; observe Containers before opening Container-1 settings

- **Run de métricas:** `RUN-20260920-009`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.ui.preview` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview-material3-preview.apks` | Archivo medido |
| SHA-256 | `1550d57b3aae56751ff94ed2a2035d967367d8a9de1fa9983af23b7320018182` | Calculado antes de instalar |
| Escenario | `container-settings-permanent-navigation-layout` | Cold install of side-by-side tablet navigation layout; observe Containers before opening Container-1 settings |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 65 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 23.215 s | N/R s | 4964 ms | N/R ms | N/R | 72487.000 | android_dialog | partial |
| redmi-note-8 | success | 23.102 s | N/R s | 1558 ms | N/R ms | N/R | 75386.000 | android_dialog | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-009); descripción: Android storage permission dialog is visible over the side-by-side permanent navigation and Containers screen in portrait..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-009); descripción: Android storage permission dialog is visible over the Material 3 Containers screen in landscape..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-009)
