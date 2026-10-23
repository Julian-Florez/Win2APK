# EXEC-136: Instalación fresca de Cuphead en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 05 de 05

- **Run de métricas:** `RUN-20261023-057`
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
| Escenario | `cuphead-cold-second-open-trial-05` | Instalación fresca de Cuphead en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 05 de 05 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 185.338 s | 295.195 s | 1820 ms | 103200 ms | 53.797 | 1328658.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 13575 ms | 1.000 | 0.980 | 53.804 | title_screen | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-057); descripción: Pantalla de carga de Winlator/Cuphead con fondo negro, texto “Cargando” e indicador circular; aún no se ve el menú ni gameplay..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-057/second-open/); descripción: Pantalla de título de Cuphead con logotipo, Cuphead, Mugman y Chalice; texto “Press Any Button”..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-057)
