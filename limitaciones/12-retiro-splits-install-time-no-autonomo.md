# Retirar splits install-time no constituye un flujo autónomo

- **Proyecto:** Win2APK
- **Aplicación:** Cuphead mediante Winlator Core
- **Estado:** resuelta experimentalmente mediante PAD on-demand
- **Fecha de registro:** 2026-08-24

## Descripción

Después de extraer Cuphead, Package Manager permitió retirar individualmente los tres asset-pack splits `install-time`. La copia extraída permaneció, pero la versión instalada de Winlator intentó consultar y extraer los packs otra vez en el siguiente arranque.

## Contexto técnico

La prueba se realizó en una Lenovo TB-J606F, API 36, con el paquete `com.cuphead` generado en `EXEC-015`. El comando aceptado fue:

```text
pm uninstall --user 0 com.cuphead cuphead_data_01
```

La misma operación se aplicó a los otros dos splits. No se borraron archivos directamente de `/data/app`.

## Reproducción o evidencia

[EXEC-016](../ejecuciones/16-retiro-splits-cuphead-lenovo/matriz.md) registró `Success` para los tres retiros, reducción del código instalado de `5.056.035.328` a `268.724.736` bytes y conservación de 804 archivos de Cuphead.

El relanzamiento mostró exactamente:

```text
Unable to create the configured container or shortcut.
```

El diagnóstico asociado informó `location=null` para los tres packs retirados.

## Impacto

El comando `pm` demuestra que Android puede liberar los splits, pero es una operación asistida mediante shell/Package Manager y no un mecanismo que deba exigirse al usuario final. Sin un marcador, el arranque tampoco distingue una extracción válida de una incompleta.

## Análisis técnico

Los packs `install-time` pertenecen a la instalación administrada por Package Manager. La aplicación no dispone del mismo flujo ordinario que el shell para retirar esos splits. En cambio, PAD proporciona `removePack()` para packs `fast-follow` y `on-demand`.

## Solución aplicada

Se cambiaron los tres packs a `on-demand` y se añadió un ciclo transaccional:

1. solicitar y esperar los tres packs;
2. extraer en un directorio staging;
3. renombrar al destino y escribir el marcador sólo al éxito;
4. ejecutar `removePack()`;
5. eliminar la fuente propia `local_testing` de bundletool;
6. omitir la extracción en arranques posteriores si existe el marcador.

## Resultado

[EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md) verificó experimentalmente el ciclo en un Mi A3: `files/assetpacks` quedó en 28 KiB, la fuente externa en 7 KiB y `Cuphead.exe` se inició en el relanzamiento sin packs.

## Limitaciones pendientes

- Se mantiene un pico temporal mientras coexisten descarga, pack interno y extracción.
- La prueba autónoma corresponde a bundletool local testing en un Mi A3; no implica compatibilidad universal.
- La confirmación de red móvil y otros estados de descarga de Google Play quedaron N/R.

## Referencias

- [Integrar Play Asset Delivery](https://developer.android.com/guide/playcore/asset-delivery/integrate-java)
- [Probar Play Asset Delivery](https://developer.android.com/guide/playcore/asset-delivery/test)

## Ejecuciones asociadas

- [EXEC-016](../ejecuciones/16-retiro-splits-cuphead-lenovo/matriz.md)
- [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md)

