# Instalación y arranque v41

## Instalación

```text
Pixel 9a       4A021JEBF06953        Success 11136 ms
Lenovo         100.110.86.15:34341   Success 21846 ms
Redmi Note 8   16f88243              Success 13301 ms
Xiaomi Mi A3   51c803a01206          Success 10656 ms
```

Todas las instalaciones usaron `adb install -r`, sin desinstalar el paquete ni copiar de nuevo Cuphead.

## Perfil y proceso

```text
Pixel:
09-18 20:44:05.574 I/Win2APKGraphicsProfile(10432): device=Google/Pixel 9a hardware=tegu renderer=Mali-G715 vendor=ARM profile=Mali/unknown / Vortek + Gladio / DXVK 2.4.1 + Fcharan BCn ETC2 auto graphicsDriver=vortek,gladio dxwrapper=dxvk
09-18 20:44:07.140 I/WinlatorProcess(10432): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Lenovo:
09-18 20:46:12.547 I/Win2APKGraphicsProfile(13602): device=LENOVO/Lenovo TB-J606F hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:46:15.917 I/WinlatorProcess(13602): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Redmi:
09-18 20:46:11.871 I/Win2APKGraphicsProfile(21986): device=Xiaomi/Redmi Note 8 hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:46:14.964 I/WinlatorProcess(21986): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Mi A3:
09-18 20:46:12.744 I/Win2APKGraphicsProfile(27653): device=Xiaomi/Mi A3 hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:46:15.646 I/WinlatorProcess(27653): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"
```

## Marcadores del payload

En el corte final de los cuatro dispositivos, el marcador informó `files=815` y `bytes=5847372363`. En Redmi, Mi A3 y Lenovo también aparecieron `version=1`, `fileCount=815`, `fileBytes=5847372363` y el destino dentro del prefijo.

