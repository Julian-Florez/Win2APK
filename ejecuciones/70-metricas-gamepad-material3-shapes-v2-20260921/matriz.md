# EXEC-070: Validación del gamepad Material 3 con botones redondeados y D-pad segmentado sin cambiar posiciones

- **Run de métricas:** `RUN-20260921-005`
- **Fecha:** 2026-09-21
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | Parámetro de ejecución |
| Publicación/hash | `6c124b21758f4a886d6f65bf19442e44bdc1adb9615d7995b37b6058ee684127` | SHA-256 del artefacto |
| Método | `bundletool-install-apks-cold` | Automatización de la skill |
| Escenario | `gamepad-material3-shapes-v2` | Validación del gamepad Material 3 con botones redondeados y D-pad segmentado sin cambiar posiciones |
| Estado esperado | title_screen | Hipótesis previa; no sustituye la observación |
| Duración | 90 s por dispositivo | Reloj monótono del host |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+60 s | Pantalla real sin navegación automática |

## Observación

Pendiente hasta finalizar la captura de datos.

## Interpretación

N/R.

## Decisión

N/R.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260921-005)
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
