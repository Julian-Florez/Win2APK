# EXEC-141: Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; intento válido 03 de 05; primer inicio y segunda apertura medidos durante cinco minutos

- **Run de métricas:** `RUN-20261023-062`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-03` | Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; intento válido 03 de 05; primer inicio y segunda apertura medidos durante cinco minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 68.070 s | 117.011 s | 1950 ms | 40200 ms | 53.964 | 749136.000 | black_screen | failed_visual_state |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 17654 ms | 1.000 | 0.977 | 53.751 | title_screen | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-062); descripción: La captura T+60 permanece negra; no se distingue interfaz, texto ni contenido identificable del juego, salvo el cursor blanco en la esquina superior izquierda..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-062/second-open/); descripción: Se ve el logotipo de Bomb Rush Cyberfunk sobre ilustraciones estilizadas; no se distingue el texto de invitación a continuar en este fotograma..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-062)
