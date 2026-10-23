# EXEC-128: Repetición del ensayo 2 de WinTest en Pixel 9a tras desbloquear Play Protect; instalación fresca, primer inicio 5 minutos y segunda apertura 5 minutos

- **Run de métricas:** `RUN-20261023-049`
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
| Escenario | `wintest-cold-second-open-trial-02-retry-01` | Repetición del ensayo 2 de WinTest en Pixel 9a tras desbloquear Play Protect; instalación fresca, primer inicio 5 minutos y segunda apertura 5 minutos |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 34.076 s | 55.628 s | 3047 ms | 20155 ms | 0.758 | 248051.000 | other | approved_experimental |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 5901 ms | 1.000 | 0.983 | 4.547 | other | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-049); descripción: Sobre un fondo negro, en la zona inferior izquierda se ven una consola de Win2APK Test y una ventana Win32 blanca con Hola mundo y el botón Cambiar texto; la consola indica que espera interacción..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-049/second-open/); descripción: En el fondo negro, en la zona inferior izquierda se ven la consola de Win2APK Test y la ventana Win32 con Hola mundo y Cambiar texto; la consola indica que espera interacción..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-049)
