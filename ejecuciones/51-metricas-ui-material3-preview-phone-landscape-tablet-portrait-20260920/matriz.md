# EXEC-051: Instalación fría de la variante general Material 3; Redmi horizontal y Lenovo vertical

- **Run de métricas:** `RUN-20260920-002`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.ui.preview` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview.apks` | Archivo medido |
| SHA-256 | `6041a788beeea0e6bb7cc51a279690c52919c33bedf2763e7c0f086bf9adc0e8` | Calculado antes de instalar |
| Escenario | `ui-material3-preview-phone-landscape-tablet-portrait` | Instalación fría de la variante general Material 3; Redmi horizontal y Lenovo vertical |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 75 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 24.988 s | N/R s | 4903 ms | N/R ms | N/R | 97908.000 | android_dialog | partial |
| redmi-note-8 | success | 23.041 s | N/R s | 4021 ms | N/R ms | N/R | 90676.000 | android_dialog | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-002); descripción: Permiso de almacenamiento del sistema Android en tablet vertical; detrás se distingue la navegación general de Winlator..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-002); descripción: Permiso de almacenamiento del sistema Android cubre la interfaz; detrás se distingue la pantalla Containers..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-002)
