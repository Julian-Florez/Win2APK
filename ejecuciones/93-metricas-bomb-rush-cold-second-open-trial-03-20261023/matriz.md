# EXEC-093: Bomb Rush Cyberfunk ensayo 3 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase

- **Run de métricas:** `RUN-20261023-014`
- **Fecha:** 2026-10-23
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-03` | Bomb Rush Cyberfunk ensayo 3 en Lenovo TB-J606F: instalación desde cero y reapertura, 300 s por fase |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 85.331 s | 172.021 s | 3200 ms | 77175 ms | 44.208 | 197370.000 | compatibility_ui | partial |

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-014); descripción: Interfaz Winlator con cuadro Starting up... e indicador circular sobre fondo oscuro; la pantalla del juego no está visible en T+60..

## Segunda apertura (sin reinstalación)

Fase completada: 253 muestras, último punto a 300.132 s; el evento monitor_finished registra 301.043 s. App y proceso Bomb Rush activos al cierre; app a 1.722 s, juego a 10.844 s, primer frame a 15.004 s. FPS medio: 48.171. Captura T+60: pantalla de título con logotipo y texto `Press Any Key`; clasificación `title_screen`, revisión confirmada, resultado `approved_experimental` para la reapertura.

Captura: [second-open T+60](../../metricas/runs/RUN-20261023-014/second-open/screenshots/lenovo-tb-j606f/t060.png), SHA-256 `37c7edf54edfc104b1fe4d8a947b8d4de8f676d8ca90bd3132d8cb6b2883c295`. Validación: OK, 253 muestras. La fase fría registró `Starting up...` de Winlator a T+60 y quedó parcial; las fases se reportan separadas.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-014)
