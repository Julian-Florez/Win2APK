# Decisión experimental de perfil DXVK 2.4.1 para Mali y Adreno

- **Fecha:** 2026-09-18
- **Estado:** revisada; v41 descartada en Pixel por pantalla negra
- **Propósito:** consolidar la investigación de forks, capas BCn y versiones DXVK en el Pixel 9a y verificar que el selector automático conserva el camino funcional de los tres dispositivos Adreno.

## Problema

El Pixel 9a usa Mali-G715 sobre Tensor G4. Las variantes iniciales con Vortek, Gladio y DXVK-Sarek iniciaban Cuphead, pero el proceso Android terminaba aproximadamente a los 70 a 72 s con `reason=3 (LOW_MEMORY)`. WineD3D no inicializó los gráficos y `largeHeap` no corrigió el cierre. Además, una publicación con `largeHeap` produjo un crash de Unity en Lenovo.

## Investigación de forks y componentes

Se revisaron CMOD, WinlatorMali, Bannerlator, `bcn_layer` de leegao y DXVK-Sarek. La evidencia pública converge en tres ideas, con alcance comunitario y no como garantía de compatibilidad:

- Mali necesita una estrategia explícita para texturas BCn porque el camino de Vulkan no ofrece el mismo soporte que Adreno.
- La familia Vortek y las capas BCn de compute son rutas habituales para D3D11 en Mali.
- WinlatorMali expone perfiles automáticos de BCn, caché y transcodificación, mientras versiones DXVK distintas pueden cambiar de forma importante el consumo de memoria.

Fuentes consultadas:

- [Winlator-CMOD releases](https://github.com/Stredohori/Winlator-CMOD/releases)
- [WinlatorMali releases](https://github.com/GunaCharanTeja/WinlatorMali/releases)
- [Bannerlator graphics wrappers guide](https://github.com/The412Banner/Bannerlator/blob/main/docs/graphics-wrappers-guide.md)
- [leegao Vortek internals](https://leegao.github.io/winlator-internals/2025/06/02/Vortek2.html)
- [DXVK-Sarek releases](https://github.com/zeyadadev/DXVK-Sarek/releases)
- [Winlator Internals, WSI en Mali](https://leegao.github.io/winlator-internals/wrapper/2026/07/28/wsi-woes-mali.html)

Las páginas de Reddit sobre Pixel 9a se trataron como evidencia anecdótica de configuración, no como validación experimental del proyecto.

## Decisión inicial

La publicación v41 se seleccionó inicialmente como candidata del perfil automático:

| GPU detectada | Perfil |
|---|---|
| Adreno / Qualcomm | Turnip 26.1.0 + Gladio 1.0 + DXVK, resolución `1280x720` |
| Mali o renderer desconocido | Vortek 2.1 + Gladio 1.0 + DXVK 2.4.1, capa BCn Fcharan, transcodificación ETC2, BCn automático, caché activada, `maxDeviceMemory=1024`, resolución `1280x720` |

La decisión excluyó `android:largeHeap=true`. El selector se basa en renderer, vendor y hardware, y no modifica el payload del juego. El payload directo permaneció en `815` archivos y `5847372363` bytes. En el Pixel se eliminó el staging `local_testing` de `5980480 KiB`; el proceso continuó vivo y se conservó la estrategia de una sola copia observada en ese dispositivo.

## Evidencia experimental

En el corte final de [EXEC-028](../ejecuciones/28-dxvk241-pixel/matriz.md), los cuatro dispositivos conservaron `com.cuphead` y `Cuphead.exe`:

| Dispositivo | Ventana observada disponible | PSS / RSS en el corte | Resultado |
|---|---:|---:|---|
| Pixel 9a | aproximadamente 11 min | `553148 / 677420 KiB` | sin nuevo `LOW_MEMORY`, incluso después de retirar `local_testing` |
| Lenovo TB-J606F | aproximadamente 9 min | `127368 / 184996 KiB` | Cuphead.exe vivo |
| Redmi Note 8 | aproximadamente 9 min | `125078 / 193868 KiB` | Cuphead.exe vivo |
| Xiaomi Mi A3 | aproximadamente 9 min | `98929 / 158592 KiB` | Cuphead.exe vivo |

El FPS real no fue medido. Los porcentajes de CPU registrados son instantáneas de `top`, no promedios.

## Revisión por pantalla negra

La validación visual posterior encontró que el Pixel presentaba un cuadro completamente negro aunque `com.cuphead` y `Cuphead.exe` siguieran vivos. El `output_log.txt` de Unity registró D3D11 y `Renderer: Vortek (Mali-G715)`, sin un error fatal, de modo que la observación de procesos y memoria no demuestra presentación correcta. v41 queda descartada para el Pixel y la sustitución de DXVK se prueba en [EXEC-029](../ejecuciones/29-pantalla-negra-dxvk241-pixel/matriz.md). La limpieza de `local_testing` permanece válida y no se revierte.

## Errores conservados

- WineD3D: `Failed to initialize player`, `Failed to initialize graphics` y `InitializeEngineGraphics failed` en Pixel.
- DXVK-Sarek 1.11.1 y 1.12.1: `reason=3 (LOW_MEMORY)` en Pixel.
- BCn automático con Sarek: menor memoria inicial, pero nuevo `LOW_MEMORY` en Pixel.
- `largeHeap`: no resolvió Pixel y v38 produjo `UnityPlayer.dll caused an Access Violation (0xc0000005)` en Lenovo.

Estos errores no se eliminan del historial. Están enlazados en [limitaciones/23](../limitaciones/23-pixel-low-memory-metrica-20260918.md), [limitaciones/24](../limitaciones/24-wined3d-no-inicializa-cuphead-pixel.md) y [limitaciones/25](../limitaciones/25-crash-unity-lenovo-v38.md).

La evidencia de limpieza de staging está en [storage-dedup.md](../ejecuciones/28-dxvk241-pixel/logs/storage-dedup.md).

## Decisiones pendientes revisadas

- Probar una versión DXVK compatible con Mali y exigir captura visible antes de medir estabilidad.
- Capturar FPS real mediante HUD de DXVK o una métrica de frames verificable.
- No recuperar v41 como candidata mientras el fallo de presentación siga reproducible.
- No presentar el perfil como válido para todas las GPU Mali o todas las versiones de Android.
