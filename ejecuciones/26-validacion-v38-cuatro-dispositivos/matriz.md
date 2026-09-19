# EXEC-026: validación de la publicación v38 en cuatro dispositivos

## Identificación

- ID: `EXEC-026`
- Fecha: 2026-09-18
- Tipo: validación de publicación, arranque y métricas comparables
- Objetivo: comprobar la misma APK base-only v38 en Pixel 9a, Lenovo TB-J606F, Redmi Note 8 y Xiaomi Mi A3 sin volver a copiar el payload de Cuphead.
- Método: instalación visible mediante `adb install -r`, conservación de datos existentes, arranque de la actividad principal y observación ADB.
- Agente de métricas: Harvey, `01a0b70b-d522-7e80-bd8a-e614c803804f`; su matriz base está en [EXEC-025](../25-metricas-multidispositivo-20260918/matriz.md).

## Publicación probada

| Campo | Valor |
|---|---|
| VersionCode | `38` |
| VersionName | `11.1-direct-files-auto-gpu-recovery-v8-fcharan-largeheap` |
| APK | `universal.apk` base-only |
| Tamaño APK | `273711050` bytes |
| SHA-256 APK | `2e8f9776b95b5dc923f365781bebe4fbe6e567af214b7bb8fcd37cb52b0c6c5e` |
| Payload esperado | `815` archivos, `5847372363` bytes |
| Modo de datos | direct files, enlace lógico `move` |
| Resolución configurada | `1280x720` |
| Perfil GPU | automático: Adreno usa Turnip + Gladio; Mali/unknown usa Vortek + Gladio + DXVK-Sarek + BCn Fcharan |
| Variación v38 | `android:largeHeap="true"` |

El payload no forma parte del APK probado. La evidencia disponible antes de esta validación conserva el marcador de `815` archivos y `5847372363` bytes en los cuatro dispositivos.

## Dispositivos y resultados

| Dispositivo | Serial | GPU / Android | Instalación | Perfil observado | Cuphead.exe | FPS real | RAM / CPU | Resultado |
|---|---|---|---:|---|---|---|---|---|
| Pixel 9a | `4A021JEBF06953` | Mali-G715 / API 37 | `12417 ms` | Mali/unknown, Vortek + Gladio, DXVK-Sarek 1.12.1 + Fcharan BCn ETC2 fast | vivo en el corte de 65 s; cierre a `20:19:12`, `LOW_MEMORY` | N/R | PSS `3101564 KiB`, RSS `3084448 KiB` en el corte; CPU N/R | No estable: cierre por `LOW_MEMORY` |
| Lenovo TB-J606F | `100.110.86.15:34341` | Adreno 610 / API 36 | `21365 ms` | Adreno, Turnip + Gladio, DXVK | iniciado; crash Unity a `20:18:26`, luego `Finished with status 0` | N/R | N/R | No estable: `UnityPlayer.dll caused an Access Violation (0xc0000005)` |
| Redmi Note 8 | `16f88243` | Adreno 610 / API 36 | `12324 ms` | Adreno, Turnip + Gladio, DXVK | vivo en el corte de 65 s | N/R | PSS `112929 KiB`, RSS `173200 KiB`; Cuphead.exe `209%` y app `19%` en instantánea | Arranque conservado en el corte |
| Xiaomi Mi A3 | `51c803a01206` | Adreno 610 / API 36 | `10630 ms` | Adreno, Turnip + Gladio, DXVK | vivo en el corte de 65 s | N/R | PSS `81926 KiB`, RSS `136304 KiB`; Cuphead.exe `185%` y app `18%` en instantánea | Arranque conservado en el corte |

`N/R` indica que el dato aún no fue registrado, no que sea cero ni que la prueba haya fallado.

## Instrumentación

- Instalación: tiempo medido alrededor de `adb install -r` con reloj monotónico del host.
- Perfil: `Win2APKGraphicsProfile` en logcat, incluyendo renderer, vendor, perfil y wrapper.
- Proceso: `pidof com.cuphead` y `pidof Cuphead.exe`.
- Memoria: `dumpsys meminfo com.cuphead` y RSS del proceso cuando esté disponible.
- CPU: `dumpsys cpuinfo` durante la ventana de observación.
- FPS: N/R salvo que se capture HUD de DXVK o una medición de frames del juego. `gfxinfo` no se tratará como FPS de Cuphead.
- Almacenamiento: marcador del payload, conteo y suma de bytes, sin duplicar la instalación.

## Observación, interpretación y decisión

### Observación inicial

La variante v38 inició en el Pixel con el perfil Mali y redujo la memoria inicial frente a las variantes F-03 y F-04, pero el proceso v38 terminó después con `reason=3 (LOW_MEMORY)` y `rss=342MB`.

### Interpretación provisional

`largeHeap` no constituye una corrección suficiente para el cierre del Pixel. La validación de los otros tres equipos es necesaria para separar una regresión general de una limitación específica del entorno Mali/Tensor.

### Decisión

No publicar v38 como solución estable universal hasta completar las cuatro filas y repetir el Pixel con un criterio temporal explícito. Si el Pixel vuelve a terminar por `LOW_MEMORY`, se conservará v38 únicamente como variante de diagnóstico y se abrirá una prueba separada con otra versión de DXVK o wrapper.

## Aislamiento de `largeHeap` en Lenovo

Después del crash de v38, se intentó instalar la APK v37 sin `largeHeap` usando `adb install -r -d`. La primera orden sin `-d` fue rechazada por `INSTALL_FAILED_VERSION_DOWNGRADE`; la orden explícita con `-d` instaló correctamente en `26457 ms`. Tras el arranque, Lenovo conservó `Cuphead.exe` vivo en el corte de aproximadamente 30 s, con PSS `118777 KiB` y RSS `187976 KiB`. Este resultado no prueba todavía una sesión larga, pero separa el crash observado en v38 de la variante sin `largeHeap`.

## Evidencia

Los registros de instalación, perfiles, procesos, memoria y marcadores están en [v38-cuatro-dispositivos.md](./logs/v38-cuatro-dispositivos.md), [lenovo-v38-crash.txt](./logs/lenovo-v38-crash.txt) y [lenovo-v37-fallback.txt](./logs/lenovo-v37-fallback.txt). Las pruebas anteriores están enlazadas en [EXEC-024](../24-investigacion-forks-pixel/matriz.md) y [EXEC-025](../25-metricas-multidispositivo-20260918/matriz.md).
