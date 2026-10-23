# EXEC-091: Bomb Rush Cyberfunk ensayo 1 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-012`
- **Fecha:** 2026-10-23
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-01` | Bomb Rush Cyberfunk ensayo 1 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 90.079 s | 179.618 s | 3229 ms | 84220 ms | 42.363 | 230824.000 | compatibility_ui | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-012); descripción: Interfaz de Winlator preparando la aplicación, con indicador giratorio; no se observa aún la pantalla del juego..

## Segunda apertura (sin reinstalación)

Fase completa de 300.785 s y 251 muestras. App y proceso del juego activos al cierre; primer proceso a 1.817 s, juego a 14.475 s y primer frame a 15.574 s. FPS medio: 47.424. La captura T+60 muestra la pantalla de título de Bomb Rush Cyberfunk, con el logotipo sobre arte gráfico verde y negro. Clasificación `title_screen`, revisión confirmada; resultado `approved_experimental` para esta apertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-012/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `5a9302a0eda04b646e386ed7609947c392202ff0d6be7582d5c641e2755b3b1c`. CSV y logs en [second-open](../../metricas/runs/RUN-20261023-012/second-open/); validación OK, 251 muestras. La fase fría quedó en interfaz de Winlator “Preparing application...” a T+60 (parcial); la reapertura alcanzó la pantalla de título. Las fases se reportan separadas.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-012)
