# 42. Mi A3 sin superficie visible durante la prueba del gamepad Material 3

## Descripción

Durante la instalación y arranque de la variante con gamepad Material You 3,
el Xiaomi Mi A3 mantuvo la aplicación observable, pero la captura T+60 fue
completamente negra y no permitió evaluar el renderer táctil.

## Contexto técnico

- Ejecución: `EXEC-069` / `RUN-20260921-004`.
- Artefacto: `bomb-rush-cyberfunk-gog-56774571391351451.apks`.
- SHA-256: `de94b1c8e0865400203261c1c545cf49cbd628263430c06983e94986dd7ab433`.
- Dispositivo: Xiaomi Mi A3, Android 16, API 36, ABI arm64-v8a.
- Ventana observada: 90 s; app visible desde 1429 ms; proceso del juego: N/R.

## Reproducción o evidencia

La clasificación de la captura canónica es `black_screen`. La evidencia está
en [T+60 del Mi A3](../metricas/runs/RUN-20260921-004/screenshots/mi-a3/t060.png),
el [resumen del run](../metricas/runs/RUN-20260921-004/resumen.csv) y el
[logcat](../metricas/runs/RUN-20260921-004/logs/mi-a3/logcat.txt).

## Impacto

No se puede confirmar en este dispositivo la apariencia ni la visibilidad de
los controles Material 3 a partir de la captura canónica.

## Análisis técnico

La observación confirma una pantalla negra, pero no confirma si la causa está
en el arranque de Bomb Rush Cyberfunk, la superficie gráfica o el tiempo de
carga. No se atribuye causalidad al cambio del renderer.

## Solución aplicada

Ninguna para este dispositivo en esta ejecución. Se conservaron la captura,
las muestras y el log para diagnóstico posterior.

## Resultado

Estado: detectada. Redmi Note 8 y Lenovo TB-J606F sí permitieron observar el
gamepad Material 3 en capturas suplementarias del mismo artefacto.

## Limitaciones pendientes

- Repetir el arranque del Mi A3 con una ventana mayor y logcat filtrado del
  proceso del juego.
- No inferir compatibilidad visual del Mi A3 a partir de Redmi o Lenovo.

## Referencias

- [Matriz EXEC-069](../ejecuciones/69-metricas-gamepad-material3-install-20260921/matriz.md)
- [Resumen RUN-20260921-004](../metricas/runs/RUN-20260921-004/resumen.csv)

## Ejecuciones asociadas

- [EXEC-069](../ejecuciones/69-metricas-gamepad-material3-install-20260921/matriz.md)
