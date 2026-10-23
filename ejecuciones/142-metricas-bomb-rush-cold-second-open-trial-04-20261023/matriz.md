# EXEC-142: Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; intento 04 de 05; primer inicio y segunda apertura medidos durante cinco minutos

- **Run de métricas:** `RUN-20261023-063`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-04` | Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; intento 04 de 05; primer inicio y segunda apertura medidos durante cinco minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 66.981 s | 108.629 s | 1535 ms | 34195 ms | 54.286 | 764416.000 | title_screen | approved_experimental |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| pixel-9a | 300.000 s | 11963 ms | 1.000 | 0.983 | 54.083 | title_screen | approved_experimental |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-063); descripción: Se muestra el logotipo de Bomb Rush Cyberfunk centrado sobre ilustraciones estilizadas; no se distingue una invitación a continuar en esta captura..
- `pixel-9a`: [evidencias second-open](../../metricas/runs/RUN-20261023-063/second-open/); descripción: Se ve la pantalla de título de Bomb Rush Cyberfunk con el logotipo y las ilustraciones estilizadas; no se distingue la invitación a continuar en este fotograma..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-063)
