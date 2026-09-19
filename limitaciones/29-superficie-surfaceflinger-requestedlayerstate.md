# 29. Superficie SurfaceFlinger envuelta en `RequestedLayerState`

## Descripción

La primera versión de la skill de métricas no pudo obtener FPS ni el primer frame
del Pixel porque Android 17 no devolvió nombres de capa planos en
`dumpsys SurfaceFlinger --list`; devolvió objetos `RequestedLayerState{...}`.

## Contexto técnico

- Aplicación: `com.cuphead`, publicación v45.
- Dispositivo: Pixel 9a, Android 17, ABI arm64-v8a.
- Herramienta: `$win2apk-medir-dispositivos`, primera ejecución automatizada.
- Superficie real observada después del diagnóstico:
  `807ea93 SurfaceView[com.cuphead/com.winlator.XServerDisplayActivity](BLAST)#30397`.

## Reproducción o evidencia

En `EXEC-033`, `monitor_device.py` seleccionaba la línea completa del wrapper y
la pasaba a `dumpsys SurfaceFlinger --latency`. El proceso y la captura T+60 sí
se registraron, pero `fps_presented` y `first_game_frame_observed` quedaron sin
valor. El evento de instrumentación conserva la observación en
[`eventos.csv`](../metricas/runs/RUN-20260919-001/eventos.csv).

## Impacto

El tiempo de instalación no podía terminar en el primer frame verificable y los
FPS del Pixel quedaban `N/R`; la medición de memoria y procesos no quedó afectada.

## Análisis técnico

La capa BLAST utilizable se encontraba dentro del wrapper y debía conservar el
texto anterior a `parentId`, `relativeParentId`, `z` o `!handle`. No se trató de
un crash del juego.

## Solución aplicada

`monitor_device.py` normaliza `RequestedLayerState{...}`, prioriza la capa
`(BLAST)` y exige un timestamp nuevo después de observar `Cuphead.exe` para
registrar `first_game_frame_observed`.

## Resultado

Resuelta experimentalmente en `EXEC-036`: Pixel, Lenovo y Mi A3 produjeron
timestamps de primer frame y `delivery_to_first_frame_seconds`. La corrección
no demuestra compatibilidad con todas las versiones de Android.

## Limitaciones pendientes

La exposición de capas y timestamps puede variar entre fabricantes. GPU y FPS
siguen siendo `N/R` cuando el dispositivo no expone nodos o timestamps legibles.

## Referencias

- [Esquema de métricas](../.codex/skills/win2apk-medir-dispositivos/references/esquema-datos.md)
- [Implementación del monitor](../.codex/skills/win2apk-medir-dispositivos/scripts/monitor_device.py)

## Ejecuciones asociadas

- [EXEC-033](../ejecuciones/33-metricas-titulo-instalacion-fria-5-min-20260919/matriz.md)
- [EXEC-036](../ejecuciones/36-metricas-titulo-instalacion-fria-5-min-20260919/matriz.md)

