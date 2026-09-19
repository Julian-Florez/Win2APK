# EXEC-027: variante BCn automática en Pixel 9a

## Identificación

- ID: `EXEC-027`
- Fecha: 2026-09-18
- Tipo: prueba de configuración gráfica aislada
- Objetivo: comparar el perfil Mali con la política BCn automática usada por el fork WinlatorMali, sin cambiar el payload ni el método de instalación.
- Dispositivo: Google Pixel 9a, serial `4A021JEBF06953`, Mali-G715, Android API 37.
- Base de comparación: v39, versionCode `39`, `largeHeap` retirado.

## Cambio aislado

| Parámetro | v39 | v40 |
|---|---|---|
| `BCN_COMPUTE_AUTO` | `0` | `1` |
| `BCN_QUALITY_PRESET` | `fast` | no forzado, queda `auto` en el fork |
| `WRAPPER_EMULATE_BCN` | `3` | `3` |
| `WRAPPER_USE_BCN_CACHE` | `1` | `1` |
| `BCN_DISABLE_DISK_CACHE` | `0` | `0` |
| DXVK | Sarek `1.12.1` | Sarek `1.12.1` |
| Resolución | `1280x720` | `1280x720` |
| Payload | `815` archivos, `5847372363` bytes | igual, esperado |

La selección se basa en la implementación pública de WinlatorMali, pero el código de esta prueba conserva Vortek + Gladio del proyecto. No se presenta como equivalente binario al fork.

## Resultado

| Campo | Valor |
|---|---|
| Build | Correcto, `3m40s` |
| Instalación | APK universal `273711050` bytes; Pixel `10014 ms` |
| Perfil observado | Esperado por el selector: Vortek + Gladio, DXVK-Sarek 1.12.1, Fcharan BCn automático; línea del selector no conservada en el corte final |
| Arranque de Cuphead | `Cuphead.exe` vivo en el primer corte |
| Memoria | Primer corte: PSS `2179056 KiB`, RSS `2243208 KiB`, Graphics `2104936 KiB` |
| CPU | N/R |
| FPS real | N/R |
| Cierre | `20:38:49.639`, `reason=3 (LOW_MEMORY)` |

## Criterio de decisión

- Mejoría: Cuphead.exe vivo más allá del umbral reproducido de aproximadamente 72 s, sin un error gráfico nuevo y con el marcador directo intacto.
- No mejoría: cierre por `LOW_MEMORY`, crash del juego, error de inicialización o alteración del payload.

## Evidencia

Los registros están en [build.md](./logs/build.md), [instalacion.md](./logs/instalacion.md) y [pixel-monitor.txt](./logs/pixel-monitor.txt). La evidencia de v39 está en [EXEC-026](../26-validacion-v38-cuatro-dispositivos/matriz.md).
