# EXEC-060: Panel lateral runtime Material 3 flotante y compacto

- **Run de métricas:** `RUN-20260920-011`
- **Fecha:** 2026-09-20
- **Tipo:** instalación fría y verificación manual ADB
- **Resultado general:** aprobado para la observación visual solicitada
- **Método:** reinstalación fría, arranque de `Container-1` y apertura del drawer mediante Atrás, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.winlator` | Paquete base requerido por las rutas del rootfs |
| Artefacto | `/tmp/win2apk-ui-build-panel-v5/win2apk-ui-preview-material3-preview-runtime.apks` | Archivo instalado |
| SHA-256 | `e8a14c80dd410b5bcec05c368a3067d13b74e24029e8cb735628e249b4a34ec8` | Calculado antes de instalar |
| Instalación | `cold` | Desinstalación completa e instalación con bundletool |
| Dispositivos | Redmi Note 8 horizontal; Lenovo TB-J606F vertical | Orientación observada, sin forzarla |

## Resultado

La actividad `XServerDisplayActivity` se verificó en ambos dispositivos. El panel ya no muestra la cabecera con la imagen de Winlator ni la sección superior de color. Usa un fondo Material 3 opaco, ocupa menos ancho que el drawer original y queda centrado verticalmente cuando el alto disponible permite mostrar todas las opciones.

En el Redmi Note 8 horizontal, la lista excede el alto disponible y queda desplazable; en la Lenovo TB-J606F vertical se observan las diez opciones: Keyboard, Input Controls, Toggle Fullscreen, Task Manager, Active Windows, Magnifier, Screen Effect, PiP Mode, Touchpad Help y Exit.

La observación ADB adicional registró 22 muestras en 10 segundos; GPU/FPS no se reportaron por la instrumentación disponible (`N/R`).

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260920-011)
- Redmi Note 8: [carga](../../metricas/runs/RUN-20260920-011/screenshots/redmi-note-8/loading.png), [panel final](../../metricas/runs/RUN-20260920-011/screenshots/redmi-note-8/panel.png), [captura canónica](../../metricas/runs/RUN-20260920-011/screenshots/redmi-note-8/t001.png).
- Lenovo TB-J606F: [carga](../../metricas/runs/RUN-20260920-011/screenshots/lenovo-tb-j606f/loading.png), [panel final](../../metricas/runs/RUN-20260920-011/screenshots/lenovo-tb-j606f/panel.png), [captura canónica](../../metricas/runs/RUN-20260920-011/screenshots/lenovo-tb-j606f/t001.png).
- [Logs](../../metricas/runs/RUN-20260920-011/logs/).
