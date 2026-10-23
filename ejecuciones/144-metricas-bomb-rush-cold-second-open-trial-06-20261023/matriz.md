# EXEC-144: Quinta pareja de instalación fría y segunda apertura de Bomb Rush Cyberfunk en Pixel 9a; último run de la campaña de 60 pares.

- **Run de métricas:** `RUN-20261023-065`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** parcial o fallido; consultar resultados por dispositivo
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-06` | Quinta pareja de instalación fría y segunda apertura de Bomb Rush Cyberfunk en Pixel 9a; último run de la campaña de 60 pares. |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | failed | 67.894 s | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R |

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

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-065); descripción: N/R.

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-065)

## Revisión documental

El `run.csv` conserva `com.cuphead` como paquete porque ese fue el valor que
recibió la herramienta; se mantiene para no reescribir el registro original. La
revisión de logs y del dispositivo confirmó que el APKS instaló
`com.win2apk.bombrushcyberfunk`, mientras que la herramienta verificó el paquete
equivocado. Antes de instalar Bomb Rush, `adb uninstall com.cuphead` terminó con
`Success`; por tanto, el intento pudo eliminar los datos privados locales de
Cuphead. No se inició el monitor y no existen muestras ni primer frame. Detalle
y corrección preventiva: [limitación 56](../../limitaciones/56-paquete-por-defecto-desinstala-app-incorrecta-pixel-20261023.md).
