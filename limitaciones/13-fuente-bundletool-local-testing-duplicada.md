# Bundletool local testing conserva una fuente adicional de los packs

- **Proyecto:** Win2APK
- **Aplicación:** Cuphead y Direct Files Probe
- **Estado:** resuelta experimentalmente
- **Fecha de registro:** 2026-08-24

## Descripción

Con `bundletool --local-testing`, los APK de packs bajo demanda se transfieren a `getExternalFilesDir(null)/local_testing`. Después de que Asset Delivery produce `STORAGE_FILES`, esa fuente externa puede coexistir con la copia interna del pack.

## Contexto técnico

El comportamiento es específico del mecanismo local que simula la entrega de Play desde el almacenamiento externo. No se debe atribuir automáticamente a una instalación descargada desde Google Play.

## Reproducción o evidencia

En el Pixel de [EXEC-018](../ejecuciones/18-prototipo-direct-files-pixel/matriz.md), después de `COMPLETED`, la aplicación registró:

```text
localTesting ... exists=true files=77 bytes=7240952
```

En el Mi A3 de [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md), la fuente de Cuphead ocupó `4.939.376` KiB antes del primer arranque.

## Impacto

Medir únicamente `files/assetpacks` o el rootfs produce una conclusión incorrecta sobre duplicación durante pruebas locales. Para Cuphead, la fuente puede ocupar varios GiB.

## Análisis técnico

Bundletool usa la carpeta externa de la propia aplicación como origen del proveedor falso de Asset Delivery. Una vez que todos los packs están `COMPLETED` y el destino ha sido validado, esa carpeta ya no fue necesaria para los reinicios observados.

## Solución aplicada

Win2APK elimina únicamente el hijo `local_testing` de `getExternalFilesDir(null)`, después de confirmar el marcador de extracción o el árbol de enlaces. No elimina el directorio externo padre ni el `assetsPath` administrado por PAD.

## Resultado

La limpieza se verificó en dos dispositivos y dos cargas:

- probe reducido en Pixel: el pack interno, los enlaces, `seek` y `mmap` siguieron funcionando tras el reinicio;
- Cuphead extraído en Mi A3: la fuente externa quedó en 7 KiB y el juego se relanzó sin re-descarga.

## Limitaciones pendientes

- El comportamiento se observó con bundletool `1.18.3`; otras versiones quedaron N/R.
- Una actualización local vuelve a transferir los artefactos y requiere repetir la validación y limpieza.
- No se debe aplicar esta limpieza a rutas distintas del directorio `local_testing` propio de la aplicación.

## Referencias

- [Pruebas locales de Play Asset Delivery](https://developer.android.com/guide/playcore/asset-delivery/test)

## Ejecuciones asociadas

- [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md)
- [EXEC-018](../ejecuciones/18-prototipo-direct-files-pixel/matriz.md)

