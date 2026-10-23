# EXEC-139: Instalación fresca de Cuphead en Pixel 9a; reemplazo de la repetición fría fuera de 300 s; primer inicio y segunda apertura medidos durante cinco minutos

- **Run de métricas:** `RUN-20261023-060`
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
| Escenario | `cuphead-cold-second-open-replacement-02` | Instalación fresca de Cuphead en Pixel 9a; reemplazo de la repetición fría fuera de 300 s; primer inicio y segunda apertura medidos durante cinco minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 181.632 s | 271.446 s | 1666 ms | 83190 ms | 53.200 | 1332615.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 13527 ms | 1.000 | 0.980 | 53.737 | title_screen | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-060); descripción: Pantalla predominantemente negra; en la zona inferior derecha aparece el texto «Cargando» junto a un indicador giratorio. La interfaz de título del juego aún no está visible..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-060/second-open/); descripción: Se ven Cuphead, Mugman y Ms. Chalice bajo el título CUPHEAD; en la parte inferior aparece «Press Any Button»..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-060)
