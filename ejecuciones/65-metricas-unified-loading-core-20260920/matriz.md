# EXEC-065: Verificación de una única pantalla Material 3 de carga para arranque core y preloader runtime

- **Run de métricas:** `RUN-20260920-016`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-unified-loading-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `ae02fdcbf7324be6e15fd0d63a4487930fd6e043ad4e8cf486d93cad6d7484e9` | Calculado antes de instalar |
| Escenario | `unified-loading-core` | Verificación de una única pantalla Material 3 de carga para arranque core y preloader runtime |
| Estado esperado | `loading` | Hipótesis previa |
| Duración | 15 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+1 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 78.093 s | N/R s | 1385 ms | N/R ms | N/R | 196112.000 | loading | approved_experimental |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-016); descripción: Estado inicial de carga del APK core; la fase posterior de preparación usa la misma tarjeta Material 3 del preloader runtime..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-016)
