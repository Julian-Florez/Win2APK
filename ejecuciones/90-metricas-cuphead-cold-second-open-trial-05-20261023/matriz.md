# EXEC-090: Cuphead ensayo 5 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-011`
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
| Escenario | `cuphead-cold-second-open-trial-05` | Cuphead ensayo 5 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 205.814 s | 382.821 s | 7291 ms | 170168 ms | 39.537 | 299768.000 | loading | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-011); descripción: Pantalla de carga de Cuphead: fondo negro, texto Cargando en la esquina inferior derecha e indicador circular; barra de estado y navegación de Android visibles..

## Segunda apertura (sin reinstalación)

Fase completa de 302.957 s y 261 muestras. App y Cuphead.exe activos al cierre; primer proceso a 2.020 s, proceso del juego a 11.312 s y primer frame observado a 14.918 s. FPS medio registrado: 50.253. La captura T+60 muestra el logotipo CUPHEAD y a Cuphead, Mugman y Ms. Chalice; no se ve instrucción para continuar. Clasificación `title_screen`, revisión confirmada; resultado `approved_experimental` para esta apertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-011/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `d2c42583a6a8a08860725758d82e4dd2a4750a27e00508c6e94676ac1d53b6c4`. CSV, eventos y logs en [second-open](../../metricas/runs/RUN-20261023-011/second-open/); validación OK, 261 muestras. La fase fría quedó en `loading`, con primer frame a 173.666 s; la reapertura alcanzó `title_screen`. Fases resumidas por separado.

Con este ensayo queda completado el conteo de **5/5 parejas válidas Cuphead en Lenovo TB-J606F**. RUN-001 se mantiene excluido por fallo de infraestructura de instalación; no se cuenta entre las cinco parejas válidas.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-011)
