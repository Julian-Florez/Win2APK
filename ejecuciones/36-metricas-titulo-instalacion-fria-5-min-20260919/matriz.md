# EXEC-036: Instalación fría completa y primer inicio observado durante cinco minutos; orden Pixel, tablet, Redmi y Xiaomi

- **Run de métricas:** `RUN-20260919-004`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v45-full-local-testing.apks` | Archivo medido |
| SHA-256 | `9063bacab88dd543bcee024e50e0b34b2f0dcb8593a0ef1784c3840c5a5e1d28` | Calculado antes de instalar |
| Escenario | `titulo-instalacion-fria-5-min` | Instalación fría completa y primer inicio observado durante cinco minutos; orden Pixel, tablet, Redmi y Xiaomi |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 507.907 s | 706.929 s | 2337 ms | 195807 ms | 36.536 | 204021.000 | loading | partial |
| mi-a3 | success | 184.781 s | 393.489 s | 4434 ms | 206143 ms | 36.532 | 209050.000 | loading | partial |
| pixel-9a | success | 197.329 s | 299.669 s | 1399 ms | 97201 ms | 53.108 | 1256653.000 | loading | partial |
| redmi-note-8 | success | 194.668 s | N/R s | 4438 ms | N/R ms | N/R | 206863.000 | loading | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260919-004); descripción: Se observa una pantalla negra de preparación con un indicador circular azul y el texto "Preparing application..."; no se ve el juego..
- `mi-a3`: [captura y CSV](../../metricas/runs/RUN-20260919-004); descripción: Se observa una pantalla negra de preparación con un pequeño indicador azul y el texto "Preparing application..."; no se ve el juego..
- `pixel-9a`: [captura y CSV](../../metricas/runs/RUN-20260919-004); descripción: Se observa un fondo negro con un indicador circular azul y el texto visible "Preparing application..."; el juego todavía no aparece..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260919-004); descripción: Se observa una pantalla negra de preparación con un indicador circular azul, el texto "Preparing application..." y parte de un control lateral del entorno; no se ve el juego..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-004)
