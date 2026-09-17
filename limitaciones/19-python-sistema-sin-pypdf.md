# 19 - Python del sistema sin `pypdf`

## Descripción

Un intento de lectura detallada de un PDF invocó `python3` del sistema, cuyo entorno no incluye `pypdf`.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-29 |
| Herramienta | Python del sistema |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md) |

## Reproducción o evidencia

Mensaje exacto:

    ModuleNotFoundError: No module named 'pypdf'

El comando pretendía leer `3711875.3729163.pdf` para extraer texto por página.

## Impacto

El primer comando no extrajo información ni modificó archivos. La revisión del artículo se retrasó hasta usar el entorno correcto.

## Análisis técnico

El repositorio dispone de un runtime Python empaquetado para documentos y PDF. El fallo se produjo por usar el ejecutable del sistema en lugar del runtime suministrado por el workspace.

## Solución aplicada

Se repitió la lectura con `/home/julian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, que incluye `pypdf` 6.10.0.

## Resultado

La extracción de las 13 páginas se completó y permitió elaborar el reporte de `ARTICLE_073`.

## Limitaciones pendientes

Ninguna para la lectura PDF. Los scripts reproducibles de la revisión ya usan el runtime empaquetado o validan sus dependencias.

## Referencias

- [Reporte de ARTICLE_073](../review_output/reports/articles/ARTICLE_073.md)

## Ejecuciones asociadas

- [EXEC-023 - Revisión PRISMA multiagente](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
