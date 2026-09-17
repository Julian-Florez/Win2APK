# Integración de fuentes para el estado del arte

## Fecha y estado

| Campo | Valor |
|---|---|
| Fecha | 2026-08-30 |
| Estado | Adoptada para la revisión documental |
| Propósito | Integrar la exportación Scopus y la bibliografía local sin duplicar estudios |

## Decisión

El flujo PRISMA principal conservará como corpus de identificación los 533 registros de la exportación conjunta de Scopus. La carpeta bibliografia se incorporará como fuente suplementaria de antecedentes y candidatos, con una matriz separada que permita rastrear su origen y evitar que los duplicados alteren los conteos.

La revisión local identificó 72 referencias declaradas, 69 PDFs presentes y 3 referencias sin archivo. Ocho PDFs coinciden con registros Scopus por DOI o título normalizado. Los 61 registros restantes se clasificaron como candidatos adicionales: 43 de relación técnica directa y 18 complementarios.

## Justificación

La separación conserva la trazabilidad del protocolo PRISMA y permite aprovechar documentos técnicos que no fueron devueltos por la ecuación de búsqueda conjunta. Los candidatos directos cubren capas de compatibilidad, Wine, traducción binaria, emulación, arquitecturas ARM/x86, QEMU, LLVM y migración de software. Los complementarios aportan contexto sobre contenedores, seguridad de código nativo, gráficos, virtualización y reproducibilidad.

La ventana temporal se controla por separado. De los 61 candidatos adicionales, 10 tienen un año verificado dentro de 2020-2026, 36 están fuera de esa ventana y 15 conservan el año como N/R. Los documentos anteriores a 2020 pueden utilizarse como fundamento técnico, pero no sustituyen los artículos requeridos para la síntesis principal.

## Aplicación

La decisión quedó implementada en [la matriz PRISMA ampliada](../outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_bibliografia_20260830.xlsx), mediante las hojas:

- Bibliografía local, con las 72 referencias catalogadas y la trazabilidad de archivo, hash y coincidencia;
- Candidatos locales, con los 61 registros no duplicados y su uso sugerido;
- Reconciliación fuentes, con los conteos y criterios de integración.

Los duplicados no se agregan como filas nuevas al corpus PRISMA. La lectura completa, la comprobación de indexación y la decisión final de inclusión permanecen pendientes.

## Evidencia y relación con el proyecto

- [EXEC-022: revisión y conciliación de bibliografía local](../ejecuciones/22-revision-bibliografia-local-20260830/matriz.md)
- [Inventario de bibliografía](../ejecuciones/22-revision-bibliografia-local-20260830/evidencias/inventario_bibliografia.csv)
- [Candidatos adicionales](../ejecuciones/22-revision-bibliografia-local-20260830/evidencias/candidatos_adicionales.csv)
- [Duplicados Scopus](../ejecuciones/22-revision-bibliografia-local-20260830/evidencias/duplicados_scopus.csv)

## Decisiones pendientes

1. Confirmar la indexación individual en Scopus o WOS de los candidatos que se incluirán en la síntesis.
2. Leer los textos completos y completar la extracción comparativa.
3. Actualizar el diagrama PRISMA y la tabla de estudios incluidos con las decisiones finales, sin contar como incluidos los candidatos que permanezcan pendientes.
