# 38. Material Components 1.14.0 requiere un AGP superior al del proyecto

## Descripción

La primera compilación de la migración Material 3 intentó usar Material
Components 1.14.0. El proyecto utiliza Android Gradle Plugin 8.5.1 y el
metadata de la dependencia arrastra una versión de AndroidX Core que exige AGP
8.6 o posterior.

## Contexto técnico

- Fecha: 2026-09-20.
- Proyecto: módulo `winlator/app/app`.
- Toolchain observado: Gradle 8.7, Android Gradle Plugin 8.5.1, compile SDK 36.
- Dependencia probada: `com.google.android.material:material:1.14.0`.
- Dependencia adoptada: `com.google.android.material:material:1.12.0`.

## Reproducción o evidencia

La tarea `checkDebugAarMetadata` terminó con el mensaje exacto:

```text
androidx.core:core/core-ktx:1.16.0 requires AGP8.6
```

La misma compilación indicó que el proyecto actual usa AGP 8.5.1. No se
actualizó AGP en esta iteración porque hacerlo amplía el cambio de toolchain y
no es necesario para probar Material 3 en Views.

## Impacto

Material Components 1.14.0 no es una opción directa para este árbol con el
toolchain actual. Una actualización conjunta de AGP, Gradle y dependencias
podría reabrir riesgos ya documentados en el empaquetado y la ejecución del
rootfs.

## Análisis técnico

El error aparece durante la verificación de metadata AAR, antes de compilar el
código de la aplicación. La limitación pertenece a la combinación de versiones
del toolchain, no a los layouts Material 3 añadidos.

## Solución aplicada

Se seleccionó Material Components 1.12.0, que permite usar `Theme.Material3`,
`MaterialCardView`, `MaterialButton`, `MaterialAlertDialogBuilder`, indicadores
de progreso y Dynamic Colors sin elevar AGP. La compilación posterior completó
con éxito y produjo APK y AAB de la variante temporal.

## Resultado

Resuelta experimentalmente para la migración actual mediante una versión
compatible de Material Components. No se evaluó todavía la actualización del
toolchain a AGP 8.6 o posterior.

## Limitaciones pendientes

- Revisar una actualización de AGP solo en una rama o experimento aislado.
- Mantener la versión de Material y sus transitivas bajo la matriz de versiones
  del proyecto mientras `targetSdk=28` siga siendo necesario para Box64.

## Referencias

- [Material Components Android](https://github.com/material-components/material-components-android)
- [Build de la variante UI](../dist/ui-preview/)

## Ejecuciones asociadas

- La compilación experimental de la variante UI precedió a [EXEC-051](../ejecuciones/51-metricas-ui-material3-preview-phone-landscape-tablet-portrait-20260920/matriz.md).
