# 22 - Campo de versión relacionada ausente en la matriz PRISMA inicial

## Descripción

La validación independiente de la matriz PRISMA confirmó que los conteos cerraban, pero detectó que `prisma_master_matrix.csv` no incluía la columna `related_version_of`, necesaria para distinguir una extensión de revista de un duplicado real.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-30 |
| Herramienta | `build_prisma.py` y validador PRISMA Luna |
| Modelo | `gpt-5.6-luna` |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md) |

## Reproducción o evidencia

El validador reportó: `falta related_version_of en prisma_master_matrix.csv`. Las cifras 98, 6, 92, 17, 75, 27 y 48 sí pasaron sus controles.

## Impacto

La omisión impedía demostrar en la matriz PRISMA la relación entre versiones relacionadas, aunque no alteraba los conteos ni la deduplicación ya registrada en el inventario.

## Análisis técnico

El generador proyectaba los campos de deduplicación, pero no copiaba el campo de versiones relacionadas desde `master_inventory.csv`. Se trata de una pérdida de trazabilidad en la salida derivada, no de una modificación del inventario fuente.

## Solución aplicada

Se añadió `related_version_of` al conjunto de columnas generado por `build_prisma.py` y se reconstruyó `prisma_master_matrix.csv`, `prisma_summary.md` y `prisma_flow.md` sin cambiar las decisiones.

## Resultado

Resuelta experimentalmente. La reconstrucción incorporó `related_version_of` y el validador PRISMA Luna confirmó PASS integral en la repetición, sin cambios en las decisiones ni en los conteos.

## Limitaciones pendientes

El campo depende de la calidad de la relación documentada en el inventario fuente. La solución no convierte automáticamente una relación de versión en duplicado.

## Referencias

- [Generador PRISMA](../review_output/scripts/build_prisma.py)
- [Inventario fuente](../review_output/master_inventory.csv)
- [Validación PRISMA](../review_output/agents/prisma_validation.md)

## Ejecuciones asociadas

- [EXEC-023 - Revisión PRISMA multiagente](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
