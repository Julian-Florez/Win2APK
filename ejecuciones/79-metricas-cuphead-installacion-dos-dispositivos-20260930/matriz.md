# EXEC-079: Instalación de Cuphead en Redmi Note 8 y Xiaomi Mi A3, seguida de primer arranque y observación

- **Run de métricas:** `RUN-20260930-001`
- **Fecha:** 2026-09-30
- **Tipo:** automatizada, instalación inicial sin desinstalación y medición temporal
- **Resultado general:** instalación completada en ambos; el primer frame no se observó dentro de la ventana de 180 s
- **Método:** `cli-bundletool-install`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `/tmp/win2apk-cuphead-dist/cuphead-11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core.apks` | Archivo medido |
| SHA-256 | `b7ce931e9045fad2b8ddd7ad00589bf83e99354eea5bac38c57cf7af9bf165ce` | Calculado antes de instalar |
| Escenario | `cuphead-installacion-dos-dispositivos` | Instalación de Cuphead en Redmi Note 8 y Xiaomi Mi A3, seguida de primer arranque y observación |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 180 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 216.000 s | N/R s | 1655 ms | N/R ms | N/R | 169282.000 | loading | partial |
| redmi-note-8 | success | 228.000 s | N/R s | 1722 ms | N/R ms | N/R | 138621.000 | black_screen | failed_visual_state |

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

- `mi-a3`: [captura y CSV](../../metricas/runs/RUN-20260930-001); descripción: La captura T+60 muestra una pantalla mayormente negra con el texto visible Cargando y un indicador de progreso; la barra de estado y navegación de Android siguen visibles.
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260930-001); descripción: La captura T+60 muestra una pantalla completamente negra, sin texto ni controles visibles.
- Observación posterior separada de la ventana medida: en Mi A3 se observaron `com.cuphead`, `start.exe`, `wineserver` y `Cuphead.exe`; esto no permite calcular retrospectivamente el tiempo a primer frame de este run.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260930-001)
