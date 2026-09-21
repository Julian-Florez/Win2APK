# EXEC-066: Reproducción del posible crash de Unity de Bomb Rush Cyberfunk en Lenovo TB-J606F

- **Run de métricas:** `RUN-20260921-001`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, ejecución preinstalada y medición temporal
- **Resultado general:** ventana del Unity Crash Handler reproducida; consultar resultados por dispositivo
- **Método:** `preinstalled`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-unified-loading-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `ae02fdcbf7324be6e15fd0d63a4487930fd6e043ad4e8cf486d93cad6d7484e9` | Calculado antes de instalar |
| Escenario | `bomb-rush-unity-crash-repro` | Reproducción del posible crash de Unity de Bomb Rush Cyberfunk en Lenovo TB-J606F |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 180 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | N/A: preinstalada | N/R s | N/R s | 1796 ms | 1796 ms | 0.857 | 115204.000 | error_screen | reproducido; procesos vivos |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica. La
instalación no se midió porque el modo fue `preinstalled`; el estado
`failed_install` que aparece en el CSV es una limitación del agregador ya
documentada y no evidencia un fallo de instalación en esta ejecución.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

Revisar `resumen.csv`, los logs y la clasificación visual antes de aceptar o
descartar una configuración para otra familia de dispositivos.

## Evidencias

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260921-001); descripción: Ventana del Unity crash handler superpuesta al título de Bomb Rush Cyberfunk; el proceso del juego permaneció activo durante la observación..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-001)
