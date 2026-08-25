# Log de bundletool — EXEC-014

## Conversión

```text
java -jar tools/bundletool-all-1.18.3.jar build-apks \
  --bundle=winlator/app/app/build/outputs/bundle/debug/app-debug.aab \
  --output=winlator/app/build/cuphead-lenovo-segmented.apks \
  --local-testing --connected-device --device-id=HA1QXMW2 --overwrite
```

Resultado: se generó `winlator/app/build/cuphead-lenovo-segmented.apks` con `5.050.689.275` bytes.

## Instalación

```text
java -jar tools/bundletool-all-1.18.3.jar install-apks \
  --apks=winlator/app/build/cuphead-lenovo-segmented.apks \
  --device-id=HA1QXMW2
```

Resultado observado: bundletool extrajo el set local, transfirió los splits y `pm path com.cuphead` confirmó:

```text
base.apk
split_config.arm64_v8a.apk
split_config.es.apk
split_config.hdpi.apk
split_cuphead_data_01.apk
split_cuphead_data_02.apk
split_cuphead_data_03.apk
```
