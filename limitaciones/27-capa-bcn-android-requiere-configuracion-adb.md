# 27. La capa BCn Android del Pixel requiere configuración ADB

## Descripción

La combinación que recuperó imagen y estabilizó la memoria en el Pixel 9a no es todavía autónoma. La prueba necesitó copiar dos bibliotecas al directorio privado de `com.cuphead` y habilitar una capa Vulkan mediante ajustes globales de depuración GPU ejecutados por ADB.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Tensor G4 / Mali-G715, Android API 37.
- Publicación: v44, `versionCode=44`.
- Perfil: Vortek 2.1 + Gladio 1.0 + DXVK-Sarek 1.13.0 + Leegao BCn ETC2.
- Capa: `VK_LAYER_BCN_BCnLayer`.
- Ejecución: [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md).

## Reproducción o evidencia

La variante funcional configuró estos valores:

```text
enable_gpu_debug_layers=1
gpu_debug_app=com.cuphead
gpu_debug_layers=VK_LAYER_BCN_BCnLayer
gpu_debug_layer_app=com.cuphead
```

El log del segundo arranque incluyó:

```text
GPU debug layers enabled for com.cuphead
Vulkan debug layer list: VK_LAYER_BCN_BCnLayer
added global layer 'VK_LAYER_BCN_BCnLayer' from library '/data/user/0/com.cuphead/libVkLayer_BCN_BCnLayer.so'
Loaded layer VK_LAYER_BCN_BCnLayer
```

La evidencia completa está en [android-layer-result.md](../ejecuciones/31-restauracion-perfil-historico-pixel/logs/android-layer-result.md).

## Impacto

Un APK instalado por un usuario normal no puede reproducir esta preparación tal como fue ensayada. Por tanto, v44 sirve como prueba del mecanismo gráfico, pero no satisface todavía el requisito de instalar y ejecutar sin preparación ADB.

## Análisis técnico

La carga mediante `GraphicsEnvironment` está controlada por ajustes globales del sistema. La prueba no verificó que una aplicación normal pueda escribirlos, y no se debe asumir que disponer de las bibliotecas dentro del APK sea suficiente para que el cargador las active. La alternativa debe validar de forma explícita el descubrimiento y encadenamiento de la capa sin privilegios externos.

## Solución aplicada

Para aislar la causa se usó ADB como procedimiento temporal. Se conservaron los hashes históricos:

- `libbcn_layer.so`: `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`;
- `libVkLayer_BCN_BCnLayer.so`: `053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565`.

## Resultado

La preparación manual funcionó en el Pixel probado: imagen visible, memoria estabilizada y procesos vivos más allá de 90 s. La limitación de autonomía permanece detectada.

## Limitaciones pendientes

- Empaquetar las bibliotecas para la ABI correspondiente y comprobar su extracción o carga desde el APK.
- Probar activación explícita desde el cargador Vulkan/Vortek sin `settings put global`.
- Confirmar el comportamiento desde una instalación limpia y sin acceso ADB previo.
- Conservar una ruta separada para Adreno; este mecanismo solo fue probado en Mali-G715.

## Referencias

- [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md)
- [Decisión sobre la restauración histórica](../documentacion/08-decision-capa-bcn-android-pixel.md)

## Ejecuciones asociadas

- [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md)
