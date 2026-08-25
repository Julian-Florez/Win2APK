# Log de bundletool — EXEC-013

## Comando

```text
java -jar tools/bundletool-all-1.18.3.jar build-apks \
  --bundle=winlator/app/app/build/outputs/bundle/debug/app-debug.aab \
  --output=winlator/app/build/cuphead-lenovo-local.apks \
  --local-testing \
  --connected-device \
  --device-id=HA1QXMW2 \
  --overwrite
```

## Resultado exacto

```text
[BT:1.18.3] Error: Unable to sign APK.
...
Caused by: com.android.apksig.apk.ApkFormatException: Malformed APK: not a ZIP archive
...
Caused by: com.android.apksig.zip.ZipFormatException: ZIP Central Directory overlaps with End of Central Directory. CD end: 8589934590, EoCD start: 4782574132
```

No se generó un archivo `.apks` válido y no se ejecutó `bundletool install-apks`.
