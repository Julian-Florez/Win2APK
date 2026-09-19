# Evidencia: procesos, memoria, CPU y `gfxinfo`

Captura de procesos y memoria: `2026-09-18T19:27:48-05:00` a `19:27:53-05:00`. Los porcentajes de CPU son instantáneas, no promedios.

| Serial | Proceso Android / `Cuphead.exe` | RES de `ps` | CPU de `ps` | PSS / RSS de `dumpsys meminfo` (KiB) | Graphics (KiB) | CPU total de `dumpsys cpuinfo` | RAM del dispositivo |
|---|---|---:|---:|---|---:|---:|---:|
| `16f88243` | `com.cuphead` / `Cuphead.exe` | 117M / 216M | 19,8% / 198% | 134397 / 181836 | 63156 | 75% | MemTotal 3728280 KiB; MemAvailable 440044 KiB; SwapFree 159756 KiB |
| `51c803a01206` | `com.cuphead` / `Cuphead.exe` | 121M / 235M | 19,0% / 183% | 105839 / 156884 | 34324 | 32% | MemTotal 3701920 KiB; MemAvailable 279524 KiB; SwapFree 1416732 KiB |
| `100.110.86.15:34341` | `com.cuphead` / `Cuphead.exe` | 80M / 759M | 21,1% / 203% | 131154 / 186480 | 68056 | 55% | MemTotal 5813780 KiB; MemAvailable 1086436 KiB; SwapFree 2129780 KiB |
| `4A021JEBF06953` | No había proceso al consultar `meminfo` final | N/R | N/R | N/R en esta corrida | N/R | 37% total tras el cierre | MemTotal 7752852 KiB; MemAvailable 2987564 KiB; SwapFree 2371440 KiB |

`Cuphead.exe` estaba vivo en Redmi, Mi A3 y Lenovo al corte. A partir de `/proc/uptime`, `starttime` y `CLK_TCK=100`, sus edades derivadas aproximadas fueron 1662,8 s, 1672,2 s y 1673,9 s, respectivamente. Esto no es tiempo de arranque; sólo indica cuánto llevaba vivo el proceso respecto de la instantánea.

Contadores de `dumpsys gfxinfo com.cuphead`:

```text
16f88243: Total frames rendered=56; Janky frames=0 (0.00%); Missed Vsync=0
51c803a01206: Total frames rendered=0; Janky frames=0 (0.00%); Missed Vsync=0
100.110.86.15:34341: Total frames rendered=5; Janky frames=3 (60.00%); Missed Vsync=1
4A021JEBF06953: sin bloque de gfxinfo utilizable después del cierre
```

Estos contadores pertenecen a la superficie/interfaz Android. No se convierten en FPS de Cuphead y por eso el FPS real queda `N/R`.
