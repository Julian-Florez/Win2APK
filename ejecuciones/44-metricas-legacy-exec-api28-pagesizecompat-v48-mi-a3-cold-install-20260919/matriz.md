# EXEC-044: Instalación fría de v48 con target API 28; comprobar ejecución de Cuphead en Mi A3

- **Run de métricas:** `RUN-20260919-012`
- **Fecha:** 2026-09-19
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** ejecución confirmada; arranque diferido dentro de la ventana
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.cuphead` | `run.csv` |
| Artefacto | `winlator/app/app/build/outputs/bundle/debug/app-debug.aab` y APKS local-testing v48 | Artefacto usado por bundletool |
| SHA-256 APKS | `23a2f8fb802c2435d2fcf1070dd6535484e15cffeb208ce30bff1e266cb41d31` | Calculado antes de instalar |
| Escenario | `legacy-exec-api28-pagesizecompat-v48-mi-a3-cold-install` | Instalación fría de v48 en Xiaomi Mi A3 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s | Reloj monótono del host |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| mi-a3 | success | 188.205 s | 391.412 s | 1867 ms | 202594 ms | 36.816 | 186150.000 | loading | ejecución confirmada |

## Observación

La medición automatizada capturó `Preparing application...` en T+60. El proceso
del juego apareció a 202.594 s y el primer frame fue registrado a 202.960 s
desde el inicio de la monitorización; permaneció observable hasta T+300.

## Interpretación

El arranque es lento, pero no corresponde a un cierre en esta ejecución. El
tiempo de 188.205 s es el tiempo de instalación, mientras que 391.412 s es la
entrega desde el inicio del envío hasta el primer frame. No se deben mezclar
ambos relojes.

## Decisión

Aceptar la variante v48 como ejecutable en Mi A3 bajo estas condiciones y
conservar el arranque diferido como métrica de rendimiento, no como evidencia
de compatibilidad inmediata en T+60.

## Evidencias

- [Resumen CSV y log del run](../../metricas/runs/RUN-20260919-012)
- [Captura T+60](../../metricas/runs/RUN-20260919-012/screenshots/mi-a3/t060.png)
- [Matriz de métricas generada](../../metricas/runs/RUN-20260919-012/resumen.csv)
