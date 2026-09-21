# EXEC-073: Validación del retorno visual del D-pad al soltar en Redmi Note 8

- **Run de métricas:** `RUN-20260921-008`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-gamepad-material3-v5/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `36799329e77be8494711df442e20a000733ad92aaeb2cd788104ba27b6d35901` | Calculado antes de instalar |
| Escenario | `gamepad-material3-dpad-release-v5-redmi` | Validación del retorno visual del D-pad al soltar en Redmi Note 8 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| redmi-note-8 | success | 76.036 s | N/R s | 1643 ms | N/R ms | N/R | 150288.000 | loading | partial |

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

- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260921-008); la captura T+60 es la pantalla de carga negra.
- [D-pad presionado](../../metricas/runs/RUN-20260921-008/screenshots/redmi-note-8/interactive-dpad-up-pressed.png): el segmento activo cambia al color de presión.
- [D-pad liberado](../../metricas/runs/RUN-20260921-008/screenshots/redmi-note-8/interactive-dpad-up-released.png): el segmento vuelve al color normal al recibir `UP`; no queda retenido como switch.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-008)
