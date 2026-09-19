# Evidencia: identidad, paquetes y almacenamiento

Captura del host: `2026-09-18T19:27:48-05:00` a `2026-09-18T19:27:53-05:00`.

Comandos principales: `adb devices -l`, `getprop`, `wm size`, `dumpsys package com.cuphead`, `df -k`, `du -sk`, `pm path` y `ls -l`.

| Serial | Modelo | API/ABI | Resolución | versionCode/versionName | firstInstallTime | lastUpdateTime | `/data` disponible | `files` / `rootfs` / `assetpacks` (KiB) |
|---|---|---|---|---|---:|---:|---:|---:|
| `16f88243` | Xiaomi Redmi Note 8 (`ginkgo`) | 36 / `arm64-v8a,armeabi-v7a,armeabi` | 1080x2340 | `32` / `11.1-direct-files-auto-gpu-recovery-v2` | 2026-08-25 22:30:09 | 2026-09-18 18:58:41 | 8.360.440 | 6.738.574 / 6.734.499 / 3.866 |
| `4A021JEBF06953` | Google Pixel 9a (`tegu`) | 37 / `arm64-v8a` | 1080x2424 | `34` / `11.1-direct-files-auto-gpu-recovery-v4` | 2026-09-18 18:25:48 | 2026-09-18 19:19:45 | 10.450.624 | 6.720.339 / 6.720.096 / 42 |
| `51c803a01206` | Xiaomi Mi A3 (`laurel_sprout`) | 36 / `arm64-v8a,armeabi-v7a,armeabi` | 720x1560 | `32` / `11.1-direct-files-auto-gpu-recovery-v2` | 2026-08-25 22:20:43 | 2026-09-18 18:58:57 | 27.520.992 | 6.738.733 / 6.734.692 / 3.832 |
| `100.110.86.15:34341` | Lenovo TB-J606F (`J606F`) | 36 / `arm64-v8a,armeabi-v7a,armeabi` | 1200x2000 | `32` / `11.1-direct-files-auto-gpu-recovery-v2` | 2026-08-24 21:40:16 | 2026-09-18 18:50:00 | 67.525.248 | 6.734.746 / 6.734.499 / 42 |

Los valores de `/data` disponible provienen de `df -k`; el tamaño de la aplicación proviene de `run-as com.cuphead du -sk`. El tamaño del staging externo `local_testing` fue consultado por separado y sólo existía en Pixel: 5.980.480 KiB. En Redmi, Mi A3 y Lenovo la ruta no existía en el momento de la captura.

Tamaños de splits instalados, observados con `pm path` y `ls -l`:

- Base APK: `254632153` bytes en los cuatro.
- Split ABI arm64: `13749113` bytes en los cuatro.
- Split español: `29018` bytes en los cuatro.
- Split de densidad: Pixel/Redmi `53595` bytes (`xxhdpi`); Mi A3 `45369` bytes (`xhdpi`); Lenovo `41234` bytes (`hdpi`).

No se dispone del hash del artefacto instalado ni de una pareja de timestamps que permita calcular el tiempo de `bundletool install-apks`; ambos campos son `N/R`.
