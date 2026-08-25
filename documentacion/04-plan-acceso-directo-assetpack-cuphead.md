# 04. Plan para ejecutar Cuphead directamente desde los datos del AAB

- **Fecha:** 2026-08-24
- **Estado:** diagnóstico realizado; acceso directo por ruta no viable en bundletool local
- **Objetivo:** evitar que Winlator extraiga una segunda copia de Cuphead al prefijo Wine y conservar una sola copia física de los datos del juego.
- **Rama de implementación Android:** `codex/direct-assetpack-cuphead` en [winlator-app](https://github.com/Julian-Florez/winlator-app/tree/codex/direct-assetpack-cuphead), commit `d3c9262`.

## Contexto actual

La ejecución [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md) demostró que el AAB segmentado se puede instalar con bundletool y ejecutar. El diseño actual contiene tres asset packs con partes de `cuphead.tzst`; en el primer arranque Winlator concatena las partes y las extrae a:

```text
files/rootfs/home/xuser-1/.wine/drive_c/Cuphead
```

Esto deja simultáneamente los asset packs instalados y la copia extraída. El objetivo de este plan es cambiar el proveedor de datos y el mapeo del contenedor, no eliminar manualmente archivos administrados por Android.

## Restricción técnica principal

Un asset dentro de un APK no es una carpeta POSIX normal. Android puede exponerlo mediante `AssetManager`, pero Wine/Box64 necesita abrir rutas ordinarias como `C:\Cuphead\Cuphead.exe`. La documentación de Play Asset Delivery distingue dos casos:

1. `STORAGE_FILES`: existe una ruta de carpeta (`assetsPath`) que puede leerse como archivos.
2. `APK_ASSETS`: el pack permanece dentro de un APK y debe leerse mediante `AssetManager`; no hay una ruta de carpeta directa.

En la prueba local actual, bundletool instaló `split_cuphead_data_01.apk`, `_02.apk` y `_03.apk`. Por tanto, no se debe asumir que exista una ruta POSIX directa en todos los dispositivos o canales de distribución.

La prueba específica [EXEC-015](../ejecuciones/15-diagnostico-acceso-directo-assetpack/matriz.md) confirmó en la Lenovo `storageMethod=1`, `path=null` y `assetsPath=null` para los tres packs. El resultado es un no-go para crear enlaces directos en esta instalación local; la extracción segmentada sigue siendo la regresión funcional.

## Decisión de arquitectura

Separar el acceso al juego del extractor comprimido mediante un proveedor:

```text
ApplicationDataProvider
├── ExtractedAssetProvider       (modo actual, regresión)
├── DirectAssetPackProvider      (objetivo, sin copia)
└── DiagnosticProvider           (métricas y prueba de rutas)
```

El modo actual permanecerá disponible hasta que el acceso directo supere las pruebas. El nuevo modo solo se activará cuando pueda demostrar que todas las rutas del juego son legibles por Wine.

## Fases

### Fase 0: conservar la línea base

- No modificar la variante funcional de [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md).
- Medir por separado el tamaño de los splits, el prefijo y la carpeta Cuphead.
- Usar la copia extraída como regresión si el acceso directo no es viable.

### Fase 1: diagnóstico real del almacenamiento PAD

Agregar temporalmente Play Asset Delivery y consultar cada pack instalado:

- nombre del pack;
- método de almacenamiento (`APK_ASSETS` o `STORAGE_FILES`);
- `assetsPath` cuando exista;
- existencia y tamaño de `Cuphead.exe` y de un archivo dentro de `Cuphead_Data`;
- lectura aleatoria de archivos grandes.

Esta fase no ejecutará Wine ni copiará el juego. Su resultado decidirá si el prototipo puede usar enlaces de archivos o debe detenerse.

### Fase 2: cambiar el formato interno de los packs

El stream `cuphead.tzst` no sirve como árbol directo. Para el modo sin extracción se generará una variante de asset packs con los archivos reales de Cuphead, repartidos por tamaño entre tres o más packs, conservando:

- rutas relativas;
- permisos necesarios;
- nombres exactos;
- `Cuphead.exe`, `Cuphead_Data`, DLL y recursos;
- un manifiesto con tamaño y hash por pack.

La copia comprimida seguirá existiendo solo para la variante de regresión.

### Fase 3: crear un árbol Wine de solo lectura

Si los packs proporcionan `assetsPath`, Win2APK creará en el prefijo únicamente la estructura de directorios y enlaces simbólicos hacia los archivos de los packs:

```text
.wine/drive_c/Cuphead/
├── Cuphead.exe -> <pack>/Cuphead.exe
├── UnityPlayer.dll -> <pack>/UnityPlayer.dll
└── Cuphead_Data/... -> <pack>/Cuphead_Data/...
```

No se copiarán los contenidos grandes. Como los packs son inmutables, se mantendrán los datos escribibles del juego —partidas, logs y configuración— fuera del árbol de recursos, en el perfil Wine o en un directorio de trabajo pequeño.

### Fase 4: compatibilidad con escrituras

Antes de aceptar el modo directo se observará si Cuphead escribe dentro de su directorio de instalación. Se probará:

- arranque limpio;
- creación de partida;
- cierre y reapertura;
- actualización de logs;
- lectura de recursos desde cada pack.

Si el juego necesita escribir en `C:\Cuphead`, se añadirá una capa escribible selectiva para esos archivos. No se copiará automáticamente todo el directorio; cualquier excepción deberá quedar medida.

### Fase 5: integración en Winlator

- Añadir un `DirectAssetPackProvider` independiente de `ContainerManager`.
- Resolver la ubicación en cada arranque; no conservar rutas de packs entre ejecuciones.
- Preparar el árbol de enlaces antes de crear el shortcut.
- Mantener `C:\Cuphead\Cuphead.exe` como ruta Windows estable.
- Emitir errores visibles si el pack está en `APK_ASSETS` y no existe un backend directo compatible.
- Evitar que el flujo fallback copie silenciosamente los datos, para que la métrica de almacenamiento sea verificable.

### Fase 6: validación con bundletool

Para cada compilación:

1. Generar el AAB.
2. Generar el APK set con `--local-testing`.
3. Instalar con `install-apks` en la Lenovo.
4. Consultar el método de almacenamiento PAD.
5. Confirmar que no aparece `files/rootfs/.../Cuphead` como copia regular.
6. Confirmar que `Cuphead.exe` se abre desde los enlaces o rutas directas.
7. Medir almacenamiento antes y después.
8. Repetir tras cerrar, reabrir y reinstalar.

## Criterios de aceptación

- El APK set sigue distribuyendo los archivos del juego sin payload externo.
- No se mantiene un `cuphead.tzst` extraído ni una segunda copia completa.
- La suma de archivos grandes dentro de `files/rootfs` no incluye Cuphead.
- `Cuphead.exe` arranca y Unity carga `Cuphead_Data`.
- Los datos escribibles sobreviven al reinicio.
- La variante fallback continúa funcionando si el proveedor directo no es compatible.

## Go/no-go

El primer punto de decisión es la Fase 1:

- **GO:** los packs entregan una ruta de archivos legible y se puede construir el árbol de enlaces.
- **NO-GO para acceso directo:** los packs solo aparecen como `APK_ASSETS`. En ese caso, eliminar la copia requeriría una capa virtual de archivos o una modificación profunda de Wine/Box64; no se debe presentar como un cambio pequeño ni garantizarlo para bundletool.

La alternativa de una capa virtual queda como investigación separada: necesitaría interceptar aperturas, lecturas, búsquedas de directorio y atributos desde Wine, además de resolver archivos repartidos entre varios APK. No se implementará antes de medir la Fase 1.

La Fase 1 ya se midió y está documentada en [Limitación 11](../limitaciones/11-assetpack-apk-assets-sin-ruta-directa.md). Para continuar hacia una sola copia con bundletool, la siguiente rama de investigación debe estudiar la capa virtual; no basta con cambiar el extractor Java.

## Resultado esperado

El mejor resultado práctico es conservar el juego dentro del conjunto de APKs generado desde el AAB y hacer que Winlator cree solo enlaces y metadatos. Si Android entrega los packs como APK assets sin ruta de archivos, el requisito de “sin segunda copia” no puede cumplirse con el extractor Java actual sin desarrollar una capa de sistema de archivos virtual.
