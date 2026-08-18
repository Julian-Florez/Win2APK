# Limitación 05: inicio de Winlator Core en una APK normal sin root

- **Proyecto:** Win2APK
- **Estado:** aceptada para el diseño; implementación pendiente
- **Fecha de registro:** 2026-08-18

## Limitación

Una APK Android normal no puede ejecutar código propio ni abrir automáticamente una actividad justo después de que el sistema termine de instalarla. Android tampoco permite preparar arbitrariamente el almacenamiento privado de la aplicación durante la instalación sin que la aplicación sea ejecutada.

El proyecto exige además que los dispositivos no tengan root.

## Decisión adoptada

El flujo aceptado será:

1. El usuario instala la APK.
2. El usuario toca el icono una vez.
3. Winlator Core muestra una carga mínima.
4. El núcleo prepara rootfs, `Container-1`, la carpeta Windows y el shortcut sin mostrar opciones.
5. El núcleo abre la aplicación Windows.

No se intentará ejecutar código durante la instalación ni se dependerá de root, permisos de sistema o un instalador privilegiado.

## Consecuencia

La afirmación verificable será “un toque inicial y después ejecución automática”, no “instalación y ejecución sin ningún toque”. Esta restricción aplica a la distribución mediante instalador normal; durante la depuración se usará `adb install`.

## Limitaciones relacionadas

- La primera preparación puede tardar mientras se extraen el rootfs y el contenedor.
- La configuración se gestionará antes de compilar mediante JSON.
- El `applicationId` se define en compilación; cambiarlo crea otra identidad de aplicación Android.

## Referencias

- [Plan de Winlator Core](../documentacion/02-plan-winlator-core.md)
- [Especificación de Winlator Core](../especificaciones/winlator-core.md)
