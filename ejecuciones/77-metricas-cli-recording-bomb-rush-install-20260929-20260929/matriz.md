# EXEC-077: Validación de la compilación mostrada en la grabación del CLI, instalada en Lenovo TB-J606F

- **Run de métricas:** `RUN-20260929-002`
- **Fecha:** 2026-09-29
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-bomb-rush/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `36799329e77be8494711df442e20a000733ad92aaeb2cd788104ba27b6d35901` | Calculado antes de instalar |
| Escenario | `cli-recording-bomb-rush-install-20260929` | Validación de la compilación mostrada en la grabación del CLI, instalada en Lenovo TB-J606F |
| Estado esperado | `loading` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 80.256 s | 154.161 s | 1509 ms | 68226 ms | 15.039 | 189940.000 | loading | approved_experimental |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260929-002); descripción: La captura T+60 muestra la pantalla de carga unificada: fondo negro, texto Cargando e indicador circular blanco en la esquina inferior derecha..
- [Video corto de la ejecución del CLI con paleta gris temporal](../../cli-bomb-rush-demo-20260929.mp4)

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260929-002)
