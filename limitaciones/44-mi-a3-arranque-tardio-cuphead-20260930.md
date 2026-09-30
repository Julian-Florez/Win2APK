# 44. Mi A3 supera la ventana de observación antes de iniciar Cuphead

## Descripción

En una instalación inicial de Cuphead, el Mi A3 completó la instalación, pero no
mostró el proceso del juego dentro de la ventana automatizada de 180 s. Después
de finalizar esa ventana se observó el arranque de `Cuphead.exe`.

## Contexto técnico

- Dispositivo: Xiaomi Mi A3, Android 16/API 36, arm64-v8a.
- GPU observada: Adreno (TM) 610.
- Artefacto: APKS de Cuphead, SHA-256
  `b7ce931e9045fad2b8ddd7ad00589bf83e99354eea5bac38c57cf7af9bf165ce`.
- Instalación: `success`, 216,000 s, sin desinstalar ni borrar datos previamente.
- Ventana de observación: 180 s, muestreo nominal de 1 s, captura T+60.

## Reproducción o evidencia

Durante la ejecución `EXEC-079`, `com.cuphead` apareció a los 1655 ms, pero no
se observó `Cuphead.exe` durante la ventana medida. La captura T+60 mostró
`Cargando` con un indicador de progreso; `delivery_to_first_frame_seconds` quedó
`N/R` porque no se observó un primer frame en ese intervalo.

Como observación posterior, fuera de la ventana de la ejecución, el logcat mostró
la confirmación del movimiento de 815 archivos (`5847372363` bytes), la limpieza
de los packs locales y el inicio de `XServerDisplayActivity`. Después se
observaron `winhandler.exe` y `Cuphead.exe`. Esta observación confirma un arranque
posterior, pero no permite asignar un tiempo a primer frame a `EXEC-079`.

## Impacto

El usuario puede interpretar la pantalla `Cargando` como un bloqueo o fallo si
espera solo 180 s. La instalación sí finaliza, pero el tiempo de disponibilidad
del juego no queda acotado por la ventana usada en esta ejecución.

## Análisis técnico

La evidencia apunta a una transición tardía entre la preparación de los archivos
directos y el arranque de Winlator. No demuestra un fallo permanente de GPU ni de
la instalación. El aviso de bundletool `run-as: package not debuggable:
com.cuphead` apareció durante la limpieza opcional de `splitcompat`; la CLI
reportó la instalación como correcta y el arranque posterior observó los procesos
del juego.

## Solución aplicada

No se modificó la configuración del juego ni se alteró la medición. Se conservó
el resultado tal como ocurrió y se registró el arranque posterior como evidencia
separada.

## Resultado

Limitación reproducida: el primer arranque del Mi A3 puede superar 180 s con este
artefacto y estas condiciones. El juego llegó a iniciar posteriormente, pero no
se dispone de un primer frame cronometrado en `EXEC-079`.

## Limitaciones pendientes

Repetir con una ventana superior a 180 s y capturas adicionales después de que
aparezca `Cuphead.exe`, sin reemplazar la matriz histórica de esta ejecución.

## Referencias

- [Matriz EXEC-079](../ejecuciones/79-metricas-cuphead-installacion-dos-dispositivos-20260930/matriz.md)
- [Resumen de métricas](../metricas/runs/RUN-20260930-001/resumen.csv)
- [Log de instalación Mi A3](../metricas/runs/RUN-20260930-001/logs/mi-a3-install.log)
- [Taxonomía de pantallas](../.codex/skills/win2apk-medir-dispositivos/references/clasificacion-pantallas.md)

## Ejecuciones asociadas

- [EXEC-079](../ejecuciones/79-metricas-cuphead-installacion-dos-dispositivos-20260930/matriz.md)
