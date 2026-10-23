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

### Repetición con observación de 300 s

En `RUN-20261023-022` / `EXEC-101`, la instalación fría desde bundletool finalizó
en 190.300 s. `Cuphead.exe` apareció 165.124 s después de comenzar la medición
posterior a la instalación y el primer frame se registró a 167.505 s de esa
medición. El campo `delivery_to_first_frame_seconds`, medido desde el inicio de
`bundletool install-apks`, fue 358.005 s. Por tanto, en este ensayo el primer
frame excedió cinco minutos de extremo a extremo, aunque apareció dentro de la
ventana de observación de 300 s iniciada tras instalar.

La captura T+60 de la fase fría seguía en `loading`; la segunda apertura sin
reinstalar llegó a `title_screen` y registró su primer frame a 12.483 s. Las dos
fases se conservaron por separado y sus datasets pasaron validación. Esta
repetición cuantifica un arranque tardío; no modifica retrospectivamente
`EXEC-079`.

## Impacto

El usuario puede interpretar la pantalla `Cargando` como un bloqueo o fallo si
espera solo 180 s. En la repetición actual, el primer frame llegó a 358.005 s
desde el inicio de la instalación, por encima de un objetivo extremo a extremo
de 300 s. La ventana de monitor de 300 s posterior a la instalación no equivale
a un timeout total de cinco minutos.

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

Limitación reproducida: `EXEC-079` no observó el proceso en 180 s; `EXEC-101`
midió el primer frame a 358.005 s desde el inicio de la instalación y dejó la
captura T+60 en `loading`. La segunda apertura sí llegó a `title_screen` dentro
de la ventana. Estas observaciones corresponden solo al Mi A3, artefacto y
condiciones registrados.

## Limitaciones pendientes

Determinar si se necesita una captura adicional posterior a la aparición del
juego para comparar estados de pantalla, sin reemplazar las capturas canónicas
T+60 ni las matrices históricas.

## Referencias

- [Matriz EXEC-079](../ejecuciones/79-metricas-cuphead-installacion-dos-dispositivos-20260930/matriz.md)
- [Matriz EXEC-101](../ejecuciones/101-metricas-cuphead-cold-second-open-trial-01-20261023/matriz.md)
- [RUN-20261023-022, fase fría y segunda apertura](../metricas/runs/RUN-20261023-022/)
- [Resumen de métricas](../metricas/runs/RUN-20260930-001/resumen.csv)
- [Log de instalación Mi A3](../metricas/runs/RUN-20260930-001/logs/mi-a3-install.log)
- [Taxonomía de pantallas](../.codex/skills/win2apk-medir-dispositivos/references/clasificacion-pantallas.md)

## Ejecuciones asociadas

- [EXEC-079](../ejecuciones/79-metricas-cuphead-installacion-dos-dispositivos-20260930/matriz.md)
