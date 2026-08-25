# Log de ejecución Android — EXEC-014

## Instalación y extracción

El paquete instalado fue `com.cuphead`, con `versionCode=28` y `versionName=11.1-core`. La primera ejecución creó el prefijo y dejó el ejecutable en:

```text
files/rootfs/home/xuser-1/.wine/drive_c/Cuphead/Cuphead.exe
```

Mediciones observadas:

```text
Cuphead.exe: 650752 bytes
Archivos en Cuphead: 804
Tamaño aproximado de la carpeta: 5.4G
```

## Arranque

```text
I/WinlatorProcess: Starting: .../box64 wine explorer /desktop=nogui,1280x720 C:\windows\winhandler.exe /dir C:\\Cuphead "Cuphead.exe"
Initialize engine version: 2017.4.9f1 (6d84dfc57ccf)
Direct3D: Version: Direct3D 11.0 [level 11.1]
Renderer: Turnip Adreno (TM) 610 (ID=0x6010000)
<RI> Initialized touch support.
Rewired: Found Xinput1_4.dll.
Galaxy SDK was initialized
Build version 1.3.4
[PlayerData] No data. Saving default data to cloud
```

Durante la captura se observaron `wineserver`, `winhandler.exe` y `Cuphead.exe`. Al finalizar se ejecutó `adb shell am force-stop com.cuphead`; el paquete permaneció instalado y los procesos asociados dejaron de aparecer.
