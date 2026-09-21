# EXEC-050: Línea base visual del paquete Winlator instalado en Redmi Note 8 horizontal, sin reinstalación

- **Run de métricas:** `RUN-20260920-001`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, lanzamiento de paquete preinstalado y medición temporal
- **Resultado general:** paquete Core observado; la interfaz general no quedó medida
- **Método:** `preinstalled-no-reinstall`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.winlator` | `run.csv` |
| Artefacto | `dist/ui-baseline/com.winlator-v11.1-core.apk` | Archivo medido |
| SHA-256 | `a95c77cffaa859ff9adcf863770479c507ab2621b6b54c5cfbaf83f74cde86dd` | Calculado sobre el APK extraído del dispositivo antes del lanzamiento |
| Escenario | `ui-base-nocore-redmi-horizontal` | Hipótesis inicial del run; la observación demostró que el paquete era Core |
| Estado esperado | `compatibility_ui` | Hipótesis previa |
| Duración | 70 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| redmi-note-8 | No realizada | N/A | N/R | 1227 ms | N/R | 1.224 | 150459.000 | `other`; secundaria `compatibility_ui` | Paquete Core visible |

## Observación

El paquete `com.winlator` ya estaba instalado. No se ejecutó `adb install`,
`bundletool install-apks` ni una desinstalación. A T+60 se observó el escritorio
del entorno de compatibilidad, una consola y la ventana de Win2APKTest con los
textos `Hola mundo` y `Cambiar texto`. Esto corresponde al flujo Core y no a la
interfaz general de Winlator que se pretendía inventariar.

El valor `failed_install` conservado en `resumen.csv` y en los catálogos es una
salida automática incorrecta: el agregador interpreta la ausencia de una fila
de instalación como fallo aun cuando `install_mode` es
`preinstalled-no-reinstall`. No se modifica el CSV histórico; la corrección se
documenta aquí y en la [limitación 37](../../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md).

## Interpretación

La ejecución confirma qué variante estaba instalada y aporta una línea base del
flujo Core en Redmi horizontal. No aporta evidencia sobre la pantalla de
contenedores, shortcuts, ajustes o gestor de archivos de la variante general.

## Decisión

Compilar una variante temporal con `coreMode=false` y un `applicationId`
independiente para medir la interfaz general sin sustituir la aplicación Core.
La validación de la nueva interfaz deberá incluir móvil y tablet, en vertical y
horizontal.

## Evidencias

- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-001); descripción: Se observa un escritorio negro del entorno de compatibilidad con una consola de Win2APKTest, una ventana gráfica que muestra Hola mundo y una pestaña lateral parcialmente visible..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-001)
