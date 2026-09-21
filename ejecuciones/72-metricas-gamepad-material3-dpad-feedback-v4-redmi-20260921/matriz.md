# EXEC-072: Validación del feedback visual de la cruceta Material 3 v4 en Redmi Note 8

- **Run de métricas:** `RUN-20260921-007`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-gamepad-material3-v4/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `6600bc2f53ea30839b0484b97d90e34b72e5422958149285d2499ea890993a99` | Calculado antes de instalar |
| Escenario | `gamepad-material3-dpad-feedback-v4-redmi` | Validación del feedback visual de la cruceta Material 3 v4 en Redmi Note 8 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| redmi-note-8 | success | 75.698 s | N/R s | 1727 ms | N/R ms | N/R | 145973.000 | loading | partial |

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

- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260921-007); descripción: La captura T+60 corresponde a la pantalla de carga negra; la validación del feedback del D-pad se realiza en una captura interactiva suplementaria..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-007)
