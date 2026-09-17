# 21 - Fuente DejaVu ausente durante la generación del diagrama PRISMA

## Descripción

La primera ejecución del generador PRISMA creó las matrices y resúmenes textuales, pero falló al producir `prisma_flow.png` porque la ruta esperada de la fuente DejaVu no existe en el entorno.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-30 |
| Herramienta | Python 3.12 incluido en el runtime del workspace, Pillow |
| Script | `review_output/scripts/build_prisma.py` |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md) |

## Reproducción o evidencia

La llamada `ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 31)` terminó con el mensaje exacto:

    OSError: cannot open resource

La búsqueda de archivos `.ttf` confirmó que el runtime incluye Bitstream Vera bajo el paquete `reportlab`, pero no la ruta DejaVu utilizada inicialmente.

## Impacto

El fallo afectó solo la salida gráfica `prisma_flow.png`. `prisma_master_matrix.csv`, `prisma_summary.md` y `prisma_flow.md` se escribieron antes del error y conservaron cifras válidas.

## Análisis técnico

La causa observada fue una ruta de fuente no portable. Pillow estaba disponible y pudo importarse; el recurso tipográfico concreto no estaba instalado en la ubicación supuesta.

## Solución aplicada

El script se actualizó para usar `Vera.ttf` y `VeraBd.ttf`, disponibles dentro del runtime de Python mediante el paquete `reportlab`.

## Resultado

La repetición finalizó sin error. Pillow abrió `prisma_flow.png` como PNG RGB de 1800 × 1500 píxeles y `Image.verify()` devolvió `PASS`. La limitación se considera resuelta experimentalmente para este runtime.

## Limitaciones pendientes

La ruta del runtime continúa siendo específica de este entorno. Una ejecución en otro equipo deberá localizar una fuente TrueType disponible o usar una fuente incorporada; la prueba no demuestra portabilidad de la ruta.

## Referencias

- [Generador PRISMA](../review_output/scripts/build_prisma.py)
- [Diagrama en Markdown](../review_output/prisma_flow.md)

## Ejecuciones asociadas

- [EXEC-023 - Revisión PRISMA multiagente](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
