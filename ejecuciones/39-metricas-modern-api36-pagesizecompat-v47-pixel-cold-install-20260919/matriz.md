# EXEC-039: Instalación fría de v47 con target API 36 y pageSizeCompat habilitado; conservar bibliotecas opcionales; comprobar arranque y ausencia del diálogo 16 KB

- **Run de métricas:** `RUN-20260919-007`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** parcial o no concluyente
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/apks/cuphead-v47-pagesizecompat-local-testing.apks` | Archivo medido |
| SHA-256 | `1bfbe6922c9d69e98f6efab22f71d4537625e4a4e800c31f486b63a433e92327` | Calculado antes de instalar |
| Escenario | `modern-api36-pagesizecompat-v47-pixel-cold-install` | Instalación fría de v47 con target API 36 y pageSizeCompat habilitado; conservar bibliotecas opcionales; comprobar arranque y ausencia del diálogo 16 KB |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 595.372 s | N/R s | 2872 ms | N/R ms | N/R | 287336.000 | loading | partial |

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

- `pixel-9a`: [captura y CSV](../../metricas/runs/RUN-20260919-007); descripción: Pantalla negra con el texto claramente visible 'Preparing application...' y un indicador circular azul en la parte superior; no se observa la pantalla de título ni el juego..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260919-007)
