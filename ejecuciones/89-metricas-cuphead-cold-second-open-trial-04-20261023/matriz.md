# EXEC-089: Cuphead ensayo 4 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-010`
- **Fecha:** 2026-10-23
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/cuphead/cuphead-11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core.apks` | Archivo medido |
| SHA-256 | `b143bfdfa9ed56d760a921c70fc5bd287f3b533da29bab5d1939732e8a249489` | Calculado antes de instalar |
| Escenario | `cuphead-cold-second-open-trial-04` | Cuphead ensayo 4 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 209.892 s | 386.736 s | 2568 ms | 167791 ms | 40.156 | 197981.000 | loading | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-010); descripción: Pantalla de carga de Cuphead: fondo negro, texto Cargando en la esquina inferior derecha e indicador de carga; barra de estado y navegación de Android visibles..

## Segunda apertura (sin reinstalación)

Fase completa de 301.685 s y 266 muestras. App y Cuphead.exe permanecieron activos al cierre; primer proceso a 1.290 s, proceso del juego a 14.078 s y primer frame observado a 14.541 s. FPS medio registrado: 50.694. La captura T+60 fue revisada de forma independiente: pantalla de título con logotipo CUPHEAD y Cuphead, Mugman y Ms. Chalice, sin instrucción visible para continuar. Clasificación `title_screen`, revisión confirmada; resultado `approved_experimental` para esta apertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-010/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `2b55b02bc59b46ae8fef0460c24100d2699fc57cd68846a7f0bc84876dea46a1`. CSV, eventos y logs de segunda apertura están en [second-open](../../metricas/runs/RUN-20261023-010/second-open/); validación: OK, 266 muestras. La fase fría quedó en `loading` a T+60 y es parcial; la reapertura llegó a `title_screen`. Las fases se conservan separadas, sin promediar sus métricas.

Durante la instalación bundletool reportó: `Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules. If you see legacy versions of dynamic feature modules installed try to uninstall and install the app again.` La instalación se registró como exitosa; advertencia original conservada en `logs/lenovo-tb-j606f/install-apks.log`.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-010)
