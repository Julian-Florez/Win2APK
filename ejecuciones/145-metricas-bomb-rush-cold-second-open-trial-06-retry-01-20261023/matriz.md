# EXEC-145: Intento para completar la quinta pareja de instalación fría y segunda apertura de Bomb Rush en Pixel 9a, tras el fallo de metadatos de RUN-065.

- **Run de métricas:** `RUN-20261023-066`
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
| Escenario | `bomb-rush-cold-second-open-trial-06-retry-01` | Intento para completar la quinta pareja de instalación fría y segunda apertura de Bomb Rush en Pixel 9a, tras el fallo de metadatos de RUN-065. |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 67.629 s | 109.490 s | 1797 ms | 34253 ms | 53.976 | 745516.000 | other | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 11933 ms | 1.000 | 0.983 | 54.371 | other | partial |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas.

En la segunda apertura, una captura complementaria tomada aproximadamente a
T+382 s (después de concluir el monitor de 300 s) todavía muestra el mismo
logotipo, sin la invitación a comenzar. La captura no reemplaza la T+60 ni
modifica sus métricas. La app y el proceso del juego seguían activos al terminar.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

Las métricas temporales y de muestreo de ambas fases son utilizables: cada una
registró 301 muestras y un primer frame dentro de 300 s. La pareja queda
`partial`, no aprobada como llegada al título: las capturas T+60 de frío y
second-open y la captura suplementaria posterior muestran el mismo logotipo sin
invitación a comenzar. No se atribuye la persistencia a la temperatura sin una
prueba que aísle esa variable.

## Evidencias

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-066); descripción: La pantalla muestra el logotipo de Bomb Rush Cyberfunk centrado sobre ilustraciones verdes, blancas y negras; no se ve una invitación a comenzar ni un indicador de carga..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-066/second-open/); descripción: La pantalla muestra el logotipo de Bomb Rush Cyberfunk centrado sobre ilustraciones verdes, blancas y negras; no se ve una invitación a comenzar ni un indicador de carga..
- Captura complementaria posterior al monitor: [post-monitor-382s.png](../../metricas/runs/RUN-20261023-066/second-open/screenshots/pixel-9a/post-monitor-382s.png); no sustituye T+60.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-066)
