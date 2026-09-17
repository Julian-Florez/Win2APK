# 18 - Límite de uso de subagentes Luna durante el cribado PRISMA

## Descripción

Los seis revisores independientes asignados al doble cribado terminaron antes de escribir sus matrices porque el servicio rechazó nuevas inferencias al alcanzar el límite temporal de uso.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-29 |
| Herramienta | Subagentes multiagente |
| Modelo | `gpt-5.6-luna` |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md) |

## Reproducción o evidencia

Se lanzaron seis revisores independientes, cada uno con 25 asignaciones. Todos devolvieron el mismo mensaje antes de crear `screening_R1.csv` a `screening_R6.csv`:

    You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 11:18 PM.

La ausencia de los seis archivos se verificó en `review_output/agents/`.

El 2026-08-30, un segundo bloque de seis subagentes que cubría arbitraje y diez lecturas completas volvió a terminar con el mensaje:

    You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 4:25 AM.

En ese segundo evento no se produjo `arbitration.csv` ni los diez informes asignados.

## Impacto

El doble cribado quedó sin resultados utilizables. El inventario, la deduplicación, las asignaciones y el protocolo no se perdieron. No es válido calcular acuerdo, arbitraje ni cifras PRISMA finales hasta recibir las 150 valoraciones.

## Análisis técnico

La causa observada es un límite temporal del servicio de subagentes, no un error de los PDF ni de las asignaciones. No se infiere una causa adicional.

## Solución aplicada

Después de la hora indicada por el servicio se cerraron las seis instancias fallidas y se relanzaron los mismos lotes con `gpt-5.6-luna`. Las asignaciones se conservaron sin cambios para mantener la reproducibilidad.

## Resultado

El primer reintento produjo los seis archivos `screening_R1.csv` a `screening_R6.csv`. La validación confirmó 25 filas por revisor, 150 valoraciones en total, dos revisiones por cada uno de los 75 estudios con texto completo y puntuaciones dentro del intervalo 0 a 5. El acuerdo exacto fue de 69 de 75 decisiones y el kappa de Cohen global fue 0,8519. Sin embargo, la recurrencia del 2026-08-30 impidió cerrar el arbitraje y el siguiente lote de lectura completa. La limitación queda reproducida; los productos completos previos se conservan y los trabajos fallidos se relanzan de forma acotada.

## Limitaciones pendientes

La disponibilidad de subagentes continúa sujeta a cuotas temporales externas. El cribado ya completado no se invalida, pero arbitraje, auditoría y lecturas adicionales deben verificarse por archivo antes de considerarse terminados.

## Referencias

- [Protocolo de cribado](../review_output/screening_protocol.md)
- [Asignaciones](../review_output/screening_assignments.csv)

## Ejecuciones asociadas

- [EXEC-023 - Revisión PRISMA multiagente](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
