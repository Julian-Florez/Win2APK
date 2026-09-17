# Registro del prototipo direct-files

## Ubicación y lectura

```text
state name=probe_assets status=COMPLETED bytes=8759/8759 error=0
resolved storageMethod=0 path=/data/data/com.win2apk.directfiles.probe/files/assetpacks/probe_assets/1/1
assetsPath=/data/data/com.win2apk.directfiles.probe/files/assetpacks/probe_assets/1/1/assets
pack files count=4
seek file=alpha.txt size=50 offset=25 read=16
mmap file=alpha.txt size=50 firstByte=97
linkPrefix=.../files/linked-prefix links=4 copiedBytes=0
link verify files=5 symlinks=4 readable=5
```

## Actualización

```text
initial location=null
resolved storageMethod=0 path=/data/data/com.win2apk.directfiles.probe/files/assetpacks/probe_assets/2/2
link verify files=5 symlinks=4 readable=5
```

## Fuente de bundletool y limpieza

```text
localTesting phase=before-delete ... exists=true files=77 bytes=7240952
localTesting delete ... success=true existsAfter=false
post-delete storageMethod=0 ... assetsPath=.../assetpacks/probe_assets/3/3/assets
link verify files=5 symlinks=4 readable=5
```

Después de cerrar y abrir la aplicación, `local_testing` siguió ausente y los cuatro enlaces permanecieron legibles.

