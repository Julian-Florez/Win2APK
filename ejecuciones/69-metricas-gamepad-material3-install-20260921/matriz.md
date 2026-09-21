# EXEC-069: Instalación y arranque de Bomb Rush Cyberfunk con gamepad Material You 3 sin cambiar posiciones

- **Run de métricas:** `RUN-20260921-004`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-gamepad-material3-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `de94b1c8e0865400203261c1c545cf49cbd628263430c06983e94986dd7ab433` | Calculado antes de instalar |
| Escenario | `gamepad-material3-install` | Instalación y arranque de Bomb Rush Cyberfunk con gamepad Material You 3 sin cambiar posiciones |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 75.763 s | 149.346 s | 1830 ms | 69182 ms | 15.924 | 180089.000 | loading | partial |
| mi-a3 | success | 68.843 s | N/R s | 1429 ms | N/R ms | N/R | 215364.000 | black_screen | failed_visual_state |
| redmi-note-8 | success | 80.586 s | N/R s | 2221 ms | N/R ms | 0.000 | 203922.000 | android_home | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260921-004); descripción: La captura T+60 muestra fondo negro con Cargando e indicador circular abajo a la derecha; el juego aún no llegó a la pantalla con gamepad en ese instante..
- `mi-a3`: [captura y CSV](../../metricas/runs/RUN-20260921-004); descripción: La captura T+60 es completamente negra y no contiene controles táctiles visibles..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260921-004); descripción: La captura T+60 muestra el panel de notificaciones/ajustes rápidos de Android cubriendo la aplicación; no permite evaluar el gamepad..

## Capturas suplementarias del gamepad

Después de cerrar el panel del sistema con Atrás, se obtuvieron dos capturas
adicionales para evaluar la estética del renderer cuando el proceso del juego ya
había presentado su superficie:

- `redmi-note-8`: [gamepad Material 3 durante carga](../../metricas/runs/RUN-20260921-004/screenshots/redmi-note-8/postrun-gamepad-material3.png). Se observan A/B/X/Y en `primary` dinámico y el resto de controles en superficies tonales, sin cambio de posición.
- `lenovo-tb-j606f`: [gamepad Material 3 en pantalla de título](../../metricas/runs/RUN-20260921-004/screenshots/lenovo-tb-j606f/postrun-gamepad-material3.png). Se observan contenedores llenos, borde de `outline` y contenido `on*` con contraste legible; la geometría coincide con el perfil existente.
- `mi-a3`: no se obtuvo una captura suplementaria evaluable; la pantalla permaneció negra durante la observación.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-004)
