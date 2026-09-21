# EXEC-064: Verificación del panel runtime en coreMode sin la opción Exit con Bomb Rush Cyberfunk

- **Run de métricas:** `RUN-20260920-015`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-bomb-rush-core-menu-v2/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `ca4fb1ce06414934db2f51403a5764599545afb90aa566611caf731949b58863` | Calculado antes de instalar |
| Escenario | `bomb-rush-core-runtime-menu-no-exit` | Verificación del panel runtime en coreMode sin la opción Exit con Bomb Rush Cyberfunk |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 15 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+5 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 76.334 s | N/R s | 444 ms | N/R ms | 56.656 | 125904.000 | menu | approved_experimental |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-015); descripción: Panel lateral runtime abierto en coreMode con Bomb Rush Cyberfunk; la lista termina en Touchpad Help y no contiene Exit..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-015)
