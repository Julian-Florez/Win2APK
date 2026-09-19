# Investigación de forks, BCn y DXVK-Sarek para Pixel Tensor/Mali

- **Versión de plantilla:** 1.0
- **ID:** `EXEC-024`
- **Fecha:** `2026-09-18`
- **Tipo:** investigación de componentes, compilación y prueba en dispositivo
- **Resultado general:** en investigación
- **Objetivo:** comprobar si una capa BCn por compute shader y una variante DXVK-Sarek reducen el cierre por memoria y el fallo de inicialización observados en el Pixel 9a, sin modificar el perfil automático de los tres dispositivos Adreno.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead empaquetado con entorno de compatibilidad (`com.cuphead`) | Rama `codex/no-duplicate-game-data` |
| Versión previa observada | `versionCode=34`, `11.1-direct-files-auto-gpu-recovery-v4` | Paquete instalado en Pixel antes de esta ejecución |
| Ejecutable | `C:\\Cuphead\\Cuphead.exe` | Prefijo existente, instalación directa validada |
| Dispositivos | Pixel 9a; Lenovo TB-J606F; Redmi Note 8; Xiaomi Mi A3 | ADB por USB o red según dispositivo |
| Pixel | Mali-G715 / Tensor, API 37 | Renderer consultado durante la ejecución previa |
| Adreno de referencia | Adreno 610 / Qualcomm en Lenovo, Redmi y Mi A3 | Perfil Turnip + Gladio |
| Perfil previo Pixel | Vortek 2.1 + Gladio 1.0 + DXVK 1.10.3; `800x450` | N/R; el archivo histórico no quedó exportado en esta ejecución |
| Componentes investigados | CMOD; `bcn_layer` shader-v3; DXVK-Sarek | Fuentes externas registradas en `logs/fuentes.md` |
| Regla de almacenamiento | No reinstalar ni copiar el payload de Cuphead; conservar el árbol directo ya movido | Marcador y conteo de 815 archivos |

## Hipótesis y variantes

| ID | Variante | Estado | Resultado observado | Decisión |
|---|---|---|---|---|
| F-01 | Vortek + DXVK 1.10.3 sin BCn, `800x450` | Ejecutada antes de EXEC-024 | El Pixel terminó con `am_low_memory` y cierre del proceso | Control negativo; no repetir salvo restauración |
| F-02 | Vortek + WineD3D, `800x450` | Ejecutada antes de EXEC-024 | `Failed to initialize player` / `InitializeEngineGraphics failed` | Descartada para Cuphead |
| F-03 | Vortek + DXVK-Sarek 1.11.1 + capa BCn shader-v3 + ETC2 | Ejecutada | Inició `Cuphead.exe`; cierre Android por `reason=3 (LOW_MEMORY)` a los ~71 s | No aprobada como perfil estable; pasa a comparación con F-04 |
| F-04 | Vortek + DXVK-Sarek 1.12.1 + `leegao_bcn.tzst` Fcharan/WinMali-Dev + ETC2 | En preparación | N/R | Siguiente variante para Pixel; conserva la ruta Adreno sin BCn |
| F-05 | F-04 + `android:largeHeap=true` | En preparación | N/R | Aísla el límite de memoria del proceso sin cambiar la ruta gráfica |
| F-05 | Perfil automático Adreno sin BCn | Pendiente de verificación tras la actualización | N/R | Debe conservarse como referencia estable |

## Revisiones experimentales posteriores

Las filas F-04 y F-05 fueron hipótesis de la planificación original. Las ejecuciones posteriores conservaron cada resultado como una observación independiente:

| Publicación | Cambio | Resultado | Registro |
|---|---|---|---|
| v36 | Fcharan BCn + DXVK-Sarek 1.12.1 | Pixel inició, pero terminó por `LOW_MEMORY` cerca de 71 s | [EXEC-024, monitor histórico](./logs/pixel-monitor.txt) |
| v37 | v36 con caché BCn y preset `fast` | Pixel terminó por `LOW_MEMORY` cerca de 71 s | [EXEC-024 histórico](./logs/pixel-monitor.txt) |
| v38 | v37 + `android:largeHeap=true` | Pixel terminó por `LOW_MEMORY` a las 20:11:40.028; Lenovo produjo después un crash Unity | [EXEC-026](../26-validacion-v38-cuatro-dispositivos/matriz.md) |
| v39 | v37 sin `largeHeap` | Pixel terminó por `LOW_MEMORY` a las 20:32:10.069; Lenovo conservó Cuphead.exe en el corte | [EXEC-026](../26-validacion-v38-cuatro-dispositivos/matriz.md) |
| v40 | BCn automático, `BCN_COMPUTE_AUTO=1`, calidad `auto` | Menor memoria inicial, pero `LOW_MEMORY` a las 20:38:49.639 | [EXEC-027](../27-variante-bcn-auto-pixel/matriz.md) |
| v41 | DXVK 2.4.1 + BCn automático | Cuatro dispositivos conservaron `Cuphead.exe` en el corte de 20:48:38; validación prolongada pendiente | [EXEC-028](../28-dxvk241-pixel/matriz.md) |

Las conclusiones de estas revisiones no reemplazan las métricas históricas de F-03. Cada cambio de publicación tiene su propia evidencia y no se usa para recalcular retrospectivamente una medición anterior.

## Métricas

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia |
|---|---|---|---|---|---|
| M-01 | Compilación del AAB | Aprobado | 3 min 44 s; 5,469,774,837 bytes | `:app:bundleDebug` | `logs/build.md` |
| M-02 | Instalación o actualización | Aprobado | 10,034 ms; APK base por USB | No se reinstaló el payload | `logs/install.md` |
| M-03 | Tiempo hasta actividad | Aprobado | `TotalTime=312 ms` | `am start -W`; no equivale a gameplay | `logs/pixel-monitor.txt` |
| M-04 | Tiempo hasta gameplay | N/R | El proceso llegó a iniciar, pero no se cronometró una escena jugable | Control físico no conectado durante la muestra | `logs/pixel-monitor.txt` |
| M-05 | Permanencia del proceso | Fallido | Vivo a ~20 s; muerto antes de ~60 s | Muestra posterior con `LOW_MEMORY` | `logs/pixel-monitor.txt` |
| M-06 | Motivo de salida | Fallido | `reason=3 (LOW_MEMORY)` | `dumpsys activity exit-info` | `logs/pixel-monitor.txt` |
| M-07 | Memoria del proceso y del sistema | Parcial | Graphics 2,171,480 kB; PSS 2,258,660 kB; RSS 2,348,008 kB | Muestra ~20 s; no es pico máximo | `logs/pixel-monitor.txt` |
| M-08 | FPS o framerate | N/R | N/R | HUD o medición disponible; no inferir FPS por sensación | `logs/pixel-fps.txt` |
| M-09 | Integridad del payload directo | Aprobado | 815 archivos y 5847372363 bytes; marcador | No se copió durante F-03 | `logs/payload.txt` |
| M-10 | Regresión en Adreno | N/R | N/R | Lenovo, Redmi y Mi A3 con perfil automático | `logs/adreno-regression.txt` |

## Resultados por dispositivo

| Dispositivo | Variante | Instalación | Primer inicio | Juego | FPS | RAM/CPU | Salida | Estado |
|---|---|---|---|---|---|---|---|
| Pixel 9a | F-03 | N/R | N/R | N/R | N/R | N/R | N/R | Pendiente |
| Lenovo TB-J606F | F-05 | N/R | N/R | N/R | N/R | N/R | N/R | Pendiente |
| Redmi Note 8 | F-05 | N/R | N/R | N/R | N/R | N/R | N/R | Pendiente |
| Xiaomi Mi A3 | F-05 | N/R | N/R | N/R | N/R | N/R | N/R | Pendiente |

## Evidencias

- [Fuentes, versiones y hashes](./logs/fuentes.md)
- [Build](./logs/build.md)
- [Instalación](./logs/install.md)
- [Payload directo](./logs/payload.txt)
- [Monitorización Pixel](./logs/pixel-monitor.txt)
- La memoria está integrada en [Monitorización Pixel](./logs/pixel-monitor.txt)
- [FPS Pixel](./logs/pixel-fps.txt)
- [Regresión Adreno](./logs/adreno-regression.txt)

## Criterios de interpretación

- Un proceso vivo durante una muestra no equivale a estabilidad de larga duración.
- Un cierre sin `ApplicationExitInfo` nuevo se registra como motivo no determinado, aunque existan señales de `am_low_memory`.
- Los valores de FPS, RAM y CPU sólo se comparan entre muestras con la misma escena y resolución; de lo contrario se mantienen separados.
- El resultado de Pixel no se extrapola automáticamente a otros dispositivos Mali o a otras versiones de Android.

## Fallos asociados

- [Limitación 23: cierre del Pixel por `LOW_MEMORY`](../../limitaciones/23-pixel-low-memory-metrica-20260918.md).
- [Limitación 24: WineD3D no inicializa Cuphead](../../limitaciones/24-wined3d-no-inicializa-cuphead-pixel.md).

Mensaje exacto de F-02:

```text
Failed to initialize player
Failed to initialize graphics.
Make sure you have DirectX 11 installed, have up to date drivers for your graphics card and have not disabled 3D acceleration in display settings.
InitializeEngineGraphics failed
```
