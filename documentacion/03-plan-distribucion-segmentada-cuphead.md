# 03. Plan de distribución segmentada para Cuphead

- **Fecha:** 2026-08-24
- **Estado:** prototipo AAB segmentado validado experimentalmente en Lenovo TB-J606F
- **Propósito:** definir cómo distribuir una publicación Windows de aproximadamente 4,45 GiB sin incluirla directamente dentro de un APK único.

## Problema

La carpeta de Cuphead funciona en Lutris/GE-Proton11-5 y se convirtió en `cuphead.tzst`, pero la compilación actual de Win2APK falla en `compressDebugAssets` con `Required array size too large`. La ejecución está documentada en [EXEC-012](../ejecuciones/12-build-cuphead-apk/matriz.md) y la restricción en la [Limitación 08](../limitaciones/08-asset-cuphead-excede-empaquetado-apk.md).

El primer prototipo AAB con un pack único `cuphead_data` sí compila, pero la generación de APKs locales mediante bundletool 1.18.3 falla al firmar el ZIP de más de 4 GiB. El resultado está documentado en [EXEC-013](../ejecuciones/13-bundletool-cuphead-aab/matriz.md) y la [Limitación 09](../limitaciones/09-bundletool-zip64-asset-pack-cuphead.md).

La variante actual divide el stream en tres packs `install-time` (`cuphead_data_01`, `_02`, `_03`). bundletool generó el APK set, la Lenovo recibió los tres splits y el extractor reconstruyó el stream original. La primera ejecución de Cuphead inicializó Unity, Direct3D 11, Turnip e input táctil; este resultado está en [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md).

## Opciones Android consideradas

### Android App Bundle y Play Asset Delivery

Android App Bundle (`.aab`) es un formato de publicación; Google Play genera los APK optimizados. Play Asset Delivery (PAD) permite colocar grandes cantidades de datos en asset packs con entrega `install-time`, `fast-follow` u `on-demand`. PAD requiere ejecutar la aplicación como App Bundle y no resuelve por sí solo la distribución de un APK independiente fuera de Google Play. Véanse la [guía de App Bundles](https://developer.android.com/guide/app-bundle) y la [guía oficial de Play Asset Delivery](https://developer.android.com/guide/playcore/asset-delivery).

Para Win2APK, el asset pack contendría `cuphead.tzst` y el núcleo esperaría a que el pack estuviera disponible antes de extraerlo al prefijo. En `on-demand` o `fast-follow`, la aplicación debe consultar el estado, mostrar progreso, manejar pausa por Wi-Fi/datos móviles y obtener la ruta con `AssetPackManager`; el archivo no debe tratarse como una ubicación permanente. La documentación oficial indica además que las descargas grandes pueden requerir confirmación explícita si no hay Wi-Fi. Véase la [integración Java](https://developer.android.com/guide/playcore/asset-delivery/integrate-java).

### Archivos de expansión OBB

Los OBB son el mecanismo legado de expansión asociado a APK en Google Play. Cada aplicación puede tener como máximo un archivo `main` y uno `patch`, y cada archivo puede medir hasta 2 GiB. La publicación de Cuphead de 4,45 GiB no cabe en dos OBB sin una reducción sustancial; además, la gestión de descarga/licencia y el almacenamiento en `Android/obb/<package>` añaden complejidad. Se conservará como referencia histórica, no como diseño principal. Véase la [documentación oficial de APK Expansion Files](https://developer.android.com/google/play/expansion-files).

### APK pequeño más payload externo

Para distribución fuera de Play, el APK puede contener solo Winlator Core y un manifiesto del payload. El archivo `cuphead.tzst` puede distribuirse como descarga posterior o como partes (`cuphead.tzst.part01`, etc.) acompañadas de tamaño, versión y SHA-256. La aplicación reconstruye o lee el payload en almacenamiento privado de la aplicación, lo valida y luego ejecuta la extracción.

Esta opción conserva el modelo de APK instalable localmente, pero deja de ser un único archivo autónomo. Requiere una pantalla visible de preparación, almacenamiento temporal suficiente y un origen de datos controlado por el distribuidor.

## Decisión propuesta

Mantener dos perfiles de distribución:

1. **Perfil Play:** `.aab` con un asset pack `cuphead_data`, inicialmente `on-demand`, y bloqueo visible del primer inicio hasta terminar la descarga y validación. PAD es la ruta nativa recomendada para publicaciones de varios GiB en Google Play; los OBB no son adecuados para el tamaño observado.
2. **Perfil fuera de Play:** APK pequeño más payload externo versionado, con descarga reanudable o transferencia local de partes. No se intentará ocultar el payload dentro del APK ni se presentará como una APK autónoma.

La prueba local de bundletool usa `--local-testing` y sirve para verificar la instalación de los splits; no equivale a una publicación en Google Play ni valida por sí sola la entrega PAD en producción.

El modo `install-time` queda como alternativa si las pruebas de almacenamiento muestran que el dispositivo puede asumir más del doble del tamaño del pack durante instalación/actualización. La documentación de PAD advierte que los asset packs `install-time` requieren espacio libre adicional equivalente, como mínimo, a dos veces su tamaño total.

## Diseño técnico común

Se añadirá un proveedor de payload independiente del origen:

```text
PayloadProvider
├── BundledAssetProvider       (prueba actual, assets del APK)
├── PlayAssetPackProvider      (AAB/PAD)
└── ExternalPayloadProvider    (descarga o partes fuera de Play)
```

El contrato de configuración incorporará, sin guardar secretos:

```json
{
  "assetMode": "play_asset_pack",
  "assetPackName": "cuphead_data",
  "assetFile": "cuphead.tzst",
  "assetSize": 4782573186,
  "assetSha256": "33aad774c30e07be8088160d35bacdd191eae7d06ed0fd507f396c726d7eff93"
}
```

El flujo de primer inicio será:

1. Mostrar el estado `Preparando datos de Cuphead`.
2. Resolver el proveedor y consultar tamaño/versión.
3. Descargar o localizar el payload con progreso visible.
4. Validar tamaño y SHA-256.
5. Extraer `cuphead.tzst` directamente desde un archivo/ruta accesible al proveedor hacia `C:\Cuphead`.
6. Crear el shortcut y continuar con el flujo Core existente.
7. Conservar un manifiesto de versión para que las aperturas posteriores no repitan la extracción.

## Fases de implementación

1. **Refactor local:** extraer una interfaz `PayloadProvider` y conservar el proveedor actual como prueba de regresión.
2. **Prueba de asset pack:** crear el módulo `cuphead_data` con `com.android.asset-pack`, conectarlo al `.aab` y probar `install-time` con `bundletool --local-testing`. La guía oficial describe la estructura Gradle y el procedimiento local de prueba en [Test asset delivery](https://developer.android.com/guide/playcore/asset-delivery/test).
3. **Proveedor PAD dinámico:** implementar `on-demand`, estado, confirmación de red, reanudación y resolución de ruta antes de iniciar Wine.
4. **Proveedor externo:** implementar manifiesto firmado por hash, descarga reanudable o ensamblaje de partes, espacio libre y recuperación ante interrupción.
5. **Decisión de publicación:** comparar tiempo de instalación, espacio temporal, consumo de red, persistencia y primer inicio en los dispositivos objetivo.

## Decisiones pendientes

- Definir si la distribución objetivo será Google Play, instalación local o ambas.
- Elegir servidor/origen para el payload externo si se mantiene el perfil fuera de Play.
- Confirmar el espacio disponible real de los dispositivos Android objetivo.
- Determinar si el primer prototipo prioriza `on-demand` PAD o payload externo local para evitar depender de una cuenta de Google Play.

## Trazabilidad

- [Configuración actual](../config/win2apk.json)
- [Instalación y primer inicio de Cuphead](../ejecuciones/11-instalacion-cuphead-lutris/matriz.md)
- [Fallo de compilación por tamaño](../ejecuciones/12-build-cuphead-apk/matriz.md)
- [Limitación del asset grande](../limitaciones/08-asset-cuphead-excede-empaquetado-apk.md)
- [Prueba AAB segmentada en Lenovo](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md)
