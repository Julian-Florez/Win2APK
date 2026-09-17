# EXEC-021 - Recuperación legal de textos completos priorizados

## Identificación

| Campo | Valor |
|---|---|
| ID | EXEC-021 |
| Fecha | 2026-08-30 |
| Tipo | Recuperación y verificación de textos completos |
| Corpus | 45 estudios priorizados del lote PRISMA |
| Aplicación | Win2APK |
| Publicación | N/A |
| Hash del código | N/R |

## Método

Se ejecutó un procedimiento automatizado con `curl` para obtener únicamente copias públicas desde páginas de editor, repositorios institucionales, servidores de autores, preprints y actas de conferencias. No se utilizaron credenciales, Sci-Hub ni mecanismos para evadir controles de acceso. Las rutas, versiones y hashes SHA-256 quedaron registradas en el [manifest de recuperación](evidencias/manifest_recuperacion_45.csv).

## Entorno

| Campo | Valor |
|---|---|
| Sistema operativo | N/R |
| Herramienta de descarga | `curl`, conexión IPv4, límite de 25 s por URL |
| Concurrencia | 6 solicitudes simultáneas |
| Dispositivo | N/A |
| Android/API | N/A |
| ABI y resolución | N/A |

## Resultado de recuperación

| Resultado | Cantidad |
|---|---:|
| Estudios priorizados | 45 |
| PDFs válidos recuperados | 24 |
| Intentos directos sin recuperación | 4 |
| Sin intento directo por no identificar una copia pública | 17 |
| Estudios evaluados a texto completo | 0 |
| Estudios incluidos finalmente | 0 |

Los 24 archivos se encuentran en `estado_del_arte/textos_completos_45/pdfs/`. El paquete [textos_completos_24.zip](../../estado_del_arte/textos_completos_45/textos_completos_24.zip) contiene una copia de cada PDF recuperado.

## Verificación

- Cada archivo recuperado fue comprobado mediante la firma `%PDF` y un tamaño distinto de cero.
- Se extrajo el texto inicial de los 24 archivos con `pypdf` para verificar que el título correspondiera al registro seleccionado.
- El estudio PRISMA-0458 fue extraído de las páginas 26-33 de las actas públicas RAPIDO 2020. Se verificaron visualmente la primera y la última página renderizadas.
- No se modificó la matriz histórica. La copia [Matriz_cribado_PRISMA_Win2APK_union_533_recuperacion_20260830.xlsx](../../outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_recuperacion_20260830.xlsx) registra 24 textos como `Recuperado` y cuatro como `No recuperado`; no declara inclusiones finales.

## Observaciones y pendientes

- Las versiones provenientes de repositorios o preprints se identifican como tales en el manifest; no se presentan automáticamente como versiones editoriales finales.
- `PRISMA-0015`, `PRISMA-0018`, `PRISMA-0106` y `PRISMA-0424` quedaron como `No recuperado` por timeout o respuesta HTTP 403 en la ruta pública intentada.
- Los 17 estudios `No intentado` conservan su DOI o EID como ruta de localización para una recuperación posterior mediante biblioteca, autor o solicitud interbibliotecaria.
- La recuperación del texto completo no equivale a la inclusión metodológica. La lectura, extracción de variables y decisión final quedan pendientes.

## Evidencias asociadas

- [Manifest de recuperación](evidencias/manifest_recuperacion_45.csv)
- [Log de recuperación](logs/recuperacion.log)
- [Carpeta de PDFs](../../estado_del_arte/textos_completos_45/pdfs/)
