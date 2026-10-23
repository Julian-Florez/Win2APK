# EXEC-143: Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; siguiente repetición tras RUN-063 para completar la serie de cinco parejas frías y segundas aperturas; cada fase observada durante cinco minutos

- **Run de métricas:** `RUN-20261023-064`
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
| Escenario | `bomb-rush-cold-second-open-trial-05` | Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; siguiente repetición tras RUN-063 para completar la serie de cinco parejas frías y segundas aperturas; cada fase observada durante cinco minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 69.088 s | 120.992 s | 1554 ms | 43194 ms | 53.359 | 755714.000 | other | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 16637 ms | 1.000 | 0.977 | 54.194 | title_screen | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-064); descripción: La pantalla muestra un fondo blanco con el logotipo y texto «TEAM REPTILE» centrados; no aparecen el título de Bomb Rush ni controles del juego..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-064/second-open/); descripción: Se ve el logotipo de Bomb Rush Cyberfunk sobre ilustraciones y el texto «PRESS ANY KEY» en la parte inferior..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-064)
