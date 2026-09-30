# EXEC-078: Grabación manual de pantalla de la tablet durante una sesión de juego

- **Run de métricas:** `RUN-20260929-003`
- **Fecha:** 2026-09-29
- **Tipo:** evidencia audiovisual manual
- **Resultado general:** completada parcialmente; la persona usuaria detuvo la grabación
- **Método:** ADB `screenrecord` sobre la tablet conectada por USB

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | Parámetro de ejecución |
| Publicación/hash | `6e9824a13cecb1420f2f1253d94635cb3db60972088d57c763749d7738f5c75e` | SHA-256 del artefacto |
| Método | `manual-adb-screenrecord` | Automatización de la skill |
| Escenario | `gameplay-recording-tablet-10min` | Grabación manual de pantalla de la tablet durante una sesión de juego |
| Estado esperado | Video de pantalla reproducible durante la sesión de juego | Hipótesis previa; no sustituye la observación |
| Duración | 142 s | Duración validada con `ffprobe`; se solicitó detener la grabación antes de 10 min |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+60 s | Pantalla real sin navegación automática |

## Observación

Se obtuvo un video reproducible de 142,331 s y una captura de pantalla en T+60 s para la tablet Lenovo TB-J606F (`HA1QXMW2`). La grabación fue detenida manualmente antes de completar los 10 minutos. El codificador rechazó 2000×1200 y aplicó 1280×720.

## Interpretación

La evidencia confirma una captura parcial de la sesión; no permite afirmar que se hayan registrado los 10 minutos completos.

## Decisión

Conservar el segmento parcial y repetir la grabación únicamente si se requiere completar los 10 minutos.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260929-003)
- Video: `gameplay-tablet-20260929-part01.mp4`.
- Captura T+60: `screenshots/HA1QXMW2/t060-tablet.png`.
- Inventario y validación: `dispositivos.csv`, `logs/video-ffprobe.txt`, `logs/video-sha256.txt`.
