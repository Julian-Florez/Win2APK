# EXEC-088: Cuphead ensayo 3 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-009`
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
| Escenario | `cuphead-cold-second-open-trial-03` | Cuphead ensayo 3 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 209.247 s | 389.347 s | 2203 ms | 169163 ms | 38.695 | 195762.000 | loading | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-009); descripción: El PNG T+60 de Cuphead trial-03 muestra carga con texto Cargando e indicador circular en la parte inferior derecha, sobre fondo oscuro..

## Segunda apertura (sin reinstalación)

Fase completa de 300.162 s, 265 muestras. App y proceso Cuphead.exe estuvieron activos al cierre; primer proceso a 2.053 s, proceso del juego a 16.112 s y primer frame observado a 19.233 s. FPS medio registrado: 48.260. La captura T+60 fue revisada independientemente: pantalla de título con logotipo CUPHEAD y Cuphead, Mugman y Ms. Chalice; sin instrucción visible para continuar. Clasificación `title_screen`, revisión confirmada; resultado `approved_experimental` para esta apertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-009/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `eed595386911196a9ef2115d5bbda4685a2027b0bd41bd57b51f9c19b353ef3f`. CSV, eventos y logs de esta fase están en [second-open](../../metricas/runs/RUN-20261023-009/second-open/); validación: OK, 265 muestras. La fase fría permaneció en `loading` a T+60 y es parcial; la reapertura alcanzó `title_screen`. No se promedian ni mezclan las dos fases.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-009)
