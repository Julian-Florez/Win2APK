# Resultado de la capa BCn cargada por Android

## Cambio aislado

Se conservaron Vortek + Gladio, DXVK-Sarek 1.13.0, resolución 1280x720 y la política ETC2. Solo cambió la ruta de integración:

- se renombraron de forma recuperable la biblioteca y el manifiesto BCn del rootfs;
- se instalaron `libbcn_layer.so` y el shim `libVkLayer_BCN_BCnLayer.so` en el directorio privado de la aplicación;
- se habilitó `VK_LAYER_BCN_BCnLayer` mediante la configuración global de depuración GPU de Android para `com.cuphead`.

## Integridad de los binarios instalados

```text
fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2  libbcn_layer.so
053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565  libVkLayer_BCN_BCnLayer.so
```

## Evidencia del cargador Android

En el segundo arranque, con el búfer de log limpio, se conservaron estas líneas:

```text
09-18 22:25:09.829 I GraphicsEnvironment: GPU debug layers enabled for com.cuphead
09-18 22:25:09.880 I GraphicsEnvironment: Vulkan debug layer list: VK_LAYER_BCN_BCnLayer
09-18 22:25:09.914 D vulkan  : added global layer 'VK_LAYER_BCN_BCnLayer' from library '/data/user/0/com.cuphead/libVkLayer_BCN_BCnLayer.so'
09-18 22:25:09.916 I vulkan  : Loaded layer VK_LAYER_BCN_BCnLayer
09-18 22:25:10.034 I Win2APKGraphicsProfile: device=Google/Pixel 9a hardware=tegu renderer=Mali-G715 vendor=ARM profile=Mali/unknown / Vortek + Gladio / DXVK-Sarek 1.13.0 + Leegao BCn ETC2 graphicsDriver=vortek,gladio dxwrapper=dxvk
```

## Permanencia y memoria

Durante una ventana aproximada de 64 a 122 s ambos procesos permanecieron vivos. Las doce muestras cada cinco segundos dieron:

- `MemAvailable`: entre `1274732 KiB` y `1322812 KiB`;
- `ION_heap`: entre `1323736 KiB` y `1324000 KiB`;
- GPU: entre `418308 KiB` y `444416 KiB`.

En el corte posterior, con el juego todavía visible:

- proceso Android: PSS `1237803 KiB`, RSS `1334224 KiB`, Graphics `1124724 KiB`;
- `MemAvailable`: `1385216 KiB`;
- `ION_heap`: `1334084 KiB`;
- `Cuphead.exe`: PID `3391` y vivo;
- no apareció un evento `LOW_MEMORY` posterior al de la variante rootfs de las `22:17:57.081`.

Un segundo arranque reprodujo la carga de la capa y conservó `com.cuphead` y `Cuphead.exe` vivos a los 45 s. La captura volvió a mostrar el contenido del juego.

## Payload

- Solo se localizó un `Cuphead.exe`: `files/rootfs/home/xuser-1/.wine/drive_c/Cuphead/Cuphead.exe`.
- Tamaño observado del árbol `Cuphead`: `5847511447` bytes mediante `du -sb`.
- El staging `local_testing` estaba ausente.

El valor de `du` no se usa como sustituto del marcador lógico histórico de 815 archivos y 5847372363 bytes, porque mide metadatos y estructura de forma distinta. La ausencia de un segundo ejecutable solo demuestra que no se encontró una segunda instalación del juego dentro del directorio privado en este corte.

## Alcance

La prueba confirma la ruta técnica en este Pixel, pero todavía depende de comandos ADB para configurar las capas GPU globales. No constituye aún una instalación autónoma para el usuario final ni una validación de sesión de juego prolongada.
