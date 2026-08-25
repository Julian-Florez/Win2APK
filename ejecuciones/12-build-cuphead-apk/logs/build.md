# Registro de compilación — EXEC-012

## Observación

- El primer intento con `./gradlew` devolvió `Permission denied`; se continuó con el wrapper equivalente `bash gradlew`.
- Sin variables Android, Gradle informó: `SDK location not found. Define a valid SDK location with an ANDROID_HOME environment variable or by setting the sdk.dir path in your project's local properties file at '/home/julian/Tesis/Win2APK/winlator/app/local.properties'.`
- Se localizó el SDK en `/home/julian/Android/Sdk` y se reintentó sin crear `local.properties`.
- La tarea `:app:prepareCoreAssets` terminó correctamente y registró 447 reemplazos en `rootfs.tzst`, además de los demás assets Core.
- La compilación falló en `:app:compressDebugAssets` con el mensaje exacto: `Required array size too large`.
- Existía un archivo `winlator/app/app/build/outputs/apk/debug/app-debug.apk` de 262.719.844 bytes con fecha 2026-08-18; su contenido referencia `assets/test_app.tzst`, por lo que no se considera resultado de esta ejecución.

## Interpretación

La configuración y las tareas de preparación del Core funcionan con Cuphead. El bloqueo aparece al convertir el conjunto de assets en el APK, cuando el empaquetador intenta procesar el archivo `cuphead.tzst` de 4.782.573.186 bytes.

## Decisión

No reutilizar ni entregar el APK histórico. Mantener el asset local para investigar una estrategia de distribución que no requiera incluir toda la publicación de Cuphead dentro de un único APK.
