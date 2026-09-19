# Target API 28 para la ejecución del entorno de compatibilidad

- **Fecha:** 2026-09-19
- **Estado:** adoptada experimentalmente en v48
- **Propósito:** restaurar el arranque de Box64/Wine después de la regresión de
  la compilación v47.

## Problema

La decisión documentada en [09](./09-decision-compatibilidad-api36-y-paginas-16kb.md)
subió el target de la aplicación a API 36 para atender la advertencia de
compatibilidad moderna. En el primer inicio de v47, Android impidió que Box64
ejecutara desde el rootfs almacenado en `app_data_file`; el Pixel quedó en
`Preparing application...` y no llegó a crear `Cuphead.exe` dentro de la
ventana de prueba.

## Decisión

La v48 conserva `compileSdk=36`, NDK 30 y las bibliotecas nativas completas,
pero fija `targetSdkVersion=28`. Esta decisión es específica de la arquitectura
actual: Winlator ejecuta binarios extraídos desde el almacenamiento privado y
necesita las reglas de ejecución compatibles con ese diseño.

## Justificación

- En v47, el log registró `avc: denied { execute_no_trans }` para
  `/data/data/com.cuphead/files/rootfs/usr/local/bin/box64`.
- En v48, el log del Pixel mostró la ruta de ejecución y `Cuphead.exe` se
  mantuvo vivo hasta el final de los 300 segundos.
- El mismo artefacto v48 se instaló en los otros tres dispositivos y el usuario
  confirmó que el juego terminó ejecutándose en todos.
- El cambio evita retirar FluidSynth, PulseAudio, MIDI o bibliotecas gráficas
  funcionales; por tanto, la estabilidad del audio y de otros procesos no se
  obtiene mediante exclusiones silenciosas.

## Alcance y trade-off

Esta es una corrección de ejecución, no una solución definitiva de publicación
moderna. Android puede mostrar advertencias por target antiguo y por binarios
precompilados de páginas de 16 KB. `pageSizeCompat` sigue declarado como modo
de compatibilidad, pero no sustituye una recompilación completa ni la
reubicación de los ejecutables del rootfs.

La validación actual demuestra el resultado para Cuphead, v48 y los cuatro
dispositivos probados; no demuestra compatibilidad universal con otras
aplicaciones Windows ni con todos los dispositivos Android.

## Evidencia

- [Limitación 33: target API 36 bloquea Box64](../limitaciones/33-target-api36-bloquea-ejecucion-box64-desde-rootfs.md)
- [EXEC-041: Pixel 9a, v48](../ejecuciones/41-metricas-legacy-exec-api28-pagesizecompat-v48-pixel-cold-install-20260919/matriz.md)
- [EXEC-042: Lenovo TB-J606F, v48](../ejecuciones/42-metricas-legacy-exec-api28-pagesizecompat-v48-lenovo-cold-install-20260919/matriz.md)
- [EXEC-043: Redmi Note 8, v48](../ejecuciones/43-metricas-legacy-exec-api28-pagesizecompat-v48-redmi-cold-install-20260919/matriz.md)
- [EXEC-044: Mi A3, v48](../ejecuciones/44-metricas-legacy-exec-api28-pagesizecompat-v48-mi-a3-cold-install-20260919/matriz.md)
- [EXEC-045: verificación posterior de `Cuphead.exe` en los cuatro dispositivos](../ejecuciones/45-verificacion-posterior-procesos-cuphead-v48-20260919/matriz.md)
- [AOSP: reglas `untrusted_app`](https://android.googlesource.com/platform/system/sepolicy/%2B/5e5228137248e04441b74e98e33a1c23f524c12e/private/untrusted_app_25.te)

## Trabajo pendiente

Diseñar y probar una ruta de ejecución moderna que no dependa de ejecutar
Box64/Wine desde `app_data_file`; hasta entonces, v48 es la variante estable
experimental para este proyecto.
