# EXEC-075: Observación del prototipo preinstalado en Redmi para la sustentación

- **Run de métricas:** `RUN-20260922-002`
- **Fecha:** 2026-09-22
- **Tipo:** automatizada, observación de una instalación existente
- **Resultado general:** aprobado experimentalmente para demo; instalación no evaluada
- **Método:** `preinstalled-no-reinstall`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto de referencia | APK base extraído de la instalación existente | No se reinstaló |
| SHA-256 | `91066eb6c60d72ad35318c1fe229dbd19d087ea946b22453b5b709f82817a803` | Calculado sobre el APK base extraído |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 120 s | Reloj monótono del host |
| Intervalo nominal | 1 s | ADB sin root |
| Captura canónica | T+60 s | Revisión visual humana |

## Métricas por dispositivo

| Dispositivo | Instalación | App visible | Juego visible | Primer frame | Captura T+60 | PSS juego máximo | Resultado |
|---|---|---:|---:|---:|---|---:|---|
| Redmi Note 8 | N/A, preinstalada | 2.274 s | 2.275 s | 6.353 s | `title_screen` | 877,570 KiB | aprobado experimentalmente para demo |

## Observación

La aplicación y el proceso del juego permanecieron observables durante toda la
ventana de 120 s. La captura T+60 muestra la pantalla de título de Bomb Rush
Cyberfunk con el gamepad táctil Material 3 superpuesto. El video de 45 segundos
conserva la misma ruta visible para usarla como respaldo de la demostración.

## Interpretación

La ejecución confirma, para esta instalación y este Redmi Note 8, el arranque
hasta la pantalla de título y la visibilidad de los controles. No evalúa una
instalación fría, la interacción completa ni la compatibilidad con otros
dispositivos.

El campo `failed_install` de `resumen.csv` no describe el resultado observado:
es el defecto conocido del agregador para el modo preinstalado, documentado en
la [limitación 37](../../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md).

Los valores de FPS se conservan en los CSV, pero no se presentan como una
medición de jugabilidad porque la ventana corresponde principalmente a carga y
pantalla de título.

## Decisión

Usar el Redmi Note 8 como dispositivo principal de la demo y el video de esta
ejecución como respaldo local. Mantener la afirmación limitada a las
condiciones observadas.

## Evidencias

- [Captura T+60](../../metricas/runs/RUN-20260922-002/screenshots/redmi-note-8/t060.png)
- [Video de 45 segundos](../../metricas/runs/RUN-20260922-002/screenshots/redmi-note-8/demo-45s.mp4)
- [Logcat](../../metricas/runs/RUN-20260922-002/logs/redmi-note-8/logcat.txt)
- [Run estructurado](../../metricas/runs/RUN-20260922-002/)
- [Limitación del agregador](../../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md)
