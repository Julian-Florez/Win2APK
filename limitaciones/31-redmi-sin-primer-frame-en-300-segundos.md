# 31. Redmi sin primer frame del juego durante la ventana de 300 segundos

## Descripción

Después de una instalación completa exitosa, el Redmi mantuvo la aplicación
principal activa, pero no se observó `Cuphead.exe` ni un primer frame del juego
durante los 300 segundos de monitoreo.

## Contexto técnico

- Publicación: v45, APKS local-testing completo.
- Dispositivo: Redmi Note 8, Android 16, arm64-v8a.
- Instalación válida posterior a los reintentos ADB: 194,668 s.
- Condición: lanzamiento automático y muestreo cada segundo, sin interacción.

## Reproducción o evidencia

`RUN-20260919-004` registró 301 muestras. En todas, `app_alive` fue observable
prácticamente toda la ventana, pero `game_alive_ratio=0.000` y
`delivery_to_first_frame_seconds` quedó vacío. La captura T+60 fue clasificada
como `loading` y muestra literalmente `Preparing application...`.

Evidencias: [resumen.csv](../metricas/runs/RUN-20260919-004/resumen.csv),
[captura T+60](../metricas/runs/RUN-20260919-004/screenshots/redmi-note-8/t060.png)
y [logcat](../metricas/runs/RUN-20260919-004/logs/redmi-note-8/logcat.txt).

## Impacto

El Redmi no alcanzó el estado esperado `title_screen` dentro de la ventana
definida; el tiempo de instalación sí es válido, pero el tiempo a primer frame es
`N/R`.

## Análisis técnico

La pantalla muestra preparación y no una pantalla negra sin interfaz. Por tanto,
la evidencia disponible indica una preparación prolongada o incompleta, pero no
permite afirmar un crash ni atribuir la causa a GPU, almacenamiento o payload sin
una prueba adicional.

## Solución aplicada

No se aplicó una corrección del juego en esta ejecución. Se registró el estado
como limitación del escenario de cinco minutos para evitar convertir una ausencia
de frame en una conclusión causal.

## Resultado

Limitación detectada y pendiente de investigación. La misma publicación sí produjo
primer frame en Pixel, Lenovo y Mi A3 bajo el mismo protocolo, pero eso no prueba
compatibilidad universal.

## Limitaciones pendientes

Repetir el Redmi con una ventana de arranque mayor o con telemetría específica del
movimiento de `STORAGE_FILES`, sin mezclar ese resultado con esta matriz histórica.

## Referencias

- [Clasificación visual](../metricas/runs/RUN-20260919-004/capturas.csv)
- [Muestras temporales](../metricas/runs/RUN-20260919-004/muestras.csv)
- [Taxonomía de pantallas](../.codex/skills/win2apk-medir-dispositivos/references/clasificacion-pantallas.md)

## Ejecuciones asociadas

- [EXEC-036](../ejecuciones/36-metricas-titulo-instalacion-fria-5-min-20260919/matriz.md)

