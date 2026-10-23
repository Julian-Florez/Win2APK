# 52. Google Play Protect bloquea una instalación fría de WinTest en Pixel 9a

## Descripción

En el segundo intento de instalación fría de WinTest en el Pixel 9a, la pantalla
mostró un aviso de Google Play Protect y el paquete no apareció instalado. El
cliente de Bundletool permaneció esperando durante 551.283 s; se interrumpió
manualmente tras comprobar que el paquete seguía ausente. No se llegó a iniciar
la fase de medición de cinco minutos ni la segunda apertura. El primer intento
frío de WinTest en este dispositivo sí se completó en 60.308 s en
[RUN-20261023-047](../metricas/runs/RUN-20261023-047/). Después, el usuario
informó que desactivó Play Protect. Las instalaciones frías posteriores de
WinTest se completaron; esto no prueba que el ajuste fuera la única causa del
bloqueo inicial.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Tensor G4, Android 17/API 37, ABI `arm64-v8a`;
  inventario en [RUN-20261023-047](../metricas/runs/RUN-20261023-047/dispositivos.csv).
- Aplicación: Win2APK Test, paquete `org.win2apk.testapp`, versión 0.1.0.
- Artefacto: `win2apk-test-0.1.0.apks`; SHA-256
  `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1`.
- Instalador: Bundletool 1.18.3; APK set de 746,216,923 bytes.
- Run: `RUN-20261023-048`, `EXEC-127`; inicio de Bundletool
  `2026-10-23T19:35:22.483Z`; interrupción y retorno del cliente
  `2026-10-23T19:44:33.766Z` (551.283 s).
- No se registraron muestras de CPU/RAM/FPS/temperatura durante una fase de
  ejecución. Winlator/container: N/R.

## Reproducción o evidencia

1. Iniciar la segunda repetición fría con `run_experiment.py` y la confirmación
   de desinstalación autorizada para la campaña.
2. `adb uninstall org.win2apk.testapp` devuelve `Success`.
3. Mientras Bundletool ejecuta `install-apks`, el Pixel presenta Google Play
   Protect en primer plano. La captura muestra exactamente:
   - «Se bloqueó la app no segura».
   - «Esta app se diseñó para una versión anterior de Android, por lo que no
     incluye las protecciones de la privacidad más recientes.»
4. La jerarquía UI obtenida con `uiautomator dump` no expone controles
   accionables. `pm path org.win2apk.testapp` y la lista de paquetes no muestran
   el paquete.
5. Tras 551.283 s se envía SIGINT únicamente al cliente Bundletool. El registro
   de instalación queda con `result=failed`, `exit_code=130`; ese código refleja
   la interrupción deliberada, no un fallo interno de Winlator.

Evidencia primaria: [captura Play Protect](../metricas/runs/RUN-20261023-048/evidencias/pixel-9a/play-protect-block.png), [instalaciones y eventos CSV](../metricas/runs/RUN-20261023-048/), [log de Bundletool](../metricas/runs/RUN-20261023-048/logs/pixel-9a/install-apks.log), [matriz EXEC-127](../ejecuciones/127-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md).

## Impacto

RUN-20261023-048 no aporta una medición válida de primer frame, FPS, memoria ni
segunda apertura y no cuenta como repetición. Después del aviso del usuario,
WinTest se instaló y completó las dos fases en RUN-20261023-049 a RUN-20261023-052;
junto con RUN-20261023-047, esas son cinco repeticiones válidas. El cambio de
Play Protect fue realizado por el usuario, no por el agente.

## Análisis técnico

El aviso visible coincide con la ausencia del paquete y la espera de Bundletool.
Esto hace plausible que Play Protect haya intervenido en el flujo, pero no se
capturó una respuesta explícita de Package Manager que confirme la causa. El
texto menciona que la app fue diseñada para una versión anterior de Android; no
se dispone aquí de un registro del `targetSdkVersion` efectivo. La diferencia
entre el primer y segundo intento frío sugiere un comportamiento intermitente o
dependiente del estado de seguridad, no una incompatibilidad universal.

## Solución aplicada

Durante RUN-20261023-048 no se desactivó Play Protect ni se intentó eludir la
protección. Se detuvo el cliente que llevaba esperando varios minutos, se
conservó la captura y se registró el intento como fallido. Posteriormente el
usuario comunicó haber desactivado Play Protect; el ajuste no fue cambiado por
el agente. Las instalaciones RUN-20261023-049 a RUN-20261023-052 terminaron sin
volver a mostrar el aviso.

## Resultado

El segundo intento frío no se completó: Bundletool fue interrumpido a los
551.283 s y no hubo fase de ejecución. Los cuatro intentos fríos posteriores
de WinTest en el Pixel terminaron con éxito después del cambio informado por el
usuario. La correlación temporal es compatible con que Play Protect interviniera,
pero no determina causalidad ni elimina el registro del intento fallido. La
limitación sigue en investigación por falta de un diagnóstico explícito de
Package Manager.

## Limitaciones pendientes

- Determinar si el bloqueo se debió a Play Protect o a otra condición; no hay
  evento explícito de rechazo de Package Manager en RUN-20261023-048.
- No modificar ajustes de seguridad adicionales sin instrucción del usuario.
- Las cinco repeticiones WinTest están completadas; Cuphead y Bomb Rush siguen
  pendientes en la campaña del Pixel.

## Referencias

- [RUN-20261023-047: primer intento frío exitoso](../metricas/runs/RUN-20261023-047/)
- [RUN-20261023-048: intento interrumpido](../metricas/runs/RUN-20261023-048/)
- [RUN-20261023-049 a RUN-20261023-052: reintentos WinTest](../metricas/runs/RUN-20261023-049/)
- [EXEC-127](../ejecuciones/127-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md)
- [EXEC-128 a EXEC-131](../ejecuciones/index.md)

## Ejecuciones asociadas

- [EXEC-126](../ejecuciones/126-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md): instalación fría y dos fases de medición completadas.
- [EXEC-127](../ejecuciones/127-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md): instalación fría bloqueada; fase de medición no iniciada.
- [EXEC-128](../ejecuciones/128-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md), [EXEC-129](../ejecuciones/129-metricas-wintest-cold-second-open-trial-03-20261023/matriz.md), [EXEC-130](../ejecuciones/130-metricas-wintest-cold-second-open-trial-04-20261023/matriz.md) y [EXEC-131](../ejecuciones/131-metricas-wintest-cold-second-open-trial-05-20261023/matriz.md): reintentos fríos completados después de que el usuario informó desactivar Play Protect.
