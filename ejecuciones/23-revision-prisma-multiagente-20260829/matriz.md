# Matriz de ejecución: revisión PRISMA multiagente

- **Versión de plantilla:** 1.0
- **ID:** `EXEC-023`
- **Fecha:** `2026-08-29`
- **Tipo:** automatizada
- **Resultado general:** cumplido con limitación de render visual del DOCX
- **Método:** inventario exhaustivo de PDF locales, deduplicación trazable, doble cribado independiente, arbitraje y síntesis PRISMA.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Win2APK | Repositorio local |
| Versión | N/R | No aplica al corpus bibliográfico |
| Ejecutable | N/A | Revisión documental |
| Publicación/hash | N/R | Se registra SHA-256 por PDF en `master_inventory.csv` |
| Método | Automatizado y revisión multiagente | Misión maestra suministrada por el usuario |
| Entorno | Codex, repositorio local | `/home/julian/Tesis/Win2APK` |
| Versión de Winlator | N/A | Revisión documental |
| Contenedor/configuración | N/A | Revisión documental |
| Dispositivo/variante | N/A | Revisión documental |
| Android/API | N/A | Revisión documental |
| ABI | N/A | Revisión documental |
| Resolución | N/A | Revisión documental |
| Fecha y hora de inicio | 2026-08-29T21:33:17-05:00 | Comando `date -Iseconds` |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Descubrimiento exhaustivo de PDF | Cumplido | 98 PDF físicos; 92 estudios únicos | Todo el repositorio, sin fuentes externas | [`review_output/master_inventory.csv`](../../review_output/master_inventory.csv) | 80 candidatos de texto completo y 18 marcadores incompletos. |
| M-02 | Legibilidad y extracción de texto | Cumplido | 75 textos completos únicos; 17 no recuperados | `pypdf`, registro por archivo | [`review_output/master_inventory.csv`](../../review_output/master_inventory.csv) | Los marcadores se separaron de los textos completos. |
| M-03 | Deduplicación | Cumplido | 6 registros duplicados | SHA-256, DOI, título y revisión manual | [`review_output/master_inventory.csv`](../../review_output/master_inventory.csv) | Cinco duplicados exactos y un marcador enlazado al texto completo; una versión relacionada se conservó. |
| M-04 | Doble cribado independiente | Cumplido | 150 valoraciones; 69/75 acuerdos; kappa 0,8519 | Dos revisores por estudio | [`review_output/inter_reviewer_agreement.csv`](../../review_output/inter_reviewer_agreement.csv) | Se detectaron seis conflictos para arbitraje. Modelo solicitado: `gpt-5.6-luna`. |
| M-05 | Arbitraje y auditoría | Cumplido | 6 conflictos arbitrados; 56 estudios auditados en cinco rondas, con estado final PASS en todos los auditados | Conflictos, estudios CORE, tabla comparativa y muestra determinista de excluidos | [`review_output/agents/arbitration.csv`](../../review_output/agents/arbitration.csv); [`review_output/agents/audit_round1.csv`](../../review_output/agents/audit_round1.csv); [`review_output/agents/audit_round2.csv`](../../review_output/agents/audit_round2.csv); [`review_output/agents/audit_round3.csv`](../../review_output/agents/audit_round3.csv); [`review_output/agents/audit_round4.csv`](../../review_output/agents/audit_round4.csv); [`review_output/agents/audit_round5.csv`](../../review_output/agents/audit_round5.csv) | Las filas históricas con discrepancias fueron reauditadas tras las correcciones y quedaron PASS en el estado integrado. |
| M-06 | Síntesis PRISMA y estado del arte | Cumplido con limitación visual | 48 incluidos; DOCX y tres libros XLSX generados; validación PRISMA PASS | Evidencia exclusiva de PDF locales | [`review_output/reports/phase_5_synthesis.md`](../../review_output/reports/phase_5_synthesis.md); [`review_output/agents/prisma_validation.md`](../../review_output/agents/prisma_validation.md); [`review_output/Estado_del_Arte_Win2APK_Preliminar.docx`](../../review_output/Estado_del_Arte_Win2APK_Preliminar.docx) | El render visual del DOCX no pudo ejecutarse porque el `soffice` del runtime carece de `liblcms2.so.2`; se completó QA estructural. |

## Fallos y decisiones

- **Limitación relacionada:** [18 - Límite de uso de subagentes Luna](../../limitaciones/18-limite-uso-subagentes-luna-prisma.md)
- **Mensaje exacto:** `You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 11:18 PM.`
- **Decisión:** conservar los productos anteriores como históricos y crear una revisión nueva en `review_output/`.
- **Recurrencia 2026-08-30:** seis subagentes de arbitraje y lectura completa finalizaron por límite de uso antes de producir sus archivos. Se conservaron los 19 informes de texto completo ya terminados y se programaron reintentos acotados.
- **Generación PRISMA 2026-08-30:** el primer intento de crear el PNG falló por una ruta de fuente inexistente; la matriz y los resúmenes textuales sí se generaron. Véase la [limitación 21](../../limitaciones/21-fuente-dejavu-ausente-diagrama-prisma.md).
- **Validación PRISMA 2026-08-30:** los conteos pasaron y la repetición del validador confirmó también `related_version_of`. Véase la [limitación 22](../../limitaciones/22-campo-related-version-prisma.md).
- **Render DOCX 2026-08-30:** `render_docx.py` no produjo PNG por la ausencia de `liblcms2.so.2` en `soffice`; se conserva la verificación estructural. Véase la [limitación 15](../../limitaciones/15-falta-liblcms2-verificacion-soffice.md).

## Evidencias

- Inventario: [`review_output/master_inventory.csv`](../../review_output/master_inventory.csv)
- Resumen: [`review_output/inventory_summary.json`](../../review_output/inventory_summary.json)
- Logs: [`logs/`](logs/)

## Repetibilidad y pendientes

- [x] Cerrar el inventario y validar discrepancias con un auditor independiente.
- [x] Completar el doble cribado y calcular acuerdo interevaluador.
- [x] Resolver conflictos y auditar exclusiones.
- [x] Generar matrices XLSX, flujo PRISMA y documento Word.
