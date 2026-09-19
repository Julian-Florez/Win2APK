# 34. Firma incompatible durante una actualización incremental

## Descripción

La primera APK del cambio de icono no pudo actualizar la aplicación existente
con `adb install -r`. Android rechazó el paquete porque la APK nueva y la
instalada tenían certificados diferentes. El bloqueo apareció antes de
reemplazar el paquete y no produjo una desinstalación ni una limpieza de datos.

## Contexto técnico

- Paquete: `com.cuphead`.
- Versión: `versionCode=48`.
- Dispositivos en los que se observó el rechazo: Pixel 9a y Lenovo TB-J606F.
- Método solicitado: actualización incremental, sin reemplazar los datos del
  juego.
- APK rechazada: firma generada desde `$HOME/.config/.android/debug.keystore`.
- Firma compatible localizada: `$HOME/.android/debug.keystore`.
- Ejecución relacionada: [EXEC-046](../ejecuciones/46-actualizacion-incremental-icono-v48-cuatro-dispositivos-20260919/matriz.md).

## Reproducción o evidencia

El instalador devolvió literalmente:

```text
INSTALL_FAILED_UPDATE_INCOMPATIBLE: Existing package com.cuphead signatures do not match newer version; ignoring!
```

La operación utilizada fue:

```text
adb -s <serial-adb> install -r app-debug.apk
```

La misma condición se reprodujo en `lenovo-tb-j606f`. La evidencia completa está en
el [log de EXEC-046](../ejecuciones/46-actualizacion-incremental-icono-v48-cuatro-dispositivos-20260919/logs/instalacion-incremental.log).

## Impacto

Android no permite actualizar una aplicación manteniendo sus datos cuando el
certificado de firma no coincide, aunque el `applicationId` y el
`versionCode` sean iguales. La alternativa destructiva sería desinstalar y
reinstalar el paquete, lo que no se usó en esta prueba porque podía poner en
riesgo los datos privados y el rootfs de Cuphead.

## Análisis técnico

La firma que rechazó Android correspondía al almacén de depuración configurado
por el entorno actual. La firma de la instalación existente se identificó como
el certificado SHA-256
`6dd429199ee34b21a52d219d2eeff6b4fc4669dece1b46a91fbfce54bc32b8bd`, asociado
al almacén `$HOME/.android/debug.keystore`. La diferencia de
certificados, y no el icono, el target SDK ni los datos del juego, explica el
rechazo.

## Solución aplicada

Se reconstruyó la misma APK usando de forma temporal el almacén de firma que ya
correspondía a la instalación:

```text
./gradlew :app:assembleDebug --no-daemon --console=plain \
  -Pandroid.injected.signing.store.file=$HOME/.android/debug.keystore \
  -Pandroid.injected.signing.key.alias=<alias-configurado-localmente> \
  -Pandroid.injected.signing.store.password=<credencial-local-no-versionada> \
  -Pandroid.injected.signing.key.password=<credencial-local-no-versionada>
```

Las credenciales se omitieron deliberadamente y las propiedades no se guardaron
en el repositorio. Después se ejecutó
`adb install -r` secuencialmente en los cuatro dispositivos.

## Resultado

La APK compatible se instaló con `Success` en Pixel 9a, Lenovo TB-J606F,
Redmi Note 8 y Xiaomi Mi A3. El tamaño de `files` permaneció sin cambios:
6713230 KiB en Pixel, 6734746 KiB en la tablet, 6734746 KiB en Redmi y
6734778 KiB en Mi A3. No se lanzó el juego en esta ejecución.

## Limitaciones pendientes

- La solución depende de conservar el almacén de firma original; no debe
  copiarse al repositorio ni distribuirse como parte del proyecto.
- Para una publicación externa hace falta definir un keystore de distribución
  gestionado y mantenerlo para todas las actualizaciones.
- La ejecución verifica instalación y persistencia, pero no demuestra que el
  icono aparezca correctamente en cada launcher ni que Cuphead arranque; esas
  verificaciones son independientes.

## Referencias

- [Android: firma de aplicaciones](https://developer.android.com/studio/publish/app-signing)
- [Evidencia de APK y certificado](../ejecuciones/46-actualizacion-incremental-icono-v48-cuatro-dispositivos-20260919/evidencias/metadatos-apk-20260919.txt)

## Ejecuciones asociadas

- [EXEC-046: actualización incremental en cuatro dispositivos](../ejecuciones/46-actualizacion-incremental-icono-v48-cuatro-dispositivos-20260919/matriz.md)
