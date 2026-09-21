# 41. Aviso de bundletool al limpiar `local_testing` en release no depurable

## Descripción

Durante la instalación fría del paquete de Bomb Rush Cyberfunk, `bundletool`
devolvió un aviso sobre la limpieza de los splits de prueba local. La
comprobación ADB posterior confirmó que el paquete sí quedó instalado en los
tres dispositivos.

## Contexto técnico

- Ejecuciones: `EXEC-068` / `RUN-20260921-003` y `EXEC-069` / `RUN-20260921-004`.
- Artefacto: `bomb-rush-cyberfunk-gog-56774571391351451.apks`.
- SHA-256: `63efdfd640e76275c48cf496d814cf484b5347de741d4fb66518845b3eb7c1d1`.
- Paquete: `com.win2apk.bombrushcyberfunk`.
- Dispositivos: Redmi Note 8, Xiaomi Mi A3 y Lenovo TB-J606F, Android 16.

## Reproducción o evidencia

El mensaje exacto conservado en cada log de instalación fue:

```text
Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules. If you see legacy versions of dynamic feature modules installed try to uninstall and install the app again.
```

Los logs están en [RUN-20260921-003](../metricas/runs/RUN-20260921-003/). Después
del mensaje, `adb shell pm path com.win2apk.bombrushcyberfunk` devolvió el APK
base y los splits ABI/idioma/densidad en los tres dispositivos; `dumpsys
package` mostró `versionName=gog-56774571391351451`.

## Impacto

El script automático clasificó los tres pasos como `failed` porque el proceso
de instalación no terminó con la condición esperada. Esa clasificación no
describe el estado final observado por ADB en esta ejecución.

## Análisis técnico

El log muestra que el instalador llegó a usar `run-as` para retirar el árbol de
splits locales, pero el artefacto release no es depurable y el dispositivo
respondió `run-as: package not debuggable`. La relación causal se considera
confirmada para el aviso; no se afirma que exista una versión antigua de los
asset packs porque no se inspeccionó ese árbol con privilegios adicionales.

## Solución aplicada

No se modificó el artefacto. Se verificó el resultado real con `pm path`,
`dumpsys package` y el arranque de la aplicación en cada dispositivo.

## Resultado

Estado: reproducida; instalación verificada pese al aviso. La tablet llegó a la
pantalla de título, el Redmi mostró la pantalla de carga y el Mi A3 mantuvo el
proceso de la aplicación activo con una captura negra.

## Limitaciones pendientes

- El instalador automático debe distinguir entre un aviso de limpieza local y
  una instalación realmente ausente.
- No se probó el ciclo conectar/desconectar de un control físico en esta
  ejecución.
- La medición temporal quedó por debajo de la ventana nominal de 90 segundos.

## Referencias

- [Matriz EXEC-068](../ejecuciones/68-metricas-gamepad-conditional-install-20260921/matriz.md)
- [Log Redmi](../metricas/runs/RUN-20260921-003/logs/redmi-note-8/install-apks.log)
- [Log Mi A3](../metricas/runs/RUN-20260921-003/logs/mi-a3/install-apks.log)
- [Log Lenovo](../metricas/runs/RUN-20260921-003/logs/lenovo-tb-j606f/install-apks.log)

## Ejecuciones asociadas

- [EXEC-068](../ejecuciones/68-metricas-gamepad-conditional-install-20260921/matriz.md)
- [EXEC-069](../ejecuciones/69-metricas-gamepad-material3-install-20260921/matriz.md)
