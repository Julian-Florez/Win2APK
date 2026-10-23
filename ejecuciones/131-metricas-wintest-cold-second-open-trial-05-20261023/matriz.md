# EXEC-131: Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 05 de 05

- **Run de métricas:** `RUN-20261023-052`
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
| Escenario | `wintest-cold-second-open-trial-05` | Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 05 de 05 |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 30.082 s | 47.109 s | 1756 ms | 15159 ms | 0.144 | 260535.000 | other | approved_experimental |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 6672 ms | 1.000 | 0.983 | 0.037 | other | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-052); descripción: Se ven dos ventanas Win32 de Win2APK Test sobre fondo negro: consola de diagnóstico y ventana con “Hola mundo” y el botón “Cambiar texto”; no es una pantalla de título ni gameplay..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-052/second-open/); descripción: Dos ventanas Win32 de Win2APK Test en pantalla: consola de diagnóstico y ventana “Hola mundo” con el botón “Cambiar texto”; ambas visibles durante la segunda apertura..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-052)
