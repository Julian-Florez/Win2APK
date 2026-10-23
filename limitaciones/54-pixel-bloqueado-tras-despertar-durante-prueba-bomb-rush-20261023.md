# 54. Pixel 9a mostró la pantalla de bloqueo tras despertar durante Bomb Rush

## Descripción

Después de enfriar el Pixel 9a, la siguiente instalación fría de Bomb Rush se
midió con la pantalla inicialmente en reposo. La captura T+60 quedó negra y una
comprobación posterior mostró `mWakefulness=Dozing`. Al despertar el teléfono,
apareció la pantalla de bloqueo con una solicitud de huella. El gesto de
deslizamiento no la descartó. No se ingresaron credenciales ni se intentó
eludir la autenticación. La medición se detuvo antes de cinco minutos. En la
continuación del 2026-10-23, el usuario desbloqueó manualmente el Pixel; antes
de iniciar RUN-065, ADB confirmó `mWakefulness=Awake` y `showing=false`. Ese run
no llegó a abrir el juego por una causa distinta, documentada en la
[limitación 56](56-paquete-por-defecto-desinstala-app-incorrecta-pixel-20261023.md).

## Contexto técnico

- Dispositivo: Google Pixel 9a, Android 17/API 37, ABI `arm64-v8a`.
- App: Bomb Rush Cyberfunk (`com.win2apk.bombrushcyberfunk`), proceso
  `Bomb Rush Cyberfunk.exe`.
- Instalación APKS completa en 68.191 s; artefacto y hash en
  [RUN-20261023-059](../metricas/runs/RUN-20261023-059/run.csv).
- Run: `RUN-20261023-059`, `EXEC-138`; 167 muestras hasta T+166 s, frente a 301
  previstas. La última muestra tiene `app_alive=true` y `game_alive=true`.
- Estado antes del run, tras enfriamiento: batería 40.7 °C, `Thermal Status 1`;
  la pantalla estaba apagada. Inventario y métricas: RUN-20261023-059.

## Reproducción o evidencia

1. Lanzar el run frío desde el Pixel con la pantalla apagada tras el periodo de
   enfriamiento.
2. La captura canónica T+60 es completamente negra. El proceso de juego se
   detecta a 85.205 s, pero no se registra un evento de primer frame.
3. Una consulta posterior informa `mWakefulness=Dozing`. `input keyevent 26`
   despierta el panel; la pantalla resultante presenta el bloqueo del Pixel y
   el icono de huella.
4. Se intenta deslizar hacia arriba una vez; la pantalla de bloqueo permanece.
   No se introduce PIN, patrón ni huella y no se ejecuta un comando para
   descartar la autenticación.
5. Se detiene el monitor a T+166 s, se detiene la app y se apaga la pantalla.
   El diagnóstico posterior informa batería 38.5 °C y `Thermal Status 1`.

Evidencia: [captura T+60 y captura del bloqueo tras despertar](../metricas/runs/RUN-20261023-059/screenshots/pixel-9a/), [log del estado de pantalla](../metricas/runs/RUN-20261023-059/logs/pixel-9a/post-monitor-screen-lock.txt), [CSV y eventos](../metricas/runs/RUN-20261023-059/), [matriz EXEC-138](../ejecuciones/138-metricas-bomb-rush-cold-second-open-replacement-01-20261023/matriz.md).

## Impacto

RUN-20261023-059 no cumple los cinco minutos, no contiene una medición de
segunda apertura y no cuenta entre las cinco repeticiones. La clase visual se
corrigió a `unknown`: la captura negra no basta para atribuir el estado al juego
porque el dispositivo estaba o pudo estar dormido. No se concluye un fallo
gráfico ni un crash.

## Análisis técnico

La última muestra del run indica que los procesos Android y de Windows seguían
activos cuando se detuvo el monitor. La pantalla de bloqueo impidió observar el
estado visual del juego tras despertar. El sistema solo confirmó `Dozing` en una
consulta posterior a la captura T+60; por ello no se puede afirmar que la
pantalla estuviera apagada exactamente en el instante de la captura. La
autenticación requerida y el estado inicial de pantalla son condiciones del
dispositivo/prueba, no evidencia de incompatibilidad de Bomb Rush.

## Solución aplicada

Se conservó el run incompleto y se detuvo la app para reducir actividad. El
usuario desbloqueó el Pixel manualmente antes de continuar; la comprobación
previa a RUN-065 observó la pantalla despierta y sin keyguard. No se cambió Play
Protect, no se omitió el bloqueo y no se modificó la configuración del juego.

## Resultado

El bloqueo dejó de impedir la continuación tras el desbloqueo manual del
usuario. RUN-065 se detuvo por el error de paquete descrito en la limitación
56; no se atribuye ese fallo al estado de pantalla. No se intentó eludir la
autenticación.

## Limitaciones pendientes

- Si el teléfono vuelve a dormir y muestra el keyguard, solicitar al usuario
  que lo desbloquee manualmente antes de continuar.
- Al terminar RUN-066 se apagó la pantalla; antes de una nueva prueba el usuario
  deberá desbloquearla manualmente si vuelve a aparecer el keyguard.

## Referencias

- [RUN-20261023-059](../metricas/runs/RUN-20261023-059/)
- [RUN-20261023-058, monitor interrumpido](../metricas/runs/RUN-20261023-058/)
- [EXEC-138](../ejecuciones/138-metricas-bomb-rush-cold-second-open-replacement-01-20261023/matriz.md)
- [RUN-20261023-065](../metricas/runs/RUN-20261023-065/): pantalla despierta y desbloqueada antes del intento; instalación detenida por la limitación 56.
- [RUN-20261023-066](../metricas/runs/RUN-20261023-066/): Pixel permaneció despierto y desbloqueado durante las dos fases.

## Ejecuciones asociadas

- [EXEC-138](../ejecuciones/138-metricas-bomb-rush-cold-second-open-replacement-01-20261023/matriz.md): instalación completa; pantalla T+60 negra, Pixel bloqueado en comprobación posterior y monitor detenido a T+166 s.
- [EXEC-144](../ejecuciones/144-metricas-bomb-rush-cold-second-open-trial-06-20261023/matriz.md): el usuario desbloqueó el Pixel; preflight confirmó pantalla despierta y sin keyguard antes de la instalación fría fallida por metadatos.
- [EXEC-145](../ejecuciones/145-metricas-bomb-rush-cold-second-open-trial-06-retry-01-20261023/matriz.md): ambas fases se realizaron despierto y sin keyguard; pantalla apagada manualmente al terminar.
