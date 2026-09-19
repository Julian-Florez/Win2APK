# Evidencia: marcador de instalación directa y payload

Comando: `adb -s SERIAL shell 'run-as com.cuphead find files -name .win2apk-moved-files-v1 -print -exec cat {} \\;'`.

```text
16f88243:
files=815
bytes=5847372363
version=1
fileCount=815
fileBytes=5847372363
destination=/data/user/0/com.cuphead/files/rootfs/home/xuser-1/.wine/drive_c/Cuphead
files/rootfs/home/xuser-1/.wine/drive_c/.win2apk-moved-files-v1
files/.win2apk-moved-files-v1

4A021JEBF06953:
files=815
bytes=5847372363
files/rootfs/home/xuser-1/.wine/drive_c/.win2apk-moved-files-v1

51c803a01206:
files=815
bytes=5847372363
version=1
fileCount=815
fileBytes=5847372363
destination=/data/user/0/com.cuphead/files/rootfs/home/xuser-1/.wine/drive_c/Cuphead
files/rootfs/home/xuser-1/.wine/drive_c/.win2apk-moved-files-v1
files/.win2apk-moved-files-v1

100.110.86.15:34341:
files=815
bytes=5847372363
files/rootfs/home/xuser-1/.wine/drive_c/.win2apk-moved-files-v1
```

El resultado verifica el contrato del payload directo en los cuatro sandbox. No demuestra que todos los archivos externos hayan sido eliminados: durante esta captura Pixel conservó `/sdcard/Android/data/com.cuphead/files/local_testing` con 5.980.480 KiB, mientras esa ruta no existía en los otros tres dispositivos.
