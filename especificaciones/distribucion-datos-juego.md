# Especificación de distribución de datos del juego

- **Identificador:** `WIN2APK-DATA-001`
- **Versión:** 0.1
- **Fecha:** 2026-08-24
- **Estado:** requisitos de una sola copia verificados experimentalmente para el modo on-demand con extracción y limpieza

## Propósito

Definir criterios verificables para distribuir una carpeta Windows grande dentro de un AAB y ejecutarla mediante el entorno de compatibilidad sin conservar dos copias completas después de la preparación.

## Requisitos funcionales

| ID | Requisito verificable |
|---|---|
| DATA-RF-01 | El AAB y su APK set deberán contener todos los datos necesarios; el usuario no deberá seleccionar un payload externo. |
| DATA-RF-02 | Los packs no disponibles deberán solicitarse mediante Asset Delivery y la aplicación deberá esperar un estado terminal verificable antes de preparar Wine. |
| DATA-RF-03 | La aplicación deberá validar el destino completo antes de eliminar cualquier fuente de instalación. |
| DATA-RF-04 | Un arranque posterior deberá reutilizar el destino validado sin volver a descargar ni extraer los mismos datos. |
| DATA-RF-05 | Si se usa acceso directo, la aplicación deberá resolver `assetsPath()` en cada versión o arranque y reconstruir enlaces obsoletos antes de iniciar Wine. |
| DATA-RF-06 | Un fallo de descarga, extracción, validación o enlace deberá producir un error visible y no un fallback silencioso que duplique todos los datos. |

## Requisitos no funcionales

| ID | Requisito verificable |
|---|---|
| DATA-RNF-01 | Después de una preparación exitosa y su limpieza, sólo deberá persistir una copia completa de los datos inmutables del juego dentro del almacenamiento atribuible a la aplicación. |
| DATA-RNF-02 | La evidencia deberá medir por separado código/splits, `files/assetpacks`, rootfs o árbol de enlaces y `getExternalFilesDir(null)/local_testing`. |
| DATA-RNF-03 | La limpieza sólo podrá ejecutarse sobre packs administrados mediante su API o sobre el directorio `local_testing` propio de la aplicación. |
| DATA-RNF-04 | El marcador de instalación sólo podrá escribirse después de que el destino haya sido preparado y validado. |
| DATA-RNF-05 | El espacio temporal máximo observado o, si no se registró, `N/R`, deberá documentarse por ejecución. |

## Criterios de aceptación

| ID | Criterio | Evidencia actual |
|---|---|---|
| DATA-CA-01 | AAB y APK set generados sin payload externo | [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md) |
| DATA-CA-02 | Fuentes PAD retiradas después de validar la extracción | [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md) |
| DATA-CA-03 | Segundo arranque sin descarga ni extracción | [EXEC-017](../ejecuciones/17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md) |
| DATA-CA-04 | `STORAGE_FILES`, enlaces y limpieza local demostrados | [EXEC-018](../ejecuciones/18-prototipo-direct-files-pixel/matriz.md) |
| DATA-CA-05 | Cuphead completo ejecutado desde enlaces | N/R; ejecución a escala completa pendiente |

## Alcance

Estos criterios describen empaquetado, distribución y ejecución mediante un entorno de compatibilidad. No convierten Cuphead ni otra aplicación Windows en una aplicación Android nativa y no afirman compatibilidad universal.

