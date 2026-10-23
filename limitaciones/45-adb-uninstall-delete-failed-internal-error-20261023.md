# 45. `adb uninstall` devuelve `DELETE_FAILED_INTERNAL_ERROR` durante ensayo frío

## Descripción

En `RUN-20261023-001` el comando de desinstalación de `org.win2apk.testapp` terminó con código 1 y devolvió literalmente `Failure [DELETE_FAILED_INTERNAL_ERROR]`. El script comprobó después que `pm path` no devolviera rutas y bundletool instaló el APKS, pero el estado previo del paquete no se registró. Por ello, no se puede acreditar que este intento comenzara con el paquete ausente ni que fuera una instalación desde cero.

## Contexto técnico

- Dispositivo: Lenovo TB-J606F (`lenovo-tb-j606f`), serial no persistido en este informe.
- Sistema observado: Android 16; API, ABI, GPU y demás características en `metricas/runs/RUN-20261023-001/dispositivos.csv`.
- Paquete: `org.win2apk.testapp`.
- APKS: `win2apk-test-0.1.0.apks`; SHA-256 `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1`.
- Bundletool: `1.18.3`.

## Reproducción o evidencia

1. Se ejecutó `cold_install.py` con la barrera `ELIMINAR-COMPLETO` autorizada.
2. `uninstall.log` contiene exactamente:

   ```text
   Failure [DELETE_FAILED_INTERNAL_ERROR]
   ```

3. El proceso devolvió código 1. La comprobación posterior a la desinstalación no encontró rutas del paquete (`pm path` vacío), y `bundletool install-apks` instaló correctamente el artefacto en 36.406 s.
4. `install-apks.log` contiene exactamente:

   ```text
   run-as: package not debuggable: org.win2apk.testapp
   Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules. If you see legacy versions of dynamic feature modules installed try to uninstall and install the app again.
   ```

5. El muestreo de la app y su segunda apertura completaron sus ventanas de 300 s; esto acredita observación funcional, pero no resuelve el estado previo de la instalación fría.

## Impacto

La primera fase no cuenta como ensayo de instalación desde cero porque el estado previo y la eliminación completa de datos no pueden demostrarse. Las métricas de apertura y reapertura se conservan como evidencia exploratoria. Se requiere una repetición fría válida para completar el número de ensayos exigido.

## Análisis técnico

La desaparición del paquete en `pm path` después del comando demuestra que no quedó instalado para el usuario consultado antes de bundletool, pero no demuestra si ya estaba ausente al inicio ni si el error interno dejó datos residuales. El aviso de bundletool sobre `local_testing` es una advertencia separada: la instalación terminó con código 0 y el paquete quedó instalado. No hay evidencia suficiente para atribuir ambos mensajes a una causa común.

## Solución aplicada

Se conservaron sin alteración ambos logs. Se marcó el paso de desinstalación como fallido, el ensayo principal como instalación fría no acreditada y la fase de reapertura como completada; sus resultados están separados en `second-open/` sin crear otro EXEC ni duplicar catálogos.

## Resultado

La UI de WinTest fue visible en las capturas T+60 de ambas aperturas. La reapertura registró primer frame a 11.371 s del lanzamiento. La validez fría queda sin acreditar y requiere una repetición que registre el estado del paquete antes de desinstalar y verifique el borrado correctamente.

## Limitaciones pendientes

- No se conoce el estado de `org.win2apk.testapp` antes de comenzar el ensayo.
- No se ha determinado la causa de `DELETE_FAILED_INTERNAL_ERROR`.
- El aviso de limpieza de `local_testing` de bundletool debe seguir documentándose por separado.

## Referencias

- [Log de desinstalación](../metricas/runs/RUN-20261023-001/logs/lenovo-tb-j606f/uninstall.log)
- [Log de instalación bundletool](../metricas/runs/RUN-20261023-001/logs/lenovo-tb-j606f/install-apks.log)
- [CSV de instalación](../metricas/runs/RUN-20261023-001/instalaciones.csv)
- [Resumen de reapertura](../metricas/runs/RUN-20261023-001/second-open/resumen.csv)

## Ejecuciones asociadas

- [EXEC-080](../ejecuciones/80-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md) / [RUN-20261023-001](../metricas/runs/RUN-20261023-001/)
