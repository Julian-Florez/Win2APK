# 56. El paquete predeterminado de la medición fría desinstala otra aplicación

## Descripción

El intento de instalación fría de Bomb Rush Cyberfunk en Pixel 9a usó por error
`com.cuphead` como paquete objetivo. El run desinstaló ese paquete y luego
Bundletool instaló Bomb Rush correctamente, pero la validación buscó el paquete
equivocado y detuvo la medición antes de abrir el juego.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Android 17/API 37, ABI `arm64-v8a`.
- Run afectado: `RUN-20261023-065`, `EXEC-144`.
- Artefacto Bomb Rush Cyberfunk APKS, SHA-256
  `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54`.
- Paquete correcto: `com.win2apk.bombrushcyberfunk`.
- Paquete registrado por error en `run.csv`: `com.cuphead`.
- El comando omitió `--package`; el parámetro era opcional y su valor
  predeterminado era `com.cuphead`.

## Reproducción o evidencia

1. `cold_install.py` ejecutó `adb uninstall com.cuphead`; el log de
   desinstalación registra `Success`.
2. Bundletool transfirió los APK del APKS y el log terminó con `Success`. También
   emitió el aviso exacto:

   ```text
   Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules. If you see legacy versions of dynamic feature modules installed try to uninstall and install the app again.
   ```

3. `adb shell pm path com.win2apk.bombrushcyberfunk` confirmó el APK base y los
   splits ABI, idioma y densidad. El verificador consultó `com.cuphead`, no
   encontró ese paquete y registró `failed_install`, aunque Bundletool terminó
   con código 0.
4. `run_experiment.py` omitió el monitor tras ese resultado: no hay muestras,
   captura T+60 ni medición de primer frame para RUN-065.
5. La revisión del código confirmó `com.cuphead` como valor predeterminado en
   `run_experiment.py` y `create_run.py`, y `Cuphead.exe` en el monitor. No se
   comprobaba que el paquete indicado coincidiera con `run.csv` antes de
   desinstalar.

Evidencia: [RUN-20261023-065](../metricas/runs/RUN-20261023-065/),
[matriz EXEC-144](../ejecuciones/144-metricas-bomb-rush-cold-second-open-trial-06-20261023/matriz.md).

## Impacto

El ensayo no cuenta como pareja de medición. La desinstalación pudo eliminar los
datos privados locales de Cuphead en el Pixel; no se ha intentado reinstalarlo ni
se afirma que esos datos sean recuperables. Bomb Rush sí quedó instalado. Este
run no produjo actividad del juego ni muestras de rendimiento.

## Análisis técnico

La causa está confirmada: el orquestador heredó un paquete predeterminado
específico de Cuphead al utilizarse con otro artefacto. La limpieza es
destructiva y ocurre antes de instalar; luego, la comprobación `pm path` reutiliza
el mismo paquete erróneo. El aviso de Bundletool no explica `failed_install`:
ADB confirmó que Bomb Rush sí se instaló. El aviso está descrito también en la
[limitación 41](41-bundletool-local-testing-release-no-debuggable.md).

## Solución aplicada

- Se conservaron los logs y CSV del run fallido; no se alteró el dato histórico.
- `run_experiment.py` y `create_run.py` ahora exigen el paquete; el orquestador
  también exige el ejecutable Windows del juego.
- `cold_install.py` y `monitor_device.py` exigen el paquete y verifican que
  coincida con `package_name` del run antes de continuar. Una diferencia detiene
  el proceso antes de desinstalar.
- Se probó el guardado de `cold_install.py` contra RUN-065 usando un serial
  ficticio; el comando terminó con el mensaje `no se desinstaló nada` antes de
  cualquier operación ADB.
- RUN-066 repitió la instalación fría con `com.win2apk.bombrushcyberfunk` y
  `Bomb Rush Cyberfunk.exe` explícitos. Bundletool terminó en 67.629 s y la
  verificación de `pm path` confirmó el paquete correcto. Las dos fases
  produjeron datos; su resultado visual parcial se describe en EXEC-145 y no
  invalida esta verificación de paquete.

## Resultado

RUN-065 queda como intento fallido por metadatos incompatibles y sin medición
del juego. La protección impidió una desinstalación cuando el paquete no
coincidía con el run y RUN-066 instaló Bomb Rush con el paquete correcto. La
protección queda resuelta experimentalmente para esta versión de la herramienta.

## Limitaciones pendientes

- El usuario debe decidir si desea reinstalar Cuphead limpio en el Pixel; una
  reinstalación no recuperaría datos privados que Android ya haya eliminado.
- Confirmar la recuperación visual del juego por separado: RUN-066 mantuvo el
  logotipo en las capturas T+60 y en la comprobación suplementaria posterior.

## Referencias

- [Log de desinstalación](../metricas/runs/RUN-20261023-065/logs/pixel-9a/uninstall.log)
- [Log de Bundletool](../metricas/runs/RUN-20261023-065/logs/pixel-9a/install-apks.log)
- [CSV de instalación](../metricas/runs/RUN-20261023-065/instalaciones.csv)
- [RUN-065](../metricas/runs/RUN-20261023-065/)
- [RUN-066: reintento con paquete explícito](../metricas/runs/RUN-20261023-066/)
- [Skill y scripts endurecidos](../.codex/skills/win2apk-medir-dispositivos/SKILL.md)
- [Limitación 41: aviso de limpieza local-testing](41-bundletool-local-testing-release-no-debuggable.md)

## Ejecuciones asociadas

- [EXEC-144](../ejecuciones/144-metricas-bomb-rush-cold-second-open-trial-06-20261023/matriz.md): paquete incorrecto, desinstalación de Cuphead y validación fallida pese a la instalación efectiva de Bomb Rush.
- [EXEC-145](../ejecuciones/145-metricas-bomb-rush-cold-second-open-trial-06-retry-01-20261023/matriz.md): paquete explícito, instalación correcta y monitor completo; resultado visual parcial.
