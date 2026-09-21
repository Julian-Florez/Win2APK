# EXEC-056: Cold install of the final Material 3 UI after reserving permanent tablet navigation space; observe Containers before opening Container-1 settings

- **Run de métricas:** `RUN-20260920-007`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview-material3-preview.apks` | Archivo medido |
| SHA-256 | `f047819bcab60d63edfe0aa75a0fcbe2cc24d4cad5e6f1c28b21ce83648efb76` | Calculado antes de instalar |
| Escenario | `container-settings-navigation-fix-final` | Cold install of the final Material 3 UI after reserving permanent tablet navigation space; observe Containers before opening Container-1 settings |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 65 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | failed | 12.106 s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |
| redmi-note-8 | failed | 10.577 s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-007); descripción: N/R.
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-007); descripción: N/R.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-007)
