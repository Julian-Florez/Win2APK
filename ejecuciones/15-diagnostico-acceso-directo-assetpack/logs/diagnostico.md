# Diagnóstico PAD — EXEC-015

Salida de `AssetPackDiagnostics` durante el primer arranque:

```text
I/Win2APKAssetPack: pack=cuphead_data_01 storageMethod=1 path=null assetsPath=null assetsDirectory=N/A
I/Win2APKAssetPack: pack=cuphead_data_02 storageMethod=1 path=null assetsPath=null assetsDirectory=N/A
I/Win2APKAssetPack: pack=cuphead_data_03 storageMethod=1 path=null assetsPath=null assetsDirectory=N/A
```

Interpretación respaldada por la API de Play Asset Delivery: el pack está en el modo de assets del APK, no en una carpeta de archivos. `assetsPath` no puede usarse como destino de enlaces para Wine.
