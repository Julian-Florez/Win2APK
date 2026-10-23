# EXEC-094: Bomb Rush Cyberfunk ensayo 4 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-015`
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
| Escenario | `bomb-rush-cold-second-open-trial-04` | Bomb Rush Cyberfunk ensayo 4 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 81.492 s | 172.868 s | 2915 ms | 77406 ms | 44.104 | 186892.000 | compatibility_ui | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-015); descripción: Interfaz Winlator con cuadro Starting up... e indicador circular; no se observa aún contenido del juego..

## Segunda apertura (sin reinstalación)

Fase de 300.635 s con 262 muestras. App y Bomb Rush Cyberfunk.exe activos al cierre; primer proceso a 1.833 s, juego a 10.845 s y primer frame a 15.226 s. FPS medio registrado: 12.104. La captura T+60 muestra el logotipo de Bomb Rush sobre arte gráfico verde/blanco/negro; `title_screen`, revisión confirmada y resultado `approved_experimental` en esta reapertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-015/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `5a9302a0eda04b646e386ed7609947c392202ff0d6be7582d5c641e2755b3b1c`. Validación warm OK (262 muestras). En frío, T+60 quedó en interfaz Winlator `Starting up...`; las dos fases se mantienen separadas.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-015)
