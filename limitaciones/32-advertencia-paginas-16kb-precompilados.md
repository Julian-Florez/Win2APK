# 32. Advertencia de páginas 16 KB por bibliotecas nativas precompiladas

## Descripción

Android mostró el diálogo de compatibilidad de páginas de memoria al iniciar `com.cuphead` en el Pixel 9a. La configuración del contenedor AAB/APKS estaba declarada con alineación `PAGE_ALIGNMENT_16K`, pero la aplicación todavía incluía bibliotecas nativas precompiladas con el formato heredado que Android inspeccionó.

## Contexto técnico

- Publicación observada: v46, `targetSdk=36`.
- Publicación de mitigación construida: v47, `targetSdk=36`, `compileSdk=36`, NDK 30.
- Dispositivo: Pixel 9a, API 37, `arm64-v8a`, páginas máximas declaradas de 16 KB.
- Artefacto observado: `RUN-20260919-006`; instalación fría por bundletool sobre ADB inalámbrico.
- Tiempo de instalación observado: `644.589 s`.

## Reproducción o evidencia

El logcat registró exactamente:

```text
AppWarnings: Showing PageSizeMismatchDialog for package com.cuphead
```

La captura [T+60](../metricas/runs/RUN-20260919-006/screenshots/pixel-9a/t060.png) mostró `Compatibilidad de apps para Android` y botones `Aceptar` y `No volver a mostrar`. Entre las bibliotecas visibles aparecieron `libgmodule-2.0.so`, `libpcre.so`, `libpcreposix.so`, `libvorbis.so`, `libhook_impl.so`, `libmain_hook.so`, `libfile_redirect_hook.so`, `libfluidsynth.so`, `libogg.so` y componentes PulseAudio.

La evidencia de la ejecución no demuestra un cierre del proceso ni que el diálogo sea la causa del comportamiento gráfico; solo demuestra la advertencia y la presencia de binarios inspeccionados.

## Impacto

El primer inicio queda interrumpido por un diálogo del sistema en dispositivos que activan esta comprobación. La experiencia se percibe como un error de compatibilidad, aunque el juego puede continuar después de aceptarlo.

## Análisis técnico

La hipótesis confirmada para la mitigación es que la alineación del ZIP/AAB no corrige automáticamente los segmentos ELF de cada biblioteca precompilada. El problema no se resuelve eliminando archivos funcionales porque eso podría romper MIDI o rutas de audio en otras aplicaciones. La recomendación oficial de Android sigue siendo recompilar todas las bibliotecas nativas y sus dependencias para 16 KB; `pageSizeCompat` es un modo de compatibilidad.

## Solución aplicada

La compilación v47 añade `android:pageSizeCompat="enabled"` al elemento `<application>` y conserva todas las bibliotecas nativas opcionales. También mantiene `targetSdkVersion=36` para evitar la clasificación de la aplicación como dirigida a una API antigua.

## Resultado

El APK y el AAB v47 compilan correctamente y la auditoría del manifiesto confirma el atributo. La supresión del diálogo en un dispositivo real está pendiente de una instalación fría de v47; por ello el estado permanece `en investigación`.

## Limitaciones pendientes

- No se ha validado todavía la instalación v47 en el Pixel.
- Las bibliotecas precompiladas no se han recompilado todas con segmentos de 16 KB.
- El aviso de Play Protect para una instalación lateral o firma de depuración es un mecanismo distinto y no queda cubierto por esta mitigación.
- Debe verificarse que la ruta de audio/MIDI siga funcionando en un perfil que la utilice.

## Referencias

- [Compatibilidad con tamaños de página de 16 KB de Android](https://developer.android.com/guide/practices/page-sizes)
- [Cambios de comportamiento de Android 16](https://developer.android.com/about/versions/16/behavior-changes-all)
- [Logcat del Pixel](../metricas/runs/RUN-20260919-006/logs/pixel-9a/logcat.txt)
- [Resumen de métricas](../metricas/runs/RUN-20260919-006/resumen.csv)

## Ejecuciones asociadas

- [EXEC-038](../ejecuciones/38-metricas-modern-api36-16k-pixel-cold-install-20260919/matriz.md)
