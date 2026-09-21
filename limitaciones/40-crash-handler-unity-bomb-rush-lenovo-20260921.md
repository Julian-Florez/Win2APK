# 40. Ventana del Unity Crash Handler de Bomb Rush Cyberfunk en Lenovo TB-J606F

## Descripción

Bomb Rush Cyberfunk muestra una ventana del gestor de errores de Unity sobre la
pantalla de título en la tablet Lenovo TB-J606F. La ventana se mantuvo visible
al menos durante la captura y la comprobación posterior, mientras el proceso
`UnityCrashHandler64.exe` continuó activo durante toda la medición.

## Contexto técnico

- Dispositivo: Lenovo TB-J606F, Android 16, API 36, Adreno 610.
- Orientación y resolución observadas: 2000x1200 en la superficie XServer.
- Paquete: `com.win2apk.bombrushcyberfunk`.
- Versión instalada: `gog-56774571391351451`, versionCode `1`.
- Artefacto observado: `/tmp/win2apk-unified-loading-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks`.
- SHA-256 del artefacto: `ae02fdcbf7324be6e15fd0d63a4487930fd6e043ad4e8cf486d93cad6d7484e9`.
- Perfil del contenedor y configuración gráfica exacta: N/R en esta ejecución.

## Reproducción o evidencia

En `EXEC-066` se lanzó la aplicación preinstalada y se observaron durante 180
segundos los procesos Android, Wine y Windows. El proceso Android, `Bomb Rush
Cyberfunk.exe` y `UnityCrashHandler64.exe` permanecieron activos durante las
162 muestras.

La ventana visible muestra exactamente el título:

```text
Bomb Rush Cyberfunk - Unity 2021.3.27f1_ca3ffb99bcc6
```

También se observa `PRESS ANY KEY` detrás de la ventana y una barra de progreso
del gestor de errores. La captura se revisó visualmente y se clasificó como
`error_screen` con confianza alta:

- [Captura de la ventana del crash handler](../metricas/runs/RUN-20260921-001/screenshots/lenovo-tb-j606f/crash-handler.png)
- [Captura canónica T+60](../metricas/runs/RUN-20260921-001/screenshots/lenovo-tb-j606f/t060.png)
- [Logcat de la ejecución](../metricas/runs/RUN-20260921-001/logs/lenovo-tb-j606f/logcat.txt)
- [Resumen CSV](../metricas/runs/RUN-20260921-001/resumen.csv)

No aparece en el logcat una excepción Android, `SIGSEGV`, `Access Violation` o
un cierre del proceso del juego. Por tanto, esta ejecución reproduce la
ventana del crash handler, pero no demuestra que el proceso Windows haya
terminado ni proporciona todavía el volcado interno de Unity.

Durante la misma ventana temporal Android registró varios eventos del
`lowmemorykiller` con el mensaje exacto `reason: low watermark is breached`,
que terminaron procesos ajenos a Bomb Rush Cyberfunk. Es una señal de presión
de memoria del dispositivo y una hipótesis de contribución, no una causa
confirmada del fallo.

## Impacto

La ejecución queda bloqueada en la pantalla de título con el gestor de errores
superpuesto; no puede considerarse una ejecución funcional estable del juego en
esta tablet bajo estas condiciones.

## Análisis técnico

La evidencia apunta a un fallo o bloqueo dentro de la capa Windows/Unity
ejecutada por Wine. La superficie Android sigue siendo `XServerDisplayActivity`
y UIAutomator no expone el contenido de la ventana porque se renderiza dentro
de esa superficie.

En la ejecución, `Bomb Rush Cyberfunk.exe` alcanzó aproximadamente 560 MiB de
RSS y `UnityCrashHandler64.exe` aproximadamente 108 MiB de RSS en la inspección
final. La memoria disponible del sistema llegó a aproximadamente 1.43 GiB y
se registraron desalojos por presión de memoria. Estas métricas describen la
condición observada, pero no prueban si la causa primaria es memoria, gráficos,
compatibilidad de Unity o el propio contenedor.

## Solución aplicada

N/A. Esta fase fue exclusivamente diagnóstica; no se modificó el código ni la
configuración del contenedor.

## Resultado

Estado: reproducido como ventana persistente del Unity Crash Handler en el
Lenovo TB-J606F. El cierre final del ejecutable Windows y el texto interno del
crash report quedan N/R porque ambos procesos seguían vivos al terminar la
observación de 180 segundos.

## Limitaciones pendientes

- Obtener el `error.log` o volcado generado por Unity desde el prefijo Wine.
- Repetir con una captura de memoria y configuración gráfica controladas.
- Separar la presión de memoria de una incompatibilidad específica de Unity
  2021.3.27f1.
- Confirmar si la barra del crash handler progresa o queda bloqueada en una
  ejecución más larga.

## Referencias

- [Matriz de la ejecución EXEC-066](../ejecuciones/66-metricas-bomb-rush-unity-crash-repro-20260921/matriz.md)
- [Limitación 37: clasificación errónea de ejecución preinstalada](./37-agregador-confunde-ejecucion-preinstalada-con-fallo.md)

## Ejecuciones asociadas

- [EXEC-066](../ejecuciones/66-metricas-bomb-rush-unity-crash-repro-20260921/matriz.md)
