# EXEC-074: Observación del prototipo preinstalado en Lenovo para la sustentación

- **Run de métricas:** `RUN-20260922-001`
- **Fecha:** 2026-09-22
- **Tipo:** automatizada, observación de una instalación existente
- **Resultado general:** error reproducido; instalación no evaluada
- **Método:** `preinstalled-no-reinstall`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto de referencia | APK base extraído de la instalación existente | No se reinstaló |
| SHA-256 | `816cd604c09984452fb643827d125bc563550a578b40c9a7b4a749ca7ee23282` | Calculado sobre el APK base extraído |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 120 s | Reloj monótono del host |
| Intervalo nominal | 1 s | ADB sin root |
| Captura canónica | T+60 s | Revisión visual humana |

## Métricas por dispositivo

| Dispositivo | Instalación | App visible | Juego visible | Captura T+60 | PSS app máximo | Resultado |
|---|---|---:|---:|---|---:|---|
| Lenovo TB-J606F | N/A, preinstalada | 2.039 s | N/R | `error_screen` | 162,968 KiB | error reproducido |

## Observación

La aplicación permaneció visible durante la ventana de 120 s. A T+60 se
observó el diálogo `Winlator Core error` con el mensaje `Unable to create the
configured container or shortcut.` El `logcat` registró exactamente:

```text
com.google.android.play.core.common.LocalTestingException: No APKs available for pack 'win2apk_payload_002'.
```

## Interpretación

El fallo está asociado a la disponibilidad del pack de pruebas locales en el
estado instalado observado. La ejecución no evaluó instalación y no demuestra
una incompatibilidad general del dispositivo ni de Bomb Rush Cyberfunk.

El valor `failed_install` conservado en `resumen.csv` es una clasificación
automática incorrecta para el modo preinstalado, ya documentada en la
[limitación 37](../../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md).

## Decisión

No usar esta instalación de Lenovo para la demostración. Mantenerla como caso
de limitación y emplear el Redmi Note 8, validado separadamente en `EXEC-075`,
como ruta principal y fuente del video de respaldo.

## Evidencias

- [Captura T+60](../../metricas/runs/RUN-20260922-001/screenshots/lenovo-tb-j606f/t060.png)
- [Video de 45 segundos](../../metricas/runs/RUN-20260922-001/screenshots/lenovo-tb-j606f/demo-45s.mp4)
- [Logcat](../../metricas/runs/RUN-20260922-001/logs/lenovo-tb-j606f/logcat.txt)
- [Run estructurado](../../metricas/runs/RUN-20260922-001/)
- [Limitación 43](../../limitaciones/43-pack-local-testing-ausente-lenovo-sustentacion-20260922.md)
