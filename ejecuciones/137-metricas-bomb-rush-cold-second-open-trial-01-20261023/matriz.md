# EXEC-137: Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 01 de 05

- **Run de métricas:** `RUN-20261023-058`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** incompleto; monitor interrumpido a T+97 s (98/301 muestras)
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.win2apk.bombrushcyberfunk` | `run.csv` |
| Artefacto | `dist/bomb-rush-cyberfunk/bomb-rush-cyberfunk-gog-56774571391351451.apks` | Archivo medido |
| SHA-256 | `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54` | Calculado antes de instalar |
| Escenario | `bomb-rush-cold-second-open-trial-01` | Instalación fresca de Bomb Rush Cyberfunk en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos; repetición 01 de 05 |
| Estado esperado | `title_screen` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | success | 72.988 s | 129.148 s | 1848 ms | 48199 ms | 47.793 | 737417.000 | loading | partial |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R |

## Observación

La instalación concluyó en 72.988 s y el primer frame se observó a 129.148 s
desde el comienzo del envío. Solo se registraron 98/301 muestras, hasta T+97 s;
la última muestra mantiene `app_alive=true` y `game_alive=true`. No existe
`monitor_finished` ni `exit-info.txt`, y no se completó la segunda apertura.
El cliente de sesión devolvió `write_stdin failed: Unknown process id 49044`;
la causa de que la sesión terminara es N/R. No se infiere un crash del juego.
Después de terminar la sesión, una comprobación separada informó batería a
44.6 °C y `Thermal Status: 4` (`CRITICAL`); se detuvo la app y se apagó la
pantalla para enfriar. Este dato posterior no prueba la causa de la interrupción
([registro](../../metricas/runs/RUN-20261023-058/logs/pixel-9a/post-monitor-thermal.txt)).

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

No contar este run entre las cinco repeticiones válidas. Repetir desde una
instalación limpia en un nuevo run; mantener este registro como evidencia
incompleta y enlazarlo con la [limitación 53](../../limitaciones/53-interrupcion-monitor-bomb-rush-pixel-9a-20261023.md).

## Evidencias

- `pixel-9a`: [evidencias frías](../../metricas/runs/RUN-20261023-058); descripción: Pantalla de presentación/carga de Bomb Rush Cyberfunk: logotipo de Team Reptile centrado sobre fondo blanco; aún no aparece el menú principal..

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-058)
