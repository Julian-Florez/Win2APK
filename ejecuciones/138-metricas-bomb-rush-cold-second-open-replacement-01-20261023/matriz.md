# EXEC-138: Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; reemplazo del run incompleto 01; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos

- **Run de métricas:** `RUN-20261023-059`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** incompleto; Pixel bloqueado tras despertar, monitor detenido a T+166 s
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-replacement-01` | Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; reemplazo del run incompleto 01; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 68.191 s | N/R s | 1777 ms | 85205 ms | N/R | 608022.000 | unknown | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R |

## Observación

La instalación terminó en 68.191 s. La app apareció a 1.777 s y
`Bomb Rush Cyberfunk.exe` a 85.205 s desde el lanzamiento. No se registró primer
frame dentro de la ventana observada. La captura T+60 es negra; después se
confirmó `mWakefulness=Dozing` y, al despertar, el Pixel mostró el bloqueo con
huella. Se detuvo el run a T+166 s (167 muestras), sin segunda apertura. No se
atribuye el negro al juego; detalles en la [limitación 54](../../limitaciones/54-pixel-bloqueado-tras-despertar-durante-prueba-bomb-rush-20261023.md).

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

No contar este run entre las cinco repeticiones. Esperar a que el usuario
desbloquee el Pixel y repetir desde cero con la pantalla despierta.

## Evidencias

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-059); descripción: La captura T+60 es completamente negra y no permite determinar si el juego presentó negro o si la pantalla estaba dormida. En una comprobación posterior ADB mostró Dozing; al despertar apareció la pantalla de bloqueo con huella. No se infiere un fallo de renderizado..
- [Captura de bloqueo tras despertar](../../metricas/runs/RUN-20261023-059/screenshots/pixel-9a/after-wake-locked.png) y [log de estado](../../metricas/runs/RUN-20261023-059/logs/pixel-9a/post-monitor-screen-lock.txt).

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-059)
