# Log de bundletool — EXEC-015

```text
java -jar tools/bundletool-all-1.18.3.jar build-apks \
  --bundle=winlator/app/app/build/outputs/bundle/debug/app-debug.aab \
  --output=winlator/app/build/cuphead-direct-diagnostic.apks \
  --local-testing --connected-device --device-id=HA1QXMW2 --overwrite
```

Resultado: `cuphead-direct-diagnostic.apks`, `5.051.038.271` bytes.

Se desinstaló la versión previa con `adb uninstall com.cuphead`, conforme a la limitación de actualizaciones del modo local, y se ejecutó:

```text
java -jar tools/bundletool-all-1.18.3.jar install-apks \
  --apks=winlator/app/build/cuphead-direct-diagnostic.apks \
  --device-id=HA1QXMW2
```

La instalación terminó con transferencia de los APK base y configuración. El paquete `com.cuphead` inició correctamente.
