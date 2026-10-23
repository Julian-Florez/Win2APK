# EXEC-095: Bomb Rush Cyberfunk ensayo 5 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-016`
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
| Escenario | `bomb-rush-cold-second-open-trial-05` | Bomb Rush Cyberfunk ensayo 5 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 80.496 s | 175.514 s | 2743 ms | 76077 ms | 44.056 | 182020.000 | compatibility_ui | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-016); descripción: Interfaz de Winlator con cuadro Starting up... e indicador circular sobre fondo oscuro; no aparece contenido del juego en T+60..

## Segunda apertura (sin reinstalación)

Fase completa: 255 muestras, evento `monitor_finished` a 301.143 s. App y Bomb Rush Cyberfunk.exe activos al cierre; primer proceso a 1.824 s, proceso del juego a 10.764 s y primer frame a 14.997 s. FPS medio: 48.469. Captura T+60: logotipo de Bomb Rush Cyberfunk sobre arte gráfico verde/blanco/negro; clase `title_screen`, revisión confirmada, resultado `approved_experimental`.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-016/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `5a9302a0eda04b646e386ed7609947c392202ff0d6be7582d5c641e2755b3b1c`. Validación warm OK con 255 muestras. La fase fría quedó en interfaz Winlator `Starting up...` a T+60 (parcial); no se mezclan las fases.

Con esta pareja queda completado **Bomb Rush Cyberfunk 5/5 en Lenovo TB-J606F**. En conjunto, las tres aplicaciones completan el objetivo de cinco parejas válidas por aplicación en esta tablet; RUN-001 de WinTest continúa excluido como inválido y preservado.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-016)
