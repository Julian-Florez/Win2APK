# Limitación 03: duplicación de bibliotecas nativas durante el empaquetado

- **Proyecto:** Win2APK
- **Aplicación:** Winlator 11.1 modificada
- **Entorno:** Gradle 7.3.3, Android Gradle Plugin 7.2.2, CMake 3.22.1 y NDK 24.0.8215888
- **Estado:** resuelta experimentalmente
- **Fecha de registro:** 2026-08-18

## Descripción

La compilación nativa terminó correctamente, pero la tarea `mergeDebugNativeLibs` rechazó el APK porque algunas bibliotecas estaban presentes en dos entradas de la build: `app/src/main/jniLibs/arm64-v8a` y la salida de targets IMPORTED declarados por `midihandler/CMakeLists.txt`.

## Contexto técnico

El módulo MIDI importa bibliotecas precompiladas desde `jniLibs`, mientras que el Android Gradle Plugin también recibe esas bibliotecas desde la compilación nativa de CMake. Las copias observadas tenían el mismo tamaño y procedencia local.

## Reproducción o evidencia

El mensaje exacto fue:

```text
2 files found with path 'lib/arm64-v8a/libFLAC.so' from inputs:
      - .../app/build/intermediates/merged_jni_libs/debug/out/arm64-v8a/libFLAC.so
      - .../app/build/intermediates/cxx/Debug/b5q55f6h/obj/arm64-v8a/libFLAC.so
```

La tarea afectada fue `:app:mergeDebugNativeLibs`.

## Impacto

La build completa no podía producir el APK, aunque el código Java y las bibliotecas nativas ya habían compilado.

## Análisis técnico

La duplicación se produce por la combinación de `jniLibs` y bibliotecas IMPORTED de CMake. El error no estaba relacionado con la lógica de creación automática del contenedor.

## Solución aplicada

Se añadieron reglas `packagingOptions.pickFirst` en `app/build.gradle` para las bibliotecas compartidas importadas por `midihandler`, incluyendo `libFLAC.so`, `libfluidsynth.so`, `libogg.so`, `libvorbis*.so` y las demás copias equivalentes.

## Resultado

La tarea `assembleDebug` finalizó con `BUILD SUCCESSFUL`. El APK debug generado fue verificado con APK Signature Scheme v2.

## Limitaciones pendientes

- La solución se validó para la ABI `arm64-v8a`.
- La igualdad binaria de las copias debe conservarse en futuras actualizaciones de las bibliotecas.
- Todavía falta instalar y ejecutar el APK en un dispositivo Android.

## Referencias

- [Configuración de empaquetado](../winlator/app/app/build.gradle)
- [CMake del módulo MIDI](../winlator/app/app/src/main/cpp/midihandler/CMakeLists.txt)
- [Ejecución asociada](../ejecuciones/03-build-apk-winlator/matriz.md)

## Ejecuciones asociadas

- [EXEC-003: generación del APK de Winlator](../ejecuciones/03-build-apk-winlator/matriz.md)

