# EXEC-033: Instalación fría completa y primer inicio observado durante cinco minutos

- **Run de métricas:** `RUN-20260919-001`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v45-full-local-testing.apks` | Archivo medido |
| SHA-256 | `9063bacab88dd543bcee024e50e0b34b2f0dcb8593a0ef1784c3840c5a5e1d28` | Calculado antes de instalar |
| Escenario | `titulo-instalacion-fria-5-min` | Instalación fría completa y primer inicio observado durante cinco minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | N/R | N/R s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |
| mi-a3 | N/R | N/R s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |
| pixel-9a | success | 192.078 s | N/R s | 2449 ms | 101513 ms | N/R | 1263380.000 | loading | partial |
| redmi-note-8 | N/R | N/R s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260919-001); descripción: N/R.
- `mi-a3`: [captura y CSV](../../metricas/runs/RUN-20260919-001); descripción: N/R.
- `pixel-9a`: [captura y CSV](../../metricas/runs/RUN-20260919-001); descripción: Pantalla oscura de preparación del entorno con un indicador circular azul; todavía no se observa el juego..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260919-001); descripción: N/R.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-001)
