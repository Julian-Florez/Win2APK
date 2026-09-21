# 39. Firma incompatible al reinstalar la variante UI Preview

## Descripción

Dos intentos de instalación fría de la variante `com.win2apk.ui.preview` no
llegaron a iniciar la aplicación porque el paquete existente tenía una firma
distinta de la colección APKS recién generada.

## Contexto técnico

- Fecha: 2026-09-20.
- Dispositivos: Redmi Note 8 y Lenovo TB-J606F, Android 16/API 36, `arm64-v8a`.
- Artefacto con el que se reprodujo: `dist/ui-preview/win2apk-ui-preview-material3-preview.apks`.
- El primer orquestado también usó el valor predeterminado `com.cuphead` en vez
  de `com.win2apk.ui.preview`, por lo que no retiró el paquete correcto antes
  de instalar.

## Reproducción o evidencia

El log de bundletool conserva literalmente:

```text
INSTALL_FAILED_UPDATE_INCOMPATIBLE: Existing package com.win2apk.ui.preview signatures do not match newer version; ignoring!
```

La evidencia está en [RUN-20260920-007](../metricas/runs/RUN-20260920-007/logs/redmi-note-8/install-apks.log)
y en el log equivalente de Lenovo.

## Impacto

La ejecución no produjo muestras ni capturas T+60 y no puede usarse para
evaluar la interfaz. La instalación correcta requiere desinstalar el paquete
exacto o conservar la misma clave de firma.

## Análisis técnico

El paquete instalado era `com.win2apk.ui.preview`, pero la automatización de
los primeros intentos esperaba `com.cuphead`. Al no eliminar el paquete real,
Android comparó certificados y rechazó la actualización. La causa de la firma
distinta es la selección de almacenes de depuración entre compilaciones; no se
atribuye al layout Material 3.

## Solución aplicada

Se generó una colección APKS con la firma persistente del CLI y se ejecutó el
flujo frío indicando explícitamente `--package com.win2apk.ui.preview`.

## Resultado

Resuelta experimentalmente en [EXEC-057](../ejecuciones/57-metricas-container-settings-navigation-fix-final-20260920/matriz.md)
y verificada de nuevo en [EXEC-058](../ejecuciones/58-metricas-container-settings-permanent-navigation-layout-20260920/matriz.md),
ambas con instalación exitosa en los dos dispositivos.

## Limitaciones pendientes

- Mantener el identificador de paquete explícito en futuras ejecuciones de la
  variante temporal.
- No extrapolar la firma persistente de esta variante a otros paquetes.

## Referencias

- [RUN-20260920-006](../metricas/runs/RUN-20260920-006/)
- [RUN-20260920-007](../metricas/runs/RUN-20260920-007/)
- [RUN-20260920-008](../metricas/runs/RUN-20260920-008/)

## Ejecuciones asociadas

- [EXEC-055](../ejecuciones/55-metricas-container-settings-navigation-fix-20260920/matriz.md)
- [EXEC-056](../ejecuciones/56-metricas-container-settings-navigation-fix-final-20260920/matriz.md)
- [EXEC-057](../ejecuciones/57-metricas-container-settings-navigation-fix-final-20260920/matriz.md)
- [EXEC-058](../ejecuciones/58-metricas-container-settings-permanent-navigation-layout-20260920/matriz.md)
