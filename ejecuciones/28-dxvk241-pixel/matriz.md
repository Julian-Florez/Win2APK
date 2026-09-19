# EXEC-028: DXVK 2.4.1 con BCn automático en Pixel 9a

## Identificación

- ID: `EXEC-028`
- Fecha: 2026-09-18
- Tipo: prueba de compatibilidad de versión DXVK
- Objetivo: probar una versión DXVK distinta sobre el perfil Mali que ya inicia Cuphead, conservando BCn automático y el payload directo.
- Dispositivo inicial: Google Pixel 9a, serial `4A021JEBF06953`, Mali-G715, Android API 37.
- Base: v40, con Vortek + Gladio, BCn automático, sin `largeHeap` y resolución `1280x720`.

## Cambio aislado

| Parámetro | v40 | v41 |
|---|---|---|
| DXVK | Sarek `1.12.1` | `2.4.1` |
| BCn compute | automático | automático |
| Capa BCn | Fcharan `5c168f4` | igual |
| Driver | Vortek + Gladio | igual |
| Memoria Vortek | `maxDeviceMemory=1024` | igual |
| Payload | `815` archivos, `5847372363` bytes | igual, esperado |

## Criterio

- Mejoría: Cuphead.exe vivo más allá de aproximadamente 72 s y sin error de inicialización.
- No mejoría: `LOW_MEMORY`, crash de Unity, error WineD3D o ausencia de texturas.

## Resultado del Pixel

| Campo | Valor |
|---|---|
| Build | Correcto, `3m43s` |
| APK e instalación | Universal base-only `273711050` bytes; instalación Pixel `11136 ms` |
| Perfil | `Mali/unknown / Vortek + Gladio / DXVK 2.4.1 + Fcharan BCn ETC2 auto` |
| Memoria | Corte final: PSS `555304 KiB`, RSS `681212 KiB`, Graphics `475084 KiB` |
| CPU | Corte `top`: com.cuphead `418%`, Cuphead.exe `45.4%` |
| FPS real | N/R |
| Cierre | No observado en la ventana de aproximadamente 11 minutos; continuó vivo tras retirar `local_testing` |

## Validación de los cuatro dispositivos

La misma universal v41 se instaló mediante `adb install -r` en los otros tres dispositivos. En el corte final `2026-09-18T20:48:38-05:00`, los cuatro conservaron `com.cuphead` y `Cuphead.exe` vivos.

| Dispositivo | Instalación | Perfil | Procesos en corte | PSS / RSS | CPU instantánea de `top` | RAM disponible | Payload |
|---|---:|---|---|---:|---|---:|---|
| Pixel 9a | `11136 ms` | Mali-G715, Vortek + Gladio, DXVK 2.4.1 + Fcharan BCn auto | `10432 / 10654` | `553148 / 677420 KiB` en corte final posterior a limpieza | app `421%`, juego `45.4%` | `N/R` | `815 / 5847372363`; `local_testing` ausente |
| Lenovo TB-J606F | `21846 ms` | Adreno 610, Turnip + Gladio, DXVK | `13602 / 13739` | `127368 / 184996 KiB` | app `20.0%`, juego `206%` | `N/R` | `815 / 5847372363` |
| Redmi Note 8 | `13301 ms` | Adreno 610, Turnip + Gladio, DXVK | `21986 / 22112` | `125078 / 193868 KiB` | app `19.3%`, juego `196%` | `N/R` | `815 / 5847372363` |
| Xiaomi Mi A3 | `10656 ms` | Adreno 610, Turnip + Gladio, DXVK | `27653 / 27770` | `98929 / 158592 KiB` | app `20.0%`, juego `186%` | `N/R` | `815 / 5847372363` |

Los porcentajes de CPU son una instantánea de `top`, no un promedio. El FPS real queda `N/R` porque no se capturó el HUD de DXVK ni una medición de frames del juego.

## Corrección posterior por validación visual

Después del corte basado en procesos, el usuario informó que el Pixel mostraba una pantalla completamente negra. Una captura ADB posterior confirmó que `XServerDisplayActivity` y `Cuphead.exe` seguían vivos, pero el SurfaceView no presentaba contenido visible. Por tanto, el criterio inicial era insuficiente: v41 mejora la memoria y evita el cierre observado, pero **no aprueba la ejecución funcional en el Pixel**. El diagnóstico y la prueba correctiva se trasladan a [EXEC-029](../29-pantalla-negra-dxvk241-pixel/matriz.md).

## Decisión revisada

v41 queda descartada como publicación para Pixel por fallo de presentación. Sus métricas de memoria se conservan porque sirven para comparar versiones DXVK, pero no se interpretan como éxito de gameplay.

## Evidencia

Los registros están en [build.md](./logs/build.md), [instalacion-cuatro-dispositivos.md](./logs/instalacion-cuatro-dispositivos.md), [pixel-v41-monitor.txt](./logs/pixel-v41-monitor.txt) y [storage-dedup.md](./logs/storage-dedup.md). Las variantes comparadas están en [EXEC-026](../26-validacion-v38-cuatro-dispositivos/matriz.md) y [EXEC-027](../27-variante-bcn-auto-pixel/matriz.md).
