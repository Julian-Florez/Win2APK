# 33. `targetSdk=36` bloquea la ejecución de Box64 desde el rootfs

## Descripción

La compilación v47 dejó de iniciar Cuphead en el Pixel 9a. La aplicación
permanecía en `Preparing application...` y el proceso de Box64 no podía
ejecutar el binario extraído en el directorio privado de la aplicación. El
efecto visible para el usuario fue que la aplicación no terminaba de iniciar o
se cerraba al intentar abrir el juego.

## Contexto técnico

- Publicación que reprodujo el problema: v47.
- `targetSdkVersion`: 36.
- Dispositivo: Pixel 9a, Android 17/API 37, `arm64-v8a`.
- Ruta del binario: `/data/data/com.cuphead/files/rootfs/usr/local/bin/box64`.
- Prueba: instalación fría por bundletool, [EXEC-039](../ejecuciones/39-metricas-modern-api36-pagesizecompat-v47-pixel-cold-install-20260919/matriz.md).

## Reproducción o evidencia

El logcat registró literalmente:

```text
avc:  denied  { execute_no_trans } for  path="/data/data/com.cuphead/files/rootfs/usr/local/bin/box64" dev="dm-79" ino=1496485 scontext=u:r:untrusted_app_34:s0:c186,c257,c512,c768 tcontext=u:object_r:app_data_file:s0:c186,c257,c512,c768 tclass=file permissive=0 app=com.cuphead
```

La misma ejecución registró intentos de `WinlatorProcess: Starting ... box64`,
pero no observó `Cuphead.exe` durante los 300 segundos de monitorización. La
captura T+60 quedó en la pantalla de preparación.

## Impacto

El diseño actual necesita ejecutar Box64, Wine y sus binarios auxiliares desde
un rootfs instalado en el almacenamiento privado de la aplicación. Subir el
target API al rango moderno cambia las reglas SELinux aplicadas a esa ruta y
rompe el arranque del entorno de compatibilidad. El problema no es específico
del controlador gráfico Mali.

## Análisis técnico

La evidencia es consistente con la política SELinux de Android para aplicaciones
no confiables: las reglas históricas permiten la ejecución desde el directorio
privado para targets antiguos, mientras que las reglas posteriores restringen
esa transición. La referencia de AOSP documenta la separación entre los grupos
de target API 26–28 y las aplicaciones posteriores:
[reglas `untrusted_app` de AOSP](https://android.googlesource.com/platform/system/sepolicy/%2B/5e5228137248e04441b74e98e33a1c23f524c12e/private/untrusted_app_25.te).

## Solución aplicada

La v48 restaura `targetSdkVersion=28`, conserva `compileSdk=36` y mantiene
`android:pageSizeCompat="enabled"`. No se eliminaron las bibliotecas de audio,
MIDI ni Vulkan como forma de ocultar el problema.

## Resultado

En la prueba fría de v48 en el Pixel 9a, `Cuphead.exe` apareció a los
96.219 segundos desde el inicio de la monitorización y permaneció observable
hasta T+300; la aplicación tuvo una razón de vida de 1.000. La misma v48 fue
instalada posteriormente en Lenovo TB-J606F, Redmi Note 8 y Mi A3; el usuario
confirmó que Cuphead terminó ejecutándose en los cuatro dispositivos.

La corrección resuelve experimentalmente la regresión de ejecución observada
con v47, pero no convierte la arquitectura actual en una aplicación compatible
con `targetSdk>=29`. El diálogo de páginas de 16 KB todavía puede aparecer en
el Pixel y es una limitación independiente.

## Limitaciones pendientes

- Mantener target API 28 genera advertencias de aplicación antigua en Android
  moderno y no satisface por sí solo los requisitos futuros de publicación.
- `pageSizeCompat` no recompila las bibliotecas nativas precompiladas ni
  garantiza ocultar el diálogo en todos los dispositivos.
- La migración correcta a un target moderno requiere reubicar o rediseñar la
  ejecución de Box64/Wine fuera de una ruta `app_data_file` no ejecutable; no se
  implementó en esta corrección.
- Los tiempos de arranque son distintos por dispositivo y la captura T+60 de
  las pruebas automatizadas no representa necesariamente la pantalla final.

## Referencias

- [Limitación 32: advertencia de páginas 16 KB](./32-advertencia-paginas-16kb-precompilados.md)
- [AOSP: política `untrusted_app_25.te`](https://android.googlesource.com/platform/system/sepolicy/%2B/5e5228137248e04441b74e98e33a1c23f524c12e/private/untrusted_app_25.te)
- [Compatibilidad con tamaños de página de 16 KB de Android](https://developer.android.com/guide/practices/page-sizes)

## Ejecuciones asociadas

- [EXEC-039 / RUN-20260919-007: v47 en Pixel, regresión](../ejecuciones/39-metricas-modern-api36-pagesizecompat-v47-pixel-cold-install-20260919/matriz.md)
- [EXEC-041 / RUN-20260919-009: v48 en Pixel](../ejecuciones/41-metricas-legacy-exec-api28-pagesizecompat-v48-pixel-cold-install-20260919/matriz.md)
- [EXEC-042 / RUN-20260919-010: v48 en Lenovo](../ejecuciones/42-metricas-legacy-exec-api28-pagesizecompat-v48-lenovo-cold-install-20260919/matriz.md)
- [EXEC-043 / RUN-20260919-011: v48 en Redmi](../ejecuciones/43-metricas-legacy-exec-api28-pagesizecompat-v48-redmi-cold-install-20260919/matriz.md)
- [EXEC-044 / RUN-20260919-012: v48 en Mi A3](../ejecuciones/44-metricas-legacy-exec-api28-pagesizecompat-v48-mi-a3-cold-install-20260919/matriz.md)
- [EXEC-045: verificación posterior de `Cuphead.exe` en los cuatro dispositivos](../ejecuciones/45-verificacion-posterior-procesos-cuphead-v48-20260919/matriz.md)
