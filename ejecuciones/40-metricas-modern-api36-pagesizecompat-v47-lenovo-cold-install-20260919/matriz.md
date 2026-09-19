# EXEC-040: Instalación fría de v47 en Lenovo TB-J606F; comprobar creación del entorno, arranque de Cuphead y compatibilidad de API moderna

- **Run de métricas:** `RUN-20260919-008`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | Parámetro de ejecución |
| Publicación/hash | `1bfbe6922c9d69e98f6efab22f71d4537625e4a4e800c31f486b63a433e92327` | SHA-256 del artefacto |
| Método | `bundletool-install-apks-cold` | Automatización de la skill |
| Escenario | `modern-api36-pagesizecompat-v47-lenovo-cold-install` | Instalación fría de v47 en Lenovo TB-J606F; comprobar creación del entorno, arranque de Cuphead y compatibilidad de API moderna |
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

- [Datos estructurados](../../metricas/runs/RUN-20260919-008)
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
