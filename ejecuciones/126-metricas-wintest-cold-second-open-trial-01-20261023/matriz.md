# EXEC-126: Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos

- **Run de métricas:** `RUN-20261023-047`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `org.win2apk.testapp` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/wintest/win2apk-test-0.1.0.apks` | Archivo medido |
| SHA-256 | `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1` | Calculado antes de instalar |
| Escenario | `wintest-cold-second-open-trial-01` | Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 60.308 s | 78.235 s | 1847 ms | 16204 ms | 0.274 | 345910.000 | other | approved_experimental |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 5920 ms | 1.000 | 0.987 | 0.132 | other | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-047); descripción: Se observan dos ventanas Win32 de Win2APK Test: una consola con datos de ejecución y una ventana blanca con el texto Hola mundo y el botón Cambiar texto..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-047/second-open/); descripción: Se observan dos ventanas Win32 de Win2APK Test: una consola con datos de ejecución y una ventana blanca con el texto Hola mundo y el botón Cambiar texto..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-047)
