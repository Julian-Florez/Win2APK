# EXEC-071: Validación visual del gamepad Material 3 v3 en Redmi Note 8

- **Run de métricas:** `RUN-20260921-006`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-gamepad-material3-v3/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fa1d43fbfc0ce3d0537402e8c61b43cfe9a7d4c7bae12fd98d80b8bbd6f348f3` | Calculado antes de instalar |
| Escenario | `gamepad-material3-shapes-v3-redmi` | Validación visual del gamepad Material 3 v3 en Redmi Note 8 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| redmi-note-8 | success | 73.982 s | N/R s | 1670 ms | N/R ms | 0.000 | 131677.000 | loading | partial |

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

- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260921-006); descripción: La captura canónica T+60 muestra la pantalla de carga negra con Cargando; la captura suplementaria posterior muestra el gamepad Material 3 v3..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-006)
