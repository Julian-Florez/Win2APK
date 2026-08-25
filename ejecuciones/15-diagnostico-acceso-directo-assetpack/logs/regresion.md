# Regresión de ejecución — EXEC-015

Después del diagnóstico, el flujo actual terminó la extracción y produjo:

```text
Cuphead.exe: 650752 bytes
Archivos en Cuphead: 804
Tamaño de la carpeta: 5.4G aproximadamente
```

Procesos observados:

```text
wineserver
winhandler.exe
Cuphead.exe
```

Log de Unity:

```text
Initialize engine version: 2017.4.9f1 (6d84dfc57ccf)
Direct3D: Version: Direct3D 11.0 [level 11.1]
Renderer: Turnip Adreno (TM) 610 (ID=0x6010000)
<RI> Initialized touch support.
```

La prueba terminó con `adb shell am force-stop com.cuphead`; no quedaron procesos Wine ni Cuphead activos.
