# EXEC-061: Verificación visual del panel runtime con esquinas redondeadas y fondo dinámico Material You

- **Run de métricas:** `RUN-20260920-012`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.winlator` | Parámetro de ejecución |
| Publicación/hash | `72a41caf7d3653804118e4f2db1ecfdfac569e37b0a5d2f6c4f13c01df936408` | SHA-256 del artefacto |
| Método | `cold` | Automatización de la skill |
| Escenario | `menu-material-you-rounded-v6` | Verificación visual del panel runtime con esquinas redondeadas y fondo dinámico Material You |
| Estado esperado | title_screen | Hipótesis previa; no sustituye la observación |
| Duración | 10 s por dispositivo | Reloj monótono del host |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+1 s | Pantalla real sin navegación automática |

## Observación

Pendiente hasta finalizar la captura de datos.

## Interpretación

N/R.

## Decisión

N/R.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260920-012)
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
