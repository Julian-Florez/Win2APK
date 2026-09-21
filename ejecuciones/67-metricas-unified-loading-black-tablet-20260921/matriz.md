# EXEC-067: Instalación y verificación de la nueva pantalla de carga negra de Bomb Rush Cyberfunk en Lenovo TB-J606F

- **Run de métricas:** `RUN-20260921-002`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `/tmp/win2apk-loading-black-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `8a25a02d6aeff4573cef9f72d6921c80b51c04d2f538919fe20562059de9a5ac` | Calculado antes de instalar |
| Escenario | `unified-loading-black-tablet` | Instalación y verificación de la nueva pantalla de carga negra de Bomb Rush Cyberfunk en Lenovo TB-J606F |
| Estado esperado | `loading` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 77.110 s | 140.258 s | 1931 ms | 69222 ms | 16.150 | 187351.000 | loading | approved_experimental |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260921-002); descripción: Pantalla de carga unificada: fondo negro, texto blanco Cargando y el indicador circular en la esquina inferior derecha..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-002)
