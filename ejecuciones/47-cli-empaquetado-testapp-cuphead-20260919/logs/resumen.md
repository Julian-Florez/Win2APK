# Resumen de comandos y resultados — EXEC-047

## Validación

```text
WIN2APK_BUNDLETOOL=/tmp/bundletool-all-1.18.3.jar cargo run -- validate config/example.testapp.json
Configuración válida: 463 archivos, 167479464 bytes, 1 asset packs

cargo run -- validate config/win2apk.json
Configuración válida: 815 archivos, 5847372363 bytes, 5 asset packs
```

## Build genérico final

```text
cargo run -- build config/example.testapp.json --output /tmp/win2apk-cli-test-dist-v5
BUILD SUCCESSFUL in 41s
jar signed.
Empaquetado terminado: /tmp/win2apk-cli-test-dist-v5
```

El AAB final de la prueba contiene 1.500 entradas, el asset pack
`win2apk_payload_001` y no contiene entradas `Cuphead`.

## Build Cuphead final

```text
cargo run -- build config/win2apk.json --output /tmp/win2apk-cuphead-dist
BUILD SUCCESSFUL in 14s
Task :app:signReleaseBundle SKIPPED
jar signed.
Empaquetado terminado: /tmp/win2apk-cuphead-dist
```

El plan registró 815 archivos en 5 packs. `bundletool validate` aprobó el AAB.
`bundletool get-size total` devolvió `MIN=291583413, MAX=291613937`; esa salida
es una estimación de selección de dispositivo y no el tamaño físico del APKS.

## Advertencias no bloqueantes

- CMake informó que encontró SDK XML versión 4 aunque esa versión de CMake solo
  entiende hasta la versión 3.
- El código nativo existente produjo advertencias de conversión de tipos.
- El proyecto existente conserva advertencias de sustituciones múltiples en
  algunos recursos de idioma.

Ninguna de estas advertencias impidió los dos builds finales.
