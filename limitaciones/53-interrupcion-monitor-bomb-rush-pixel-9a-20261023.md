# 53. Interrupción del monitor durante Bomb Rush Cyberfunk en Pixel 9a

## Descripción

La instalación fría de Bomb Rush Cyberfunk terminó correctamente, pero la
sesión de medición se interrumpió después de 98 muestras (T+97 s de 300 s). La
última muestra registró tanto la app Android como `Bomb Rush Cyberfunk.exe`
activos. No se registró salida del proceso ni se produjo la segunda apertura.
No hay evidencia suficiente para atribuir la interrupción a un crash del juego,
al estado térmico o a una causa concreta del host.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Android 17/API 37, ABI `arm64-v8a`; inventario en
  [RUN-20261023-058](../metricas/runs/RUN-20261023-058/dispositivos.csv).
- Aplicación: Bomb Rush Cyberfunk, paquete `com.win2apk.bombrushcyberfunk`,
  proceso `Bomb Rush Cyberfunk.exe`.
- Artefacto APKS: 2,286,674,276 bytes; SHA-256
  `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54`.
- Bundletool: 1.18.3. Instalación completa en 72.988 s.
- Run: `RUN-20261023-058`, `EXEC-137`; se registraron 98 muestras de las 301
  previstas, con cobertura hasta T+97 s. No existe `exit-info.txt` porque la
  sesión del monitor terminó antes de ejecutar su cierre.
- Captura T+60: splash de Team Reptile, clasificado como `loading`.
- La máxima temperatura de batería registrada en las muestras disponibles fue
  43.6 °C; no se registró un estado térmico que demuestre que esto causara la
  interrupción.
- En una comprobación posterior, el dispositivo informó batería a 44.6 °C y
  `Thermal Status: 4` (`CRITICAL`). Luego se detuvo la app y se apagó la pantalla
  para enfriamiento. La observación fue posterior y no identifica la causa de la
  pérdida de sesión; véase [post-monitor-thermal.txt](../metricas/runs/RUN-20261023-058/logs/pixel-9a/post-monitor-thermal.txt).

## Reproducción o evidencia

1. Ejecutar instalación fría secuencial con `run_experiment.py` en el Pixel.
2. Bundletool completa la instalación; la aplicación aparece y posteriormente
   se detecta `Bomb Rush Cyberfunk.exe`.
3. La captura T+60 muestra el splash de Team Reptile y el primer frame se observa
   a los 129.148 s desde el inicio del envío del artefacto.
4. `muestras.csv` contiene índices 0–97. La fila final, a T+97 s, indica
   `app_alive=true` y `game_alive=true`.
5. Al continuar la supervisión, el cliente de sesión devuelve exactamente:
   `write_stdin failed: Unknown process id 49044`. Después no quedan procesos
   `run_experiment.py` ni `monitor_device.py`; `eventos.csv` no contiene el
   cierre automático `monitor_finished`.

Evidencia primaria: [CSV, captura y logs de RUN-20261023-058](../metricas/runs/RUN-20261023-058/), [matriz EXEC-137](../ejecuciones/137-metricas-bomb-rush-cold-second-open-trial-01-20261023/matriz.md).

## Impacto

RUN-20261023-058 conserva evidencia parcial de instalación y arranque, pero no
cumple la ventana de cinco minutos ni permite evaluar estabilidad completa. No
cuenta entre las cinco repeticiones requeridas y no tiene medición de segunda
apertura.

## Análisis técnico

Los datos disponibles contradicen la hipótesis de un cierre del juego durante
la última muestra: app y proceso del juego seguían presentes. El error observado
se refiere a la sesión host que exponía la salida del monitor; no se cuenta con
stack trace, `exit-info.txt` ni evento final que determine por qué terminó esa
sesión. La temperatura elevada y el nivel térmico `CRITICAL` observados después
son una señal de seguridad relevante, pero no prueban que el calor terminara la
sesión del monitor ni que el juego hubiera fallado.

## Solución aplicada

No se alteraron ajustes gráficos, configuración de seguridad ni archivos del
juego. Después del diagnóstico térmico se detuvo la app con `am force-stop` y se
apagó la pantalla (`mWakefulness=Dozing`) para enfriar el Pixel. Luego se hizo
un reintento fresco, [RUN-20261023-059](../metricas/runs/RUN-20261023-059/), con
el Pixel ya en estado térmico 1; tampoco cuenta, pues la pantalla seguía
bloqueada y el monitor se detuvo a T+166 s (véase [limitación 54](54-pixel-bloqueado-tras-despertar-durante-prueba-bomb-rush-20261023.md)).
RUN-20261023-058 se conserva como `completed_with_errors`; las muestras que
faltan no se completan ni inventan.

## Resultado

Instalación correcta y primer frame medido; monitoreo interrumpido a T+97 s, con
app y juego presentes en la última muestra. Causa de terminación del monitor:
N/R. Segunda apertura: N/A, no ejecutada.

## Limitaciones pendientes

- Repetir desde cero en el Pixel y comprobar si el monitor completa los 300 s.
- Desbloquear el dispositivo manualmente antes de comenzar el siguiente intento;
  no se puede resolver la condición de huella mediante ADB.
- Si el monitor vuelve a interrumpirse con el teléfono despierto y desbloqueado,
  obtener estado y logs del host antes de relanzar la suite.
- No generalizar este incidente a la estabilidad de Bomb Rush ni del Pixel.

## Referencias

- [RUN-20261023-058](../metricas/runs/RUN-20261023-058/)
- [EXEC-137](../ejecuciones/137-metricas-bomb-rush-cold-second-open-trial-01-20261023/matriz.md)
- [Skill de medición](../.codex/skills/win2apk-medir-dispositivos/SKILL.md)

## Ejecuciones asociadas

- [EXEC-137](../ejecuciones/137-metricas-bomb-rush-cold-second-open-trial-01-20261023/matriz.md): instalación completa; monitoreo interrumpido a T+97 s, sin causa confirmada.
- [EXEC-138](../ejecuciones/138-metricas-bomb-rush-cold-second-open-replacement-01-20261023/matriz.md): reintento tras enfriamiento; pantalla dormida/bloqueada; monitoreo detenido a T+166 s.
