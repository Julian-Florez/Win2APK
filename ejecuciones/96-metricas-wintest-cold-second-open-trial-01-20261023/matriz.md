# EXEC-096: WinTest ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-017`
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
| Escenario | `wintest-cold-second-open-trial-01` | WinTest ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 32.448 s | 68.419 s | 1723 ms | 33402 ms | 0.267 | 125184.000 | other | approved_experimental |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| mi-a3 | 300.000 s | 12376 ms | 1.000 | 0.967 | 0.294 | other | approved_experimental |

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

- `mi-a3`: [evidencias frías](../../metricas/runs/RUN-20261023-017); descripción: En la captura T+60 se ve la consola de Win2APKTest.exe y una ventana Win2APK Test con Hola mundo y el botón Cambiar texto..
- `mi-a3`: [evidencias second-open](../../metricas/runs/RUN-20261023-017/second-open/); descripción: La captura muestra la consola Win2APKTest.exe y, en el centro, la ventana Win2APK Test con Hola mundo y el botón Cambiar texto. El fondo de pantalla restante es negro; la interfaz de la aplicación sí está visible..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-017)
