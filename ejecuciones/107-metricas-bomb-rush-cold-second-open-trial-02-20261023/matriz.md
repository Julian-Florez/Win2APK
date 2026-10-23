# EXEC-107: Bomb Rush Cyberfunk ensayo 2 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-028`
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
| Escenario | `bomb-rush-cold-second-open-trial-02` | Bomb Rush Cyberfunk ensayo 2 en Xiaomi Mi A3: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 74.760 s | 151.007 s | 2370 ms | 72532 ms | 24.479 | 143274.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| mi-a3 | 300.000 s | 9503 ms | 1.000 | 0.970 | 25.726 | title_screen | approved_experimental |

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

- `mi-a3`: [evidencias frías](../../metricas/runs/RUN-20261023-028); descripción: La captura T+60 muestra el cuadro Starting up... con indicador circular sobre fondo negro durante la preparación inicial de Winlator..
- `mi-a3`: [evidencias second-open](../../metricas/runs/RUN-20261023-028/second-open/); descripción: Se observa el logotipo de Bomb Rush Cyberfunk y el texto PRESS ANY KEY en la pantalla de título; app y juego estuvieron activos durante los 300 s..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-028)
