# EXEC-052: Interfaz general Material 3 después del permiso inicial, sin reinstalar

- **Run de métricas:** `RUN-20260920-003`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, lanzamiento preinstalado y medición temporal
- **Resultado general:** aprobado para la observación inicial de la interfaz; validación de orientaciones restantes pendiente
- **Método:** `preinstalled-no-reinstall`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.ui.preview` | `run.csv` |
| Artefacto | `dist/ui-preview/win2apk-ui-preview.apks` | Archivo medido |
| SHA-256 | `6041a788beeea0e6bb7cc51a279690c52919c33bedf2763e7c0f086bf9adc0e8` | Calculado antes de instalar |
| Escenario | `ui-material3-preview-after-permission-phone-landscape-tablet-portrait` | Interfaz general Material 3 después del permiso inicial; sin reinstalar |
| Estado esperado | `menu` | Hipótesis previa |
| Duración | 70 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 2.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| lenovo-tb-j606f | No realizada | N/A | N/R | 386 ms | N/R | N/R | 103127.000 | menu | Observado |
| redmi-note-8 | No realizada | N/A | N/R | 361 ms | N/R | N/R | 94947.000 | menu | Observado |

## Observación

El run no desinstaló ni reinstaló el APK. Después de conceder manualmente el
permiso de almacenamiento solicitado durante EXEC-051, ambos procesos quedaron
visibles y el monitor registró 36 muestras por dispositivo.

En el Redmi horizontal se observó la pantalla `Containers` con `Container-1`,
acciones de ejecutar y menú contextual. En la Lenovo vertical se observó una
barra de navegación permanente a la izquierda y el contenido de `Containers` a
la derecha. Las celdas `N/R` no se infieren a partir de otras métricas.

El campo `failed_install` conservado por `resumen.csv` es una clasificación
automática incorrecta para `preinstalled-no-reinstall`; se corrige aquí sin
reescribir el CSV histórico. Ver [limitación 37](../../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md).

## Interpretación

La ejecución confirma el arranque y la composición inicial de la interfaz
general en un teléfono horizontal y una tablet vertical. También confirma que
los colores dinámicos del dispositivo modifican la paleta visible, que en esta
sesión tomó tonos naranja. Esto no valida todavía tema claro, orientación
vertical del teléfono, horizontal de la tablet, TalkBack ni todas las pantallas.

## Decisión

Conservar la migración Material 3 y continuar con pruebas de tema, navegación,
diálogos, runtime y las dos orientaciones no cubiertas por este run. No afirmar
compatibilidad general a partir de estos dos dispositivos.

## Evidencias

- `lenovo-tb-j606f`: [captura y CSV](../../metricas/runs/RUN-20260920-003); descripción: Pantalla general en tablet vertical con navegación permanente a la izquierda y contenido Containers a la derecha..
- `redmi-note-8`: [captura y CSV](../../metricas/runs/RUN-20260920-003); descripción: Pantalla Containers de la interfaz general en teléfono horizontal; se observa Container-1, acción de ejecutar y menú contextual..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20260920-003)
