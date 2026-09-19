# Compatibilidad de API moderna y páginas de 16 KB

- **Fecha:** 2026-09-19
- **Estado:** decisión histórica para v47; supersedida experimentalmente por v48 para recuperar la ejecución de Box64
- **Propósito:** evitar que la instalación de Win2APK se presente como una aplicación antigua y ocultar el diálogo de compatibilidad de páginas de memoria sin retirar bibliotecas funcionales.

## Problema

La ejecución [EXEC-038](../ejecuciones/38-metricas-modern-api36-16k-pixel-cold-install-20260919/matriz.md) instaló una compilación con `targetSdkVersion=36` y configuración de bundle alineada a 16 KB, pero Android mostró `PageSizeMismatchDialog` al iniciar. La causa operativa observada son bibliotecas nativas precompiladas que permanecen con segmentos ELF heredados; la alineación del contenedor AAB/APKS, por sí sola, no garantiza que cada ELF sea compatible.

## Decisión

La publicación v47 adoptó estas medidas:

1. `compileSdk=36` y `targetSdkVersion=36`.
2. NDK 30 y enlaces de 16 KB para las bibliotecas nativas compiladas por Win2APK.
3. `android:pageSizeCompat="enabled"` en el manifiesto para que Android use el modo de compatibilidad y no muestre el diálogo al iniciar.
4. Conservación de la pila precompilada FluidSynth/PulseAudio/MIDI y de las capas Vulkan; no se eliminan `.so` para silenciar el aviso.

La medida 3 es una mitigación de presentación y compatibilidad, no una afirmación de que todos los binarios ya estén recompilados para 16 KB.

## Evidencia

- En [RUN-20260919-006](../metricas/runs/RUN-20260919-006), el log registró literalmente `AppWarnings: Showing PageSizeMismatchDialog for package com.cuphead`.
- La captura T+60 de esa ejecución mostró el diálogo de compatibilidad y enumeró bibliotecas heredadas como `libgmodule-2.0.so`, `libpcre.so`, `libvorbis.so`, `libhook_impl.so`, `libmain_hook.so`, `libfile_redirect_hook.so`, `libfluidsynth.so`, `libogg.so` y componentes PulseAudio.
- El APK v47 compilado contiene 37 entradas nativas, incluidas las bibliotecas opcionales; no se hizo una exclusión funcional.
- La auditoría del manifiesto fusionado del AAB v47 verificó `targetSdk=36` y `android:pageSizeCompat="32"`, representación compilada de `enabled`.

## Alcance y riesgos

El cambio está dirigido a Android 16/17 y a dispositivos con páginas de 16 KB. No cambia bibliotecas del sistema ni debe afectar dispositivos con páginas de 4 KB. La compatibilidad puede tener un coste de rendimiento y no sustituye la recompilación completa de todos los precompilados. Si una versión futura de Android fuerza la incompatibilidad de forma fatal, ocultar el diálogo no será suficiente.

El aviso de Play Protect asociado a una instalación lateral o a una firma de depuración es independiente de `targetSdk` y de `pageSizeCompat`; esta decisión no promete suprimirlo.

## Resultado y pendientes

El build APK y el AAB v47 terminaron correctamente, pero la instalación fría
en el Pixel reprodujo una regresión de ejecución de Box64 con `targetSdk=36`.
La corrección adoptada está documentada en
[10. Target API 28 para la ejecución](./10-decision-target-api28-para-winlator-exec.md):
v48 conserva `compileSdk=36` y `pageSizeCompat`, pero vuelve a
`targetSdkVersion=28`. Por ello, v47 ya no es la variante operativa aunque
conserva valor como experimento histórico.

## Relaciones

- [Limitación 32: advertencia de páginas 16 KB](../limitaciones/32-advertencia-paginas-16kb-precompilados.md)
- [EXEC-038: detección en Pixel](../ejecuciones/38-metricas-modern-api36-16k-pixel-cold-install-20260919/matriz.md)
- [RUN-20260919-006](../metricas/runs/RUN-20260919-006)
- [Limitación 33: bloqueo de Box64 con target API 36](../limitaciones/33-target-api36-bloquea-ejecucion-box64-desde-rootfs.md)
- [EXEC-039: regresión de ejecución en Pixel con v47](../ejecuciones/39-metricas-modern-api36-pagesizecompat-v47-pixel-cold-install-20260919/matriz.md)
- [EXEC-041: recuperación experimental con v48](../ejecuciones/41-metricas-legacy-exec-api28-pagesizecompat-v48-pixel-cold-install-20260919/matriz.md)
- [Documentación oficial de tamaños de página de Android](https://developer.android.com/guide/practices/page-sizes)
