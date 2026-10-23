# 48. El resumidor trataba la fase second-open como instalación fallida

## Descripción

Al resumir RUN-017/EXEC-096, `summarize_run.py` asignó `failed_install` a la fase `second_open_no_reinstall` porque esa fase no tiene una fila `install_apks`. No era un fallo de instalación: la ausencia de instalación es parte del escenario de reapertura.

## Contexto técnico

- Herramienta: `.codex/skills/win2apk-medir-dispositivos/scripts/summarize_run.py`.
- Escenario: segunda apertura de WinTest sin reinstalación en Xiaomi Mi A3, Android 16/API 36.
- Run asociado: `RUN-20261023-017`, ejecución `EXEC-096`.

## Reproducción o evidencia

1. La fase `second-open/run.csv` declara `install_mode=second_open_no_reinstall` y su `instalaciones.csv` contiene solo el encabezado, correctamente.
2. Antes de corregir el resumidor, el campo `install_result` quedó vacío y el resultado fue `failed_install`, aunque hubo 301 muestras y se observó `first_game_frame_observed`.
3. El preflight confirma `am force-stop` exitoso, proceso ausente antes del relanzamiento y paquete todavía instalado.

## Impacto

El resultado confundía una fase que no instala con una instalación fallida y podía contaminar análisis de fallos. En RUN-017, la pantalla negra de T+60 era el resultado visual real y debía expresarse como `failed_visual_state`, no `failed_install`.

## Análisis técnico

La condición del agregador requería `install_result == success` para cualquier modo. No distinguía el flujo `second_open_no_reinstall`, en el que no debe existir un paso de instalación.

## Solución aplicada

`summarize_run.py` ahora asigna `install_result=N/A` a `second_open_no_reinstall` y evalúa muestras, procesos y clasificación visual sin exigir una fila de instalación. Se ejecutó `py_compile`, se resumió y validó la fase second-open, y luego se resumió y validó de nuevo la fase fría para restaurar su fila en el catálogo.

## Resultado

Resuelta experimentalmente para el caso RUN-017: el resumen warm indica `install_result=N/A` y `result=failed_visual_state`, acorde con la captura negra y los procesos activos. Las fases fría y second-open pasaron `validate_dataset.py`.

## Limitaciones pendientes

- No se han ejecutado pruebas unitarias independientes del agregador; la verificación actual cubre la ruta real de RUN-017.
- La corrección no cambia los datos medidos ni reclasifica ejecuciones históricas.

## Referencias

- [Código del resumidor](../.codex/skills/win2apk-medir-dispositivos/scripts/summarize_run.py)
- [Resumen second-open](../metricas/runs/RUN-20261023-017/second-open/resumen.csv)
- [Preflight second-open](../metricas/runs/RUN-20261023-017/logs/mi-a3/second-open-preflight.txt)
- [Matriz EXEC-096](../ejecuciones/96-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md)

## Ejecuciones asociadas

- [EXEC-096](../ejecuciones/96-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md) / [RUN-20261023-017](../metricas/runs/RUN-20261023-017/)

