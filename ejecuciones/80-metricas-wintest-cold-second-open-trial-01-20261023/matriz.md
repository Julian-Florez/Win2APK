# EXEC-080: WinTest ensayo 1: instalación desde cero, primera apertura y reapertura observadas durante 300 s cada una

- **Run de métricas:** `RUN-20261023-001`
- **Fecha:** 2026-10-23
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** apertura funcional observada; requisito de instalación fría no acreditado por error de desinstalación
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `org.win2apk.testapp` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/wintest/win2apk-test-0.1.0.apks` | Archivo medido |
| SHA-256 | `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1` | Calculado antes de instalar |
| Escenario | `wintest-cold-second-open-trial-01` | WinTest ensayo 1: instalación desde cero, primera apertura y reapertura observadas durante 300 s cada una |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | success | 36.406 s | 79.251 s | 2245 ms | 41509 ms | 0.461 | 162545.000 | other | approved_experimental |

## Observación

La apertura inicial tuvo 261 muestras durante 296.760 s; `Win2APKTest.exe` apareció a los 41.509 s y el primer timestamp presentado a los 42.596 s desde el lanzamiento. El tiempo desde el inicio de instalación hasta el primer frame fue 79.251 s. La captura fría T+60 fue clasificada `other` y muestra la consola y la ventana “Win2APK Test” con “Hola mundo” y “Cambiar texto”.

### Reapertura sin reinstalación

| Duración observada | Primer proceso de app | Proceso Windows | Primer frame verificable | Captura T+60 | Resultado |
|---:|---:|---:|---:|---|---|
| 300.073 s (262 muestras) | 1.625 s | 10.221 s | 11.371 s desde el lanzamiento | `other`; misma interfaz funcional | `approved_experimental` |

La fase secundaria está en [`second-open/`](../../metricas/runs/RUN-20261023-001/second-open/). Su resumen estructurado está en [`resumen.csv`](../../metricas/runs/RUN-20261023-001/second-open/resumen.csv), la captura T+60 en [`t060.png`](../../metricas/runs/RUN-20261023-001/second-open/screenshots/lenovo-tb-j606f/t060.png), y la clasificación en [`capturas.csv`](../../metricas/runs/RUN-20261023-001/second-open/capturas.csv). Se confirmó visualmente que muestra la ventana “Win2APK Test”, “Hola mundo” y el botón “Cambiar texto”.

La instalación fría no se considera válida: `adb uninstall` terminó con código 1 y el mensaje exacto `Failure [DELETE_FAILED_INTERNAL_ERROR]`. Después del comando, `pm path` no devolvió rutas y bundletool instaló el artefacto; sin embargo, el estado previo del paquete no quedó registrado, por lo que no es posible confirmar que estuviera ausente ni que se borraran todos sus datos. Los dos logs originales se conservan en [`uninstall.log`](../../metricas/runs/RUN-20261023-001/logs/lenovo-tb-j606f/uninstall.log) y [`install-apks.log`](../../metricas/runs/RUN-20261023-001/logs/lenovo-tb-j606f/install-apks.log). La salida de bundletool incluye literalmente `Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules.`

## Interpretación

Los resultados funcionales describen esta tablet y este artefacto. La captura no
prueba por sí sola el estado de la instalación anterior; por eso esta ejecución
no cuenta como ensayo frío válido hasta repetirla con la ausencia del paquete
verificada antes de instalar.

## Decisión

Conservar este intento como ejecución con error. Hacer una repetición fría
válida más adelante, registrando `pm path` antes de desinstalar y exigiendo que
el comando de desinstalación termine correctamente; no sustituir esta evidencia.

## Evidencias

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20261023-001); descripción: La captura muestra una ventana de consola con información de Win2APKTest.exe y, encima, una ventana de aplicación titulada Win2APK Test con el texto Hola mundo y el botón Cambiar texto..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-001)
