# 43. Pack local-testing ausente al abrir el prototipo preinstalado en Lenovo

## Descripción

Durante la verificación previa a la sustentación, la instalación existente de
Bomb Rush Cyberfunk en la Lenovo TB-J606F abrió la pantalla de carga de
Winlator Core, pero no pudo preparar el contenedor ni el acceso directo. El
diálogo visible informó: `Unable to create the configured container or shortcut.`

## Contexto técnico

- Ejecución: `EXEC-074` / `RUN-20260922-001`.
- Fecha: 2026-09-22.
- Método: observación de una instalación preexistente, sin reinstalar ni
  eliminar datos.
- Paquete: `com.win2apk.bombrushcyberfunk`.
- Dispositivo: Lenovo TB-J606F, Android 11, API 30, ABI `arm64-v8a`.
- Ventana observada: 120 s.
- Artefacto de referencia: copia del APK base instalado, con SHA-256
  `816cd604c09984452fb643827d125bc563550a578b40c9a7b4a749ca7ee23282`.

## Reproducción o evidencia

La captura T+60 conserva el diálogo de error. El `logcat` registra exactamente:

```text
com.google.android.play.core.common.LocalTestingException: No APKs available for pack 'win2apk_payload_002'.
```

La evidencia está en la [captura T+60](../metricas/runs/RUN-20260922-001/screenshots/lenovo-tb-j606f/t060.png),
el [logcat](../metricas/runs/RUN-20260922-001/logs/lenovo-tb-j606f/logcat.txt)
y el [video de 45 segundos](../metricas/runs/RUN-20260922-001/screenshots/lenovo-tb-j606f/demo-45s.mp4).

## Impacto

Esta instalación de la Lenovo no es una ruta segura para la demostración en
vivo del 29 de septiembre. El resultado no permite afirmar que el juego ni los
controles táctiles funcionen en el estado observado.

## Análisis técnico

La excepción localiza el fallo en la obtención del pack
`win2apk_payload_002` mediante el proveedor de pruebas locales de Play Core.
El registro no demuestra por sí solo por qué el estado instalado conservó una
referencia al pack sin tener su APK disponible. Distinguir entre datos
residuales, una instalación incompleta o una incompatibilidad de la variante
requiere una instalación fría controlada.

## Solución aplicada

No se modificó ni reinstaló la aplicación para conservar el estado observado.
Se descartó esta Lenovo como dispositivo principal de la demo y se verificó el
mismo paquete preinstalado en Redmi Note 8 mediante `EXEC-075`.

## Resultado

Estado: reproducida en la instalación observada de Lenovo; causa del estado
inconsistente pendiente de aislamiento. En Redmi Note 8, la observación
separada alcanzó la pantalla de título y mantuvo los procesos visibles durante
120 s. Ese resultado no corrige ni generaliza el de Lenovo.

## Limitaciones pendientes

- Repetir en Lenovo con una instalación fría que incluya todos los splits y
  packs de `local_testing`.
- Comparar el estado de la configuración y los datos de Play Core antes y
  después de la instalación fría.
- No usar la instalación actual de Lenovo como respaldo de la demostración.

## Referencias

- [Matriz EXEC-074](../ejecuciones/74-metricas-sustentacion-demo-preinstalada-lenovo-20260922/matriz.md)
- [Run RUN-20260922-001](../metricas/runs/RUN-20260922-001/)
- [Observación de control en Redmi, EXEC-075](../ejecuciones/75-metricas-sustentacion-demo-preinstalada-redmi-20260922/matriz.md)

## Ejecuciones asociadas

- [EXEC-074](../ejecuciones/74-metricas-sustentacion-demo-preinstalada-lenovo-20260922/matriz.md)
- [EXEC-075](../ejecuciones/75-metricas-sustentacion-demo-preinstalada-redmi-20260922/matriz.md)
