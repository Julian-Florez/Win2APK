# Asset packs instalados como APK assets no tienen ruta directa para Wine

## Descripción

El prototipo de acceso directo consulta Play Asset Delivery, pero la instalación local generada por bundletool expone los packs de Cuphead como assets dentro de APKs. Android devuelve `path=null` y `assetsPath=null`; Winlator no puede presentar esos assets como un árbol POSIX sin copiar los archivos o implementar una capa virtual.

## Evidencia

La ejecución [EXEC-015](../ejecuciones/15-diagnostico-acceso-directo-assetpack/matriz.md) registró:

```text
pack=cuphead_data_01 storageMethod=1 path=null assetsPath=null
pack=cuphead_data_02 storageMethod=1 path=null assetsPath=null
pack=cuphead_data_03 storageMethod=1 path=null assetsPath=null
```

La misma ejecución confirmó que el fallback extraído conserva el arranque de Cuphead.

## Impacto

No es válido crear un enlace simbólico a `assetsPath` en esta variante. El requisito de una sola copia física no se resuelve cambiando únicamente `ContainerManager` o `TarCompressorUtils`.

## Opciones pendientes

1. Probar una distribución PAD que entregue `STORAGE_FILES` y crear un árbol de enlaces de solo lectura.
2. Diseñar una capa virtual de archivos que traduzca las aperturas de Wine hacia `AssetManager`/APK assets.
3. Mantener el fallback de extracción segmentada para bundletool y dispositivos donde no haya ruta directa.

## Estado

Reproducida en la instalación local con bundletool; acceso directo por ruta no viable en esta configuración.
