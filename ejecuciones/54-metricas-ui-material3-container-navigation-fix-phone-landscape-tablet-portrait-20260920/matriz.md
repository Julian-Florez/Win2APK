# EXEC-054: Instalación fría de la corrección de navegación Material 3; comprobar acceso a configuración de Container-1

- **Run de métricas:** `RUN-20260920-005`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** pendiente de clasificación visual
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.ui.preview` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview.apks` | Archivo medido |
| SHA-256 | `7608f43af3517ba19759f7e7895d4191a8bffdf7c55a6712552c717d8d0ba216` | Calculado antes de instalar |
| Escenario | `ui-material3-container-navigation-fix-phone-landscape-tablet-portrait` | Instalación fría de la corrección de navegación Material 3; comprobar acceso a configuración de Container-1 |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 65 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 22.816 s | N/R s | 1419 ms | N/R ms | N/R | 100488.000 | pending | pending_classification |
| redmi-note-8 | success | 22.442 s | N/R s | 1675 ms | N/R ms | N/R | 93850.000 | pending | pending_classification |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-005); descripción: N/R.
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-005); descripción: N/R.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-005)
