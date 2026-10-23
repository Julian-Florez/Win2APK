# EXEC-085: WinTest ensayo 6: reemplazo para completar cinco parejas válidas, instalación fría y reapertura observadas 300 s cada una

- **Run de métricas:** `RUN-20261023-006`
- **Fecha:** 2026-10-23
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** aprobado experimentalmente en los dispositivos medidos
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `org.win2apk.testapp` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/wintest/win2apk-test-0.1.0.apks` | Archivo medido |
| SHA-256 | `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1` | Calculado antes de instalar |
| Escenario | `wintest-cold-second-open-trial-06` | WinTest ensayo 6: reemplazo para completar cinco parejas válidas, instalación fría y reapertura observadas 300 s cada una |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 33.232 s | 76.724 s | 1694 ms | 35440 ms | 2.829 | 184660.000 | other | approved_experimental |

### Reapertura sin reinstalar

| Observación | Muestras | App visible | WinTest visible | Primer frame | FPS medio | PSS app máx. KiB | Captura | Resultado |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 300.201 s | 266 | 1216 ms | 9921 ms | 14039 ms | 0.466 | 118532 | `other` | `approved_experimental` |

La pareja fría+cálida queda como el quinto válido del lote. RUN-001 fue excluido
por instalación fría no acreditada; RUN-002 a RUN-006 son **5/5 válidos**.
Ambas capturas originales de RUN-006 muestran la ventana “Hola mundo” y están
clasificadas `other` con revisión confirmada.

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

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-006); descripción: PNG frío T+60: consola Win2APKTest.exe con PID 224 y ventana Win2APK Test visible con Hola mundo y el botón Cambiar texto; OCR confirma el texto..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-006)
