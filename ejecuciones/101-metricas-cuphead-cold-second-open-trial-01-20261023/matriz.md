# EXEC-101: Cuphead ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-022`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/cuphead/cuphead-11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core.apks` | Archivo medido |
| SHA-256 | `b143bfdfa9ed56d760a921c70fc5bd287f3b533da29bab5d1939732e8a249489` | Calculado antes de instalar |
| Escenario | `cuphead-cold-second-open-trial-01` | Cuphead ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 190.300 s | 358.005 s | 1572 ms | 165124 ms | 42.117 | 142946.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| mi-a3 | 300.000 s | 12483 ms | 1.000 | 0.967 | 50.206 | title_screen | approved_experimental |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

Revisar `resumen.csv`, los logs y la clasificación visual antes de aceptar o
descartar una configuración para otra familia de dispositivos.

## Evidencias

- `mi-a3`: [evidencias frías](../../metricas/runs/RUN-20261023-022); descripción: La captura T+60 muestra pantalla mayormente negra de carga de Cuphead, el texto Cargando y un indicador circular abajo a la derecha; también están visibles las barras de estado y navegación de Android..
- `mi-a3`: [evidencias second-open](../../metricas/runs/RUN-20261023-022/second-open/); descripción: La captura muestra la pantalla de título de Cuphead con Cuphead, Mugman y Ms. Chalice, el logotipo CUPHEAD y el texto Press Any Button..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-022)
