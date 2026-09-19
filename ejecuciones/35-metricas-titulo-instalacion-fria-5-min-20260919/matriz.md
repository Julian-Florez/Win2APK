# EXEC-035: Instalación fría completa y primer inicio observado durante cinco minutos; repetición desde cero

- **Run de métricas:** `RUN-20260919-003`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | Parámetro de ejecución |
| Publicación/hash | `9063bacab88dd543bcee024e50e0b34b2f0dcb8593a0ef1784c3840c5a5e1d28` | SHA-256 del artefacto |
| Método | `bundletool-install-apks-cold` | Automatización de la skill |
| Escenario | `titulo-instalacion-fria-5-min` | Instalación fría completa y primer inicio observado durante cinco minutos; repetición desde cero |
| Estado esperado | title_screen | Hipótesis previa; no sustituye la observación |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+60 s | Pantalla real sin navegación automática |

## Observación

Pendiente hasta finalizar la captura de datos.

## Interpretación

N/R.

## Decisión

N/R.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260919-003)
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
