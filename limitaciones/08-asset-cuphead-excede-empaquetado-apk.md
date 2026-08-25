# Asset de Cuphead excede la capacidad del empaquetado APK

## Descripción

La publicación instalada de Cuphead puede ejecutarse en el prefijo Lutris, pero el asset comprimido de la carpeta ocupa `4.782.573.186` bytes (aproximadamente 4,45 GiB). La compilación de Win2APK falla al comprimir los assets del APK.

## Contexto técnico

- Fecha: 2026-08-24.
- Proyecto: Win2APK con Winlator Core.
- Asset: `winlator/app/app/src/main/assets/cuphead.tzst`.
- Hash SHA-256: `33aad774c30e07be8088160d35bacdd191eae7d06ed0fd507f396c726d7eff93`.
- Configuración: `Cuphead`, directorio Windows `Cuphead`, ejecutable `Cuphead.exe`.
- Android SDK usado: `/home/julian/Android/Sdk`.
- Dispositivo Android: N/A.
- ABI: `arm64-v8a` configurada; no se alcanzó la generación del APK Cuphead.

## Reproducción o evidencia

1. Instalar Cuphead en Lutris con el prefijo `/home/julian/Games/cuphead`.
2. Confirmar el primer inicio visible de `Cuphead.exe`.
3. Generar `cuphead.tzst` desde `C:\Program Files\Cuphead`, excluyendo `_Redist`, `unins000.*` y `goggame-*`.
4. Ejecutar `ANDROID_HOME=/home/julian/Android/Sdk ANDROID_SDK_ROOT=/home/julian/Android/Sdk bash gradlew assembleDebug --console=plain` desde `winlator/app`.
5. Observar el mensaje exacto:

   `Required array size too large`

   en la tarea `:app:compressDebugAssets`.

La evidencia detallada está en [EXEC-012](../ejecuciones/12-build-cuphead-apk/matriz.md) y su [log de compilación](../ejecuciones/12-build-cuphead-apk/logs/build.md).

## Impacto

No se generó un APK nuevo utilizable para Cuphead. El APK histórico presente en `build/outputs` contiene `test_app.tzst` y no debe confundirse con un resultado de Cuphead.

## Análisis técnico

La preparación de assets del Core termina correctamente, por lo que la observación apunta al empaquetado del archivo grande y no a la instalación Wine ni a la configuración de Cuphead. La causa exacta interna del `Array` no fue determinada; se registra como hipótesis que el empaquetador o una etapa de compresión usa estructuras con límite de tamaño inferior al asset.

## Solución aplicada

No se aplicó una solución definitiva. Se conservaron el asset y la configuración para continuar la investigación. La instalación original no fue borrada ni modificada.

## Resultado

Reproducido en una compilación local: la instalación y el primer inicio funcionan en Lutris/GE-Proton11-5, pero la inclusión directa del asset completo en la APK no funciona con el pipeline actual.

## Limitaciones pendientes

- No se ha probado una distribución mediante OBB, asset pack, descarga posterior o segmentación.
- No se ha determinado un tamaño máximo documentado para este pipeline.
- No se debe afirmar compatibilidad con Android hasta resolver la distribución y probar en un dispositivo.

## Referencias

- [Configuración de Win2APK](../config/win2apk.json)
- [Build de la aplicación](../winlator/app/app/build.gradle)
- [Flujo de extracción del asset](../winlator/app/app/src/main/java/com/winlator/container/ContainerManager.java)

## Ejecuciones asociadas

- [EXEC-011: instalación y primer inicio de Cuphead](../ejecuciones/11-instalacion-cuphead-lutris/matriz.md)
- [EXEC-012: compilación de APK con asset de Cuphead](../ejecuciones/12-build-cuphead-apk/matriz.md)
