# EXEC-068: Instalación y arranque de Bomb Rush Cyberfunk con controles táctiles condicionales

- **Run de métricas:** `RUN-20260921-003`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** instalación verificada en los tres dispositivos; arranque visual parcial
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` y `pm path` posterior |
| Artefacto | `/tmp/win2apk-gamepad-conditional-v1/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `63efdfd640e76275c48cf496d814cf484b5347de741d4fb66518845b3eb7c1d1` | Calculado antes de instalar |
| Escenario | `gamepad-conditional-install` | Instalación y arranque de Bomb Rush Cyberfunk con controles táctiles condicionales |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | warning_verified | 77.422 s | N/R s | 1270 ms | N/R ms | 37.574 | 118220.000 | title_screen | installed_and_visible |
| mi-a3 | warning_verified | 68.986 s | N/R s | 1423 ms | N/R ms | N/R | 62567.000 | black_screen | installed_and_running |
| redmi-note-8 | warning_verified | 75.307 s | N/R s | 1420 ms | N/R ms | 59.058 | 140053.000 | loading | installed_and_running |

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas. El instalador devolvió el aviso
de limpieza de `local_testing`, pero una comprobación ADB posterior encontró
`com.win2apk.bombrushcyberfunk` instalado con `versionName=gog-56774571391351451`
en los tres dispositivos. La tablet mostró la pantalla de título y el overlay
`Virtual Gamepad`.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

La instalación se acepta para esta comprobación porque el paquete y la versión
se verificaron con ADB después del aviso. El arranque funcional queda parcial:
la tablet llegó al título, el Redmi permaneció en carga y el Mi A3 quedó negro
con el proceso de la aplicación vivo.

## Evidencias

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260921-003); descripción: Pantalla de título de Bomb Rush Cyberfunk visible; el control táctil Virtual Gamepad aparece superpuesto con botones y sticks translúcidos..
- `mi-a3`: [captura y CSV](../../metricas/runs/RUN-20260921-003); descripción: Pantalla completamente negra a T+60; la aplicación permaneció visible durante el monitoreo, sin texto legible..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260921-003); descripción: Pantalla negra de carga; se observan el texto Cargando y el indicador circular en la esquina inferior derecha..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260921-003)
- [Limitación 41: aviso de limpieza de bundletool](../../limitaciones/41-bundletool-local-testing-release-no-debuggable.md)
