# EXEC-053: Interfaz general Material 3 en las orientaciones complementarias; sin reinstalar

- **Run de métricas:** `RUN-20260920-004`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `preinstalled-no-reinstall`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.ui.preview` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview.apks` | Archivo medido |
| SHA-256 | `6041a788beeea0e6bb7cc51a279690c52919c33bedf2763e7c0f086bf9adc0e8` | Calculado antes de instalar |
| Escenario | `ui-material3-preview-phone-portrait-tablet-landscape` | Interfaz general Material 3 en las orientaciones complementarias; sin reinstalar |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 65 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | N/R | N/R s | N/R s | 370 ms | N/R ms | N/R | 97937.000 | menu | failed_install |
| redmi-note-8 | N/R | N/R s | N/R s | 342 ms | N/R ms | N/R | 92068.000 | menu | failed_install |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-004); descripción: Pantalla general en tablet horizontal con navegación permanente a la izquierda y contenido Containers al lado derecho..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-004); descripción: Pantalla Containers en teléfono vertical con barra superior, Container-1 y acciones táctiles reacomodadas al ancho estrecho..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-004)
