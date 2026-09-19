# EXEC-042: Instalación fría de v48 con target API 28 compatible con ejecución desde rootfs; comprobar creación del entorno, arranque de Cuphead y estabilidad

- **Run de métricas:** `RUN-20260919-010`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v48-legacy-exec-local-testing.apks` | Archivo medido |
| SHA-256 | `23a2f8fb802c2435d2fcf1070dd6535484e15cffeb208ce30bff1e266cb41d31` | Calculado antes de instalar |
| Escenario | `legacy-exec-api28-pagesizecompat-v48-lenovo-cold-install` | Instalación fría de v48 con target API 28 compatible con ejecución desde rootfs; comprobar creación del entorno, arranque de Cuphead y estabilidad |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 209.096 s | 479.049 s | 2040 ms | 266370 ms | 11.365 | 203151.000 | black_screen | failed_visual_state |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260919-010); descripción: La captura T+60 es esencialmente negra y no contiene texto ni controles visibles; el monitoreo posterior sí observó Cuphead.exe al final de la ventana..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-010)
