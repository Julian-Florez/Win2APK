# Registro v38 en cuatro dispositivos

## Artefacto

- VersionCode: `38`
- VersionName: `11.1-direct-files-auto-gpu-recovery-v8-fcharan-largeheap`
- APK universal base-only: `273711050` bytes
- SHA-256: `2e8f9776b95b5dc923f365781bebe4fbe6e567af214b7bb8fcd37cb52b0c6c5e`
- Payload conservado: `files=815`, `bytes=5847372363` en los cuatro dispositivos.

## Instalación

```text
pixel  4A021JEBF06953       Success 12417 ms
lenovo 100.110.86.15:34341  Success 21365 ms
redmi  16f88243             Success 12324 ms
mia3   51c803a01206         Success 10630 ms
```

Las instalaciones se hicieron con `adb install -r`. No se desinstaló el paquete ni se volvió a copiar el juego.

## Perfil y arranque

```text
Pixel 9a:
09-18 20:17:59.828 I/Win2APKGraphicsProfile(23533): device=Google/Pixel 9a hardware=tegu renderer=Mali-G715 vendor=ARM profile=Mali/unknown / Vortek + Gladio / DXVK-Sarek 1.12.1 + Fcharan BCn ETC2 fast graphicsDriver=vortek,gladio dxwrapper=dxvk
09-18 20:18:00.227 I/WinlatorProcess(23533): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Lenovo TB-J606F:
09-18 20:18:00.999 I/Win2APKGraphicsProfile( 9652): device=LENOVO/Lenovo TB-J606F hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:18:04.231 I/WinlatorProcess( 9652): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Redmi Note 8:
09-18 20:18:00.478 I/Win2APKGraphicsProfile(18219): device=Xiaomi/Redmi Note 8 hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:18:03.644 I/WinlatorProcess(18219): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"

Xiaomi Mi A3:
09-18 20:18:01.239 I/Win2APKGraphicsProfile(25141): device=Xiaomi/Mi A3 hardware=qcom renderer=Adreno (TM) 610 vendor=Qualcomm profile=Adreno / Turnip + Gladio / DXVK graphicsDriver=turnip,gladio dxwrapper=dxvk
09-18 20:18:04.234 I/WinlatorProcess(25141): Starting: ... wine explorer /desktop=nogui,1280x720 ... "Cuphead.exe"
```

## Corte de memoria, CPU y procesos, `2026-09-18 20:19:04 -05:00`

```text
Pixel:  com.cuphead=23533, Cuphead.exe=23916, TOTAL PSS=3101564 KiB, TOTAL RSS=3084448 KiB, Graphics=3036716 KiB
Redmi:  com.cuphead=18219, Cuphead.exe=18520, TOTAL PSS=112929 KiB, TOTAL RSS=173200 KiB, Graphics=63108 KiB, Cuphead.exe=209%, app=19%
Mi A3:  com.cuphead=25141, Cuphead.exe=25263, TOTAL PSS=81926 KiB, TOTAL RSS=136304 KiB, Graphics=34128 KiB, Cuphead.exe=185%, app=18%
Lenovo: com.cuphead=9652, Cuphead.exe no estaba vivo en el corte; el proceso había terminado con status 0
```

El FPS real de Cuphead es `N/R`. Los contadores Android de `gfxinfo` no se usan como FPS del juego.

## Cierre observado

```text
Pixel:  09-18 20:19:12.175, reason=3 (LOW_MEMORY), rss=350MB
Lenovo: 09-18 20:18:30.456, WinlatorProcess Finished with status 0; Crash Unity registrado en el payload
```

