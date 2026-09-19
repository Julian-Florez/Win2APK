# EXEC-041: Instalación fría de v48 con target API 28 para permitir la ejecución de box64 desde el rootfs; se conserva compileSdk 36 y pageSizeCompat

- **Run de métricas:** `RUN-20260919-009`
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
| Escenario | `legacy-exec-api28-pagesizecompat-v48-pixel-cold-install` | Instalación fría de v48 con target API 28 para permitir la ejecución de box64 desde el rootfs; se conserva compileSdk 36 y pageSizeCompat |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 569.231 s | 672.564 s | 2586 ms | 96219 ms | 50.333 | 2061536.000 | loading | partial |

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

- `pixel-9a`: [captura y CSV](../../metricas/runs/RUN-20260919-009); descripción: A T+60 se observa la pantalla de preparación con el indicador azul y el texto 'Preparing application...'; el proceso Cuphead.exe aparece después y permanece vivo hasta T+300..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-009)
