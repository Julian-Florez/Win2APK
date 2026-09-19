# EXEC-043: Instalación fría de v48 en Redmi Note 8; comprobar ejecución de Cuphead y estabilidad de la ruta Adreno

- **Run de métricas:** `RUN-20260919-011`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v48-legacy-exec-local-testing.apks` | Archivo medido |
| SHA-256 | `23a2f8fb802c2435d2fcf1070dd6535484e15cffeb208ce30bff1e266cb41d31` | Calculado antes de instalar |
| Escenario | `legacy-exec-api28-pagesizecompat-v48-redmi-cold-install` | Instalación fría de v48 en Redmi Note 8; comprobar ejecución de Cuphead y estabilidad de la ruta Adreno |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| redmi-note-8 | success | 202.914 s | N/R s | 1999 ms | N/R ms | N/R | 217876.000 | loading | partial |

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

- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260919-011); descripción: La captura T+60 muestra la pantalla de preparación con un indicador azul y el texto Preparing application...; no se observa el juego..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-011)
