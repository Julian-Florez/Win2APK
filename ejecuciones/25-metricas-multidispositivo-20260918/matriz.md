# Matriz de métricas reproducibles en cuatro dispositivos

- **Versión de plantilla:** 1.0
- **ID:** `EXEC-025`
- **Fecha:** `2026-09-18`
- **Tipo:** observación automatizada por ADB y repetición manual de arranque
- **Resultado general:** parcial; el Pixel no completó la ventana de observación
- **Método:** captura de propiedades, paquete instalado, almacenamiento, procesos, memoria, CPU y `dumpsys gfxinfo`. En el Pixel se ejecutó un arranque con `monkey` y se sondeó `Cuphead.exe` durante 150 s. No se reinstaló, desinstaló ni borró contenido.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` / Cuphead mediante entorno de compatibilidad | Paquete instalado en cada dispositivo |
| Ejecutable | `C:\Cuphead\Cuphead.exe` | Proceso observado en Redmi, Mi A3 y Lenovo; en Pixel durante el arranque |
| Publicación/hash | Hash del AAB/APKS instalado: `N/R` | No se conservó el hash del artefacto correspondiente a cada instalación |
| Método | ADB; una repetición de arranque sólo en Pixel | Las otras tres instalaciones se observaron sin interrumpir sus procesos |
| Entorno | Winlator fork local; configuración exacta seleccionada por dispositivo: `N/R` en esta captura | No se modificó código ni configuración durante la medición |
| Fecha y hora de captura | `2026-09-18T19:27:48-05:00` a `19:32:53-05:00` | Reloj del host; cada dispositivo también fue consultado |
| FPS | FPS real del juego: `N/R` | `dumpsys gfxinfo` sólo mide frames de la interfaz Android, no el render de Cuphead dentro de Wine |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Dispositivos conectados | Cumplido | 4/4 | `adb devices -l` | [`identidad-paquetes-storage.md`](./logs/identidad-paquetes-storage.md) | Redmi y Pixel por USB; Mi A3 por USB; Lenovo por ADB inalámbrico. |
| M-02 | Versión instalada | Parcial | Pixel `versionCode=34`, los otros tres `versionCode=32` | `dumpsys package com.cuphead` | [`identidad-paquetes-storage.md`](./logs/identidad-paquetes-storage.md) | No es una comparación de un único artefacto. |
| M-03 | Tiempo de instalación | N/R | N/R | Sólo existen `firstInstallTime` y `lastUpdateTime` | [`identidad-paquetes-storage.md`](./logs/identidad-paquetes-storage.md) | No se registró el inicio y fin de `bundletool install-apks` en esta ejecución. |
| M-04 | Tiempo hasta `Cuphead.exe` | Parcial | Pixel: aproximadamente 5 s por timestamps de sondeo; restantes: N/R | Arranque medido sólo en Pixel | [`pixel-arranque-150s.txt`](./logs/pixel-arranque-150s.txt) | El cálculo decimal del primer comando tuvo un error de escape; se conservan timestamps y se usa sólo una aproximación en segundos enteros. |
| M-05 | Vida del proceso | Parcial | Pixel: `Cuphead.exe` visto 19:29:58; salida Android 19:31:05.513. Redmi/Mi/Lenovo vivos al corte | Pixel sondeado 150 s; otros observados en una instantánea | [`procesos-memoria-cpu.md`](./logs/procesos-memoria-cpu.md), [`pixel-arranque-150s.txt`](./logs/pixel-arranque-150s.txt) | La permanencia del Pixel fue aproximadamente 67,5 s entre primera detección y salida registrada. |
| M-06 | Motivo de salida | Parcial | Pixel: `reason=3 (LOW_MEMORY)` | `dumpsys activity exit-info` | [`pixel-arranque-150s.txt`](./logs/pixel-arranque-150s.txt) | No se observó un cierre del juego en los otros tres durante el corte. |
| M-07 | PSS/RSS/Graphics | Parcial | Redmi, Mi A3 y Lenovo medidos; Pixel actual `N/R` porque ya había terminado al tomar `meminfo` final | `dumpsys meminfo com.cuphead` | [`procesos-memoria-cpu.md`](./logs/procesos-memoria-cpu.md) | Valores en KiB, tal como los devuelve Android. |
| M-08 | CPU | Parcial | CPU del proceso y total del sistema medidos en una instantánea | `ps` y `dumpsys cpuinfo` | [`procesos-memoria-cpu.md`](./logs/procesos-memoria-cpu.md) | No es un promedio ni un benchmark comparable entre escenas. |
| M-09 | Almacenamiento | Cumplido para la instantánea | Uso de `/data`, tamaño de `files`, `rootfs`, `assetpacks` y staging externo | `df`, `du`, `run-as` | [`identidad-paquetes-storage.md`](./logs/identidad-paquetes-storage.md), [`markers-y-payload.md`](./logs/markers-y-payload.md) | El Pixel conserva `local_testing` externo de 5.980.480 KiB; los otros tres no lo tienen. |
| M-10 | Integridad del payload directo | Cumplido en los cuatro | Marcador de 815 archivos y 5.847.372.363 bytes | `find`/`cat` dentro del sandbox de la aplicación | [`markers-y-payload.md`](./logs/markers-y-payload.md) | El contenido está movido al prefijo; no se afirma que el staging externo sea igual en todos. |
| M-11 | FPS | N/R para FPS real | Redmi proxy Android: 56 frames, 0 janky; Mi A3: 0; Lenovo: 5 frames, 3 janky; Pixel: N/R | `dumpsys gfxinfo` | [`procesos-memoria-cpu.md`](./logs/procesos-memoria-cpu.md) | Estos contadores no representan FPS de `Cuphead.exe`. |
| M-12 | Tasa de éxito | N/R | N/R | No hubo cuatro pruebas equivalentes de duración fija | N/A | No se calcula numerador/denominador a partir de una instantánea. |

## Identidad y resultados por dispositivo

| Dispositivo / serial | Android/API, ABI, resolución | Publicación instalada | RAM del dispositivo | Arranque y proceso | PSS/RSS/Graphics | CPU de proceso (muestra) | Almacenamiento disponible | Estado observado |
|---|---|---|---:|---|---|---|---:|---|
| Redmi Note 8 / `16f88243` | Android 16 / API 36; `arm64-v8a, armeabi-v7a, armeabi`; 1080x2340 | `32`, `11.1-direct-files-auto-gpu-recovery-v2`; actualización 18:58:41 | `MemTotal=3.728.280 KiB` | `Cuphead.exe` vivo; edad derivada aproximada 1.662,8 s al corte | PSS 134.397 KiB; RSS 181.836 KiB; Graphics 63.156 KiB | `Cuphead.exe` 198% en `ps`; total 75% en `dumpsys cpuinfo` | 8.360.440 KiB en `/data`; `files=6.738.574 KiB` | Proceso vivo; marker directo presente; staging externo ausente |
| Pixel 9a / `4A021JEBF06953` | Android 17 / API 37; `arm64-v8a`; 1080x2424 | `34`, `11.1-direct-files-auto-gpu-recovery-v4`; actualización 19:19:45 | `MemTotal=7.752.852 KiB` | `Cuphead.exe` detectado 19:29:58 y desapareció antes del sondeo 70; salida 19:31:05.513 | N/R en la captura actual; histórico EXEC-020 no se mezcla con esta muestra | N/R al momento del cierre | 10.450.624 KiB en `/data`; `files=6.720.339 KiB`; staging externo 5.980.480 KiB | No aprobado para estabilidad en esta ventana; `LOW_MEMORY` |
| Mi A3 / `51c803a01206` | Android 16 / API 36; `arm64-v8a, armeabi-v7a, armeabi`; 720x1560 | `32`, `11.1-direct-files-auto-gpu-recovery-v2`; actualización 18:58:57 | `MemTotal=3.701.920 KiB` | `Cuphead.exe` vivo; edad derivada aproximada 1.672,2 s al corte | PSS 105.839 KiB; RSS 156.884 KiB; Graphics 34.324 KiB | `Cuphead.exe` 183% en `ps`; total 32% en `dumpsys cpuinfo` | 27.520.992 KiB en `/data`; `files=6.738.733 KiB` | Proceso vivo; marker directo presente; staging externo ausente |
| Lenovo TB-J606F / `100.110.86.15:34341` | Android 16 / API 36; `arm64-v8a, armeabi-v7a, armeabi`; 1200x2000 | `32`, `11.1-direct-files-auto-gpu-recovery-v2`; actualización 18:50:00 | `MemTotal=5.813.780 KiB` | `Cuphead.exe` vivo; edad derivada aproximada 1.673,9 s al corte | PSS 131.154 KiB; RSS 186.480 KiB; Graphics 68.056 KiB | `Cuphead.exe` 203% en `ps`; total 55% en `dumpsys cpuinfo` | 67.525.248 KiB en `/data`; `files=6.734.746 KiB` | Proceso vivo; marker directo presente; staging externo ausente |

Las edades aproximadas se derivaron de `/proc/uptime`, el `starttime` de `/proc/<pid>/stat` y `CLK_TCK=100`; no equivalen al tiempo de arranque del juego. El tiempo de arranque de Redmi, Mi A3 y Lenovo queda `N/R` porque los procesos ya estaban iniciados antes de la captura.

## Configuración gráfica y alcance

La matriz registra la publicación y el estado observable, pero no atribuye automáticamente un wrapper o una versión de driver a partir del modelo de GPU. La configuración efectiva del contenedor en cada dispositivo durante esta captura es `N/R` porque no quedó un log runtime completo del selector para los cuatro dispositivos. El perfil histórico de Pixel y las variantes CMOD/DXVK-Sarek se documentan por separado en [EXEC-020](../20-comparacion-graficos-pixel-tensor-mali/matriz.md) y [EXEC-024](../24-investigacion-forks-pixel/matriz.md).

## Fallos y decisiones

- **Limitación relacionada:** [23 - cierre del Pixel por presión de memoria](../../limitaciones/23-pixel-low-memory-metrica-20260918.md).
- **Mensaje exacto:** `reason=3 (LOW_MEMORY) subreason=0 (UNKNOWN) status=0`.
- **Decisión:** conservar los valores faltantes como `N/R`, no calcular FPS real ni una tasa de éxito, y no modificar código en esta ejecución.

## Evidencias

- [Identidad, versiones, timestamps y almacenamiento](./logs/identidad-paquetes-storage.md)
- [Procesos, memoria, CPU y gfxinfo](./logs/procesos-memoria-cpu.md)
- [Arranque y salida del Pixel durante 150 s](./logs/pixel-arranque-150s.txt)
- [Marcadores e integridad del payload](./logs/markers-y-payload.md)

## Repetibilidad y pendientes

- [ ] Repetir los cuatro arranques con el mismo `versionCode`, misma escena y duración fija.
- [ ] Obtener un FPS real mediante una herramienta de telemetría del juego o un HUD verificable; `gfxinfo` no es suficiente.
- [ ] Capturar el hash del AAB/APKS instalado y la duración completa de `bundletool install-apks`.
- [ ] Capturar el selector gráfico efectivo y los logs runtime de cada dispositivo.
- [ ] Repetir PSS/RSS/Graphics y CPU en puntos temporales comparables, no sólo en una instantánea.
