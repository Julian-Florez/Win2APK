# Log de build — EXEC-014

## Configuración aplicada

Se reemplazó el asset pack único `cuphead_data` por:

```text
cuphead_data_01  -> cuphead_data_01.part  (1800000000 bytes)
cuphead_data_02  -> cuphead_data_02.part  (1800000000 bytes)
cuphead_data_03  -> cuphead_data_03.part  (1182573186 bytes)
```

La concatenación de las partes produjo el SHA-256:

```text
33aad774c30e07be8088160d35bacdd191eae7d06ed0fd507f396c726d7eff93
```

## Build final

```text
nix shell nixpkgs#jdk17 --command env JAVA_HOME=... ANDROID_HOME=/home/julian/Android/Sdk ANDROID_SDK_ROOT=/home/julian/Android/Sdk bash gradlew clean bundleDebug --console=plain
```

Resultado observado: AAB generado en `winlator/app/app/build/outputs/bundle/debug/app-debug.aab`, con `5.043.469.401` bytes.

Durante el primer reintento apareció el mensaje `Could not get unknown property 'coreAssetPackName'`; se corrigió la referencia obsoleta a la nueva lista `coreAssetPackNames` y el build final continuó.
