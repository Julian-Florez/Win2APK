# EXEC-106: Bomb Rush Cyberfunk ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-027`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-01` | Bomb Rush Cyberfunk ensayo 1 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 83.177 s | 160.923 s | 2207 ms | 72543 ms | 45.226 | 143772.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| mi-a3 | 300.000 s | 12487 ms | 1.000 | 0.970 | 49.686 | title_screen | approved_experimental |

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

- `mi-a3`: [evidencias frías](../../metricas/runs/RUN-20261023-027); descripción: La captura T+60 muestra el cuadro Starting up... con un indicador circular sobre fondo negro, señal de que Winlator sigue preparando el arranque..
- `mi-a3`: [evidencias second-open](../../metricas/runs/RUN-20261023-027/second-open/); descripción: Se observa el logotipo de Bomb Rush Cyberfunk y el texto PRESS ANY KEY sobre la pantalla de título; el juego permaneció activo durante la medición..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-027)
