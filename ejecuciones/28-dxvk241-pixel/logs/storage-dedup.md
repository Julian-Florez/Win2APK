# Verificación de almacenamiento directo después de v41

## Estado previo

En el Pixel 9a, el prefijo directo ya contenía el marcador:

```text
files=815
bytes=5847372363
files/rootfs/home/xuser-1/.wine/drive_c/.win2apk-moved-files-v1
```

También existía la ruta exacta:

```text
/sdcard/Android/data/com.cuphead/files/local_testing
5980480 KiB
```

Su contenido incluía `cuphead_files_01-master.apk` a `cuphead_files_05-master.apk`, por lo que se identificó como staging de asset packs y no como el prefijo directo en uso.

## Acción controlada

Se eliminó únicamente:

```text
/sdcard/Android/data/com.cuphead/files/local_testing
```

La comprobación devolvió `target_removed`. No se eliminaron `files/rootfs`, el prefijo Wine ni el APK instalado.

## Verificación posterior

```text
timestamp=2026-09-18T20:55:06-05:00
com.cuphead=10432
Cuphead.exe=10654
Graphics: 475092 KiB
TOTAL PSS: 553377 KiB
TOTAL RSS: 677636 KiB
local_testing=
files=815
bytes=5847372363
```

El juego permaneció en ejecución después de retirar el staging. Esta evidencia demuestra la eliminación de la duplicación observada en el Pixel, no una regla universal para cualquier instalación o dispositivo.
