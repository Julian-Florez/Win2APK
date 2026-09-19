# 30. Inestabilidad ADB del Redmi durante la transferencia local-testing

## Descripción

El Redmi Note 8 perdió la sesión ADB mientras `bundletool install-apks` copiaba
los splits y archivos de local-testing del APKS completo.

## Contexto técnico

- Aplicación: `com.cuphead`, v45.
- Artefacto: APKS local-testing de 6.160.286.207 bytes.
- Dispositivo: Redmi Note 8, Android 16, arm64-v8a.
- Orden de la prueba: Pixel → Lenovo TB-J606F → Redmi → Mi A3.

## Reproducción o evidencia

En `EXEC-036`, el primer intento terminó después de 173,366 s con el mensaje
exacto:

`Error during Sync: EOF`

El segundo intento terminó después de 18,636 s con:

`device offline`

Los mensajes completos están en
[`install-apks.log`](../metricas/runs/RUN-20260919-004/logs/redmi-note-8/install-apks.log).
El dispositivo desapareció de `adb devices` durante el segundo intento.

## Impacto

La primera ejecución no pudo verificar que todos los packs hubieran quedado
disponibles y no debía iniciar el cronómetro de juego con esa instalación parcial.

## Análisis técnico

La evidencia apunta a una interrupción del transporte ADB durante `sync`; no se
observó falta de espacio. Tras reconectar el cable y mantener el estado `device`,
la instalación posterior terminó correctamente en 194,668 s.

## Solución aplicada

Se dejó que bundletool terminara sin paralelizar otro dispositivo, se reconectó
el Redmi y se repitió la desinstalación e instalación completa. La ejecución
conserva los intentos fallidos y el reintento exitoso en `instalaciones.csv`.

## Resultado

Reproducida en dos intentos y resuelta experimentalmente con un transporte ADB
estable. No se debe usar el tiempo de los intentos EOF/offline como tiempo de
instalación válido.

## Limitaciones pendientes

La skill no puede garantizar la estabilidad física del cable, puerto o controlador
USB. Una prueba futura debe registrar el estado ADB antes y después de cada pack.

## Referencias

- [Log de instalación](../metricas/runs/RUN-20260919-004/logs/redmi-note-8/install-apks.log)
- [Instalaciones cronometradas](../metricas/runs/RUN-20260919-004/instalaciones.csv)

## Ejecuciones asociadas

- [EXEC-036](../ejecuciones/36-metricas-titulo-instalacion-fria-5-min-20260919/matriz.md)

