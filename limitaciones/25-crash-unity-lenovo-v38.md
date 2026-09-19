# 25. Crash de Unity en Lenovo TB-J606F con la publicación v38

## Descripción

La publicación v38 inició la sesión de Winlator en el Lenovo TB-J606F, pero Cuphead terminó con un acceso inválido dentro de `UnityPlayer.dll`. La variante v37, que no incluye `android:largeHeap="true"`, conservó `Cuphead.exe` vivo en una observación corta posterior.

## Contexto técnico

- Dispositivo: Lenovo TB-J606F, Adreno 610, Android API 36.
- Publicación v38: versionCode `38`, `11.1-direct-files-auto-gpu-recovery-v8-fcharan-largeheap`.
- Perfil automático: `Adreno / Turnip + Gladio / DXVK`.
- Resolución del contenedor: `1280x720`.
- Payload: `815` archivos, `5847372363` bytes, marcador directo presente.
- La variante v37 usa el mismo perfil Adreno, sin `largeHeap`, con versionCode `37`.

## Reproducción o evidencia

En la prueba de v38, el log de Cuphead creó `Crash_2026-09-19_011812/error.log` y contiene exactamente:

```text
Cuphead [version: Unity 2017.4.9f1 (6d84dfc57ccf)]

UnityPlayer.dll caused an Access Violation (0xc0000005)
  in module UnityPlayer.dll at 0033:7ecddb53.

Error occurred at 2026-09-19_011826.
C:\Cuphead\Cuphead.exe, run by xuser.
65% memory in use.
5678 MB physical memory [1978 MB free].
8750 MB paging file [4056 MB free].
134217728 MB user address space [134217334 MB free].
Write to location 022c48b5 caused an access violation.
```

El cierre ocurrió después del inicio de Cuphead y fue acompañado por `WinlatorProcess Finished with status 0`. El logcat también mostró `java.io.IOException: Failed to send data`, pero ese mensaje aparece durante el cierre de la sesión y no se toma como causa primaria.

## Impacto

La v38 no puede considerarse una publicación estable para el Lenovo. La misma APK base-only sí conservó el payload directo y no exigió volver a copiar los archivos del juego.

## Análisis técnico

La observación es consistente con un crash del proceso Windows/Unity, no con un cierre por `LOW_MEMORY` del proceso Android. La comparación v37 es un aislamiento preliminar de `largeHeap`, porque v37 no incluye ese atributo y mantuvo `Cuphead.exe` vivo aproximadamente 30 s. No demuestra causalidad ni estabilidad larga.

## Solución aplicada

No se marcó una solución definitiva. Se instaló v37 con `adb install -r -d` para permitir la comparación contra v38 sin desinstalar ni eliminar el payload.

## Resultado

Estado: reproducido con v38; aislamiento preliminar favorable a v37, pendiente de una prueba prolongada y de una publicación con versionCode incremental que retire `largeHeap`.

## Limitaciones pendientes

- N/R para FPS real en este intento.
- N/R para una correlación causal entre `largeHeap` y el acceso inválido.
- El Pixel mantiene de forma independiente el cierre `reason=3 (LOW_MEMORY)` documentado en [limitación 23](./23-pixel-low-memory-metrica-20260918.md).
- No se deben extrapolar los aproximadamente 30 s de v37 a estabilidad general.

## Referencias

- [Registro completo del crash](../ejecuciones/26-validacion-v38-cuatro-dispositivos/logs/lenovo-v38-crash.txt)
- [Aislamiento v37](../ejecuciones/26-validacion-v38-cuatro-dispositivos/logs/lenovo-v37-fallback.txt)
- [Matriz de validación](../ejecuciones/26-validacion-v38-cuatro-dispositivos/matriz.md)

## Ejecuciones asociadas

- [EXEC-026](../ejecuciones/26-validacion-v38-cuatro-dispositivos/matriz.md)
