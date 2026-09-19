# EXEC-037: Instalación fría de la compilación API 36 con empaquetado PAGE_ALIGNMENT_16K y observación del primer inicio

- **Run de métricas:** `RUN-20260919-005`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | Parámetro de ejecución |
| Publicación/hash | `f0529d375c1a1a4b1211586362ea0492a37a954ea0db5f1ec1d092e6bc9bd616` | SHA-256 del artefacto |
| Método | `bundletool-install-apks-cold` | Automatización de la skill |
| Escenario | `modern-api36-16k-pixel-cold-install` | Instalación fría de la compilación API 36 con empaquetado PAGE_ALIGNMENT_16K y observación del primer inicio |
| Estado esperado | title_screen | Hipótesis previa; no sustituye la observación |
| Duración | 60 s por dispositivo | Reloj monótono del host |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+60 s | Pantalla real sin navegación automática |

## Observación

Pendiente hasta finalizar la captura de datos.

## Interpretación

N/R.

## Decisión

N/R.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260919-005)
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
