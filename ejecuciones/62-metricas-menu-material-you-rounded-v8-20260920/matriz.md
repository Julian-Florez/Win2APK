# EXEC-062: Verificación visual final del panel runtime Material You en orientación horizontal y vertical

- **Run de métricas:** `RUN-20260920-013`
- **Fecha:** 2026-09-20
- **Tipo:** actualización incremental y medición temporal
- **Resultado general:** aprobado para verificación visual; la instalación fría no se midió en este run
- **Método:** `update`, sin root, con apertura manual del panel mediante Atrás

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.winlator` | `run.csv` |
| Artefacto | `/tmp/win2apk-ui-build-panel-v8/win2apk-ui-preview-material3-preview-runtime.apks` | Archivo medido |
| SHA-256 | `b5f4eaf8ef5b47ac0e42b0aff57e812ada8b9d96f5ccef4e6a9d112f8d1bbaad` | Calculado antes de instalar |
| Escenario | `menu-material-you-rounded-v8` | Verificación visual final del panel runtime Material You en orientación horizontal y vertical |
| Estado esperado | `runtime_menu` | Hipótesis previa |
| Duración | 10 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+1 s | Panel runtime abierto; clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | N/A | N/R s | N/R s | 387 ms | N/R ms | 0.000 | 118193.000 | menu | visual_ok |
| redmi-note-8 | N/A | N/R s | N/R s | 342 ms | N/R ms | 0.000 | 124137.000 | menu | visual_ok |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas. La instalación es `N/A` porque
la compilación v8 se actualizó antes de iniciar este run.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. En ambos dispositivos se observa el panel runtime con las cuatro esquinas
redondeadas y el fondo naranja resuelto desde el tema Material You; el teléfono
queda con opciones desplazables por su menor altura y la tablet muestra las diez
opciones.

## Decisión

Aceptar la configuración como verificación visual del panel en estas dos
orientaciones. Mantener una prueba de instalación fría separada para medir
tiempos de instalación de la misma compilación.

## Evidencias

- `lenovo-tb-j606f`: [panel](../../metricas/runs/RUN-20260920-013/screenshots/lenovo-tb-j606f/panel.png) y [captura canónica](../../metricas/runs/RUN-20260920-013/screenshots/lenovo-tb-j606f/t001.png); descripción: Panel runtime abierto en orientación vertical; fondo opaco naranja de Material You, cuatro esquinas redondeadas y diez opciones visibles hasta Exit.
- `redmi-note-8`: [panel](../../metricas/runs/RUN-20260920-013/screenshots/redmi-note-8/panel.png) y [captura canónica](../../metricas/runs/RUN-20260920-013/screenshots/redmi-note-8/t001.png); descripción: Panel runtime abierto en orientación horizontal; fondo opaco naranja de Material You, cuatro esquinas redondeadas y opciones Keyboard, Input Controls, Toggle Fullscreen, Task Manager, Active Windows, Magnifier y Screen Effect.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-013)
