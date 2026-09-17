# 20 - Salidas no conformes de subagentes durante la revisión PRISMA

## Descripción

Dos productos generados por subagentes no cumplieron inicialmente el contrato de salida: un par de informes se escribió en una ruta distinta de la prevista y el CSV del revisor R6 quedó con comillas sin cerrar en el último campo.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-29 |
| Herramienta | Subagentes multiagente y validación local de CSV |
| Modelo | `gpt-5.6-luna` |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md) |

## Reproducción o evidencia

La verificación de rutas detectó informes bajo `review_output/articles/` cuando el contrato exigía `review_output/reports/articles/`. La lectura estructurada de `screening_R6.csv` detectó campos desplazados por comillas sin cerrar en la última columna. El problema se observó antes de consolidar las 150 valoraciones.

En una fase posterior, `ARTICLE_008.md` usó `ADVANCE` en las secciones 2 y 22, aunque la plantilla solo admite las cinco clasificaciones finales. El resto del informe y sus puntuaciones estaban completos.

La validación global de los 48 informes detectó además `SECONDARY` en `ARTICLE_063.md`, otra etiqueta fuera del conjunto permitido.

## Impacto

Sin corrección, los informes no habrían sido descubiertos por la fase de síntesis y las filas de R6 no habrían podido validarse ni compararse con sus asignaciones.

## Análisis técnico

La causa comprobada fue el incumplimiento del formato y la ruta solicitados. No se atribuye el problema al contenido de los PDF. No se dispone de evidencia para identificar una causa interna adicional del modelo.

## Solución aplicada

Los informes se trasladaron a la ruta canónica sin sobrescribir archivos existentes. El CSV de R6 se reparó de forma mecánica con `review_output/scripts/repair_screening_r6.py`; además, los DOI de `ARTICLE_073` y `ARTICLE_088` se contrastaron directamente con sus PDF antes de consolidar.

La etiqueta `ADVANCE` de `ARTICLE_008.md` se normalizó a `RELEVANT`, coherente con la puntuación propuesta por el propio lector y con el conjunto permitido por el protocolo. La decisión queda sujeta a la consolidación del agente clasificador.

La etiqueta `SECONDARY` de `ARTICLE_063.md` también se normalizó a `RELEVANT`; el uso narrativo secundario se conservó en la justificación, no como categoría PRISMA.

## Resultado

Los informes quedaron en `review_output/reports/articles/`. El CSV reparado superó la validación de 25 filas, columnas obligatorias, asignaciones, puntuaciones y códigos de exclusión. La consolidación produjo 150 revisiones válidas, por lo que la limitación se considera resuelta experimentalmente en esta ejecución.

## Limitaciones pendientes

La reparación preserva el contenido entregado por el revisor y corrige la estructura. No sustituye la auditoría posterior de exactitud factual contra los PDF.

## Referencias

- [Script de reparación](../review_output/scripts/repair_screening_r6.py)
- [Matriz maestra provisional](../review_output/master_evidence_matrix.csv)
- [Acuerdo interevaluador](../review_output/inter_reviewer_agreement.csv)

## Ejecuciones asociadas

- [EXEC-023 - Revisión PRISMA multiagente](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
