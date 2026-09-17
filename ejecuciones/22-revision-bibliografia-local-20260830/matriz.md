# EXEC-022 - Revisión y conciliación de bibliografía local

## Identificación

| Campo | Valor |
|---|---|
| ID | EXEC-022 |
| Fecha | 2026-08-30 |
| Tipo | Revisión automatizada y conciliación de fuentes |
| Resultado general | Parcial: inventario y matriz ampliada generados; lectura completa pendiente |
| Aplicación | Win2APK |
| Publicación / hash | N/A |

## Método

Se comparó la bibliografía local con la exportación conjunta de 533 registros de Scopus. La fuente local se tomó de bibliografia/LISTA_FINAL.csv y de los archivos existentes en bibliografia/articulos/.

El procedimiento automatizado:

1. comprobó la existencia de cada archivo listado;
2. calculó el SHA-256 de cada PDF presente;
3. verificó si el archivo era un PDF legible y si tenía texto extraíble;
4. extrajo metadatos iniciales con pypdf;
5. comparó DOI normalizado y título normalizado contra los 533 registros Scopus;
6. clasificó los registros por relación directa o complementaria con Win2APK;
7. generó una hoja suplementaria sin alterar el corpus PRISMA principal.

La clasificación es una preselección bibliográfica. No representa inclusión final ni evaluación metodológica a texto completo.

## Condiciones de revisión

| Campo | Valor | Evidencia |
|---|---|---|
| Registros declarados en la lista local | 72 | [inventario_bibliografia.csv](evidencias/inventario_bibliografia.csv) |
| PDFs presentes | 69 | [resumen_revision.json](evidencias/resumen_revision.json) |
| Registros sin archivo local | 3 | [inventario_bibliografia.csv](evidencias/inventario_bibliografia.csv) |
| Exportación Scopus de referencia | 533 registros | estado_del_arte/export_24f23048-3942-463f-9f1d-46dcf6a7f367_2026-08-30T004723.331226035.csv |
| Herramienta de extracción | pypdf 6.10.0 | N/A |
| Ventana temporal de la síntesis principal | 2020-2026 | Criterio PRISMA del proyecto |
| Dispositivo / Android / ABI | N/A | Revisión documental |

## Matriz de criterios

| ID | Criterio | Resultado | Valor | Evidencia | Observaciones |
|---|---|---|---:|---|---|
| M-01 | Referencias de la lista local catalogadas | Verificado | 72 | [inventario_bibliografia.csv](evidencias/inventario_bibliografia.csv) | Incluye tres referencias sin archivo. |
| M-02 | PDFs presentes en la carpeta | Verificado | 69 | [resumen_revision.json](evidencias/resumen_revision.json) | Se verificó la existencia física. |
| M-03 | PDFs con texto extraíble | Verificado | 51 | [inventario_bibliografia.csv](evidencias/inventario_bibliografia.csv) | Texto disponible para lectura posterior; no equivale a lectura realizada. |
| M-04 | PDFs sin texto suficiente o marcador | Verificado | 18 | [inventario_bibliografia.csv](evidencias/inventario_bibliografia.csv) | Requieren recuperación o fuente alternativa. |
| M-05 | Coincidencias con Scopus | Verificado | 8 | [duplicados_scopus.csv](evidencias/duplicados_scopus.csv) | No se agregaron como filas nuevas. |
| M-06 | Candidatos adicionales directos | Verificado | 43 | [candidatos_adicionales.csv](evidencias/candidatos_adicionales.csv) | Compatibilidad, emulación, traducción binaria, migración o capas de ejecución. |
| M-07 | Candidatos adicionales complementarios | Verificado | 18 | [candidatos_adicionales.csv](evidencias/candidatos_adicionales.csv) | Contenedores, seguridad, gráficos, virtualización o reproducibilidad. |
| M-08 | Candidatos adicionales totales | Verificado | 61 | [candidatos_adicionales.csv](evidencias/candidatos_adicionales.csv) | Se incorporaron a una hoja suplementaria. |
| M-09 | Candidatos locales con año 2020-2026 verificado | Verificado | 10 | [resumen_revision.json](evidencias/resumen_revision.json) | Pueden competir en la ventana temporal, sujetos a lectura. |
| M-10 | Candidatos fuera de la ventana 2020-2026 | Verificado | 36 | [resumen_revision.json](evidencias/resumen_revision.json) | Útiles como antecedentes técnicos, no para la síntesis principal. |
| M-11 | Candidatos con año no registrado | Verificado | 15 | [resumen_revision.json](evidencias/resumen_revision.json) | No se cuentan como estudios 2020-2026. |
| M-12 | Actualización de la matriz de trabajo | Verificado | 1 archivo | [Matriz ampliada](../../outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_bibliografia_20260830.xlsx) | Se conservaron las hojas Scopus y se añadieron tres hojas locales. |

## Observación, interpretación y decisión

### Observación

La carpeta local contiene 69 PDFs, mientras que LISTA_FINAL.csv contiene 72 referencias. Ocho archivos corresponden a trabajos que ya estaban en los 533 registros Scopus. Los 61 restantes fueron clasificados como candidatos adicionales: 43 directos y 18 complementarios.

### Interpretación

La bibliografía local amplía la cobertura técnica con trabajos sobre Wine, capas de compatibilidad, traducción binaria dinámica y estática, emulación cruzada, ARM/x86, QEMU, LLVM y migración de software. También aporta material contextual sobre contenedores, seguridad de código nativo, gráficos y reproducibilidad. Parte del material es anterior a 2020 o tiene el año pendiente de verificación, por lo que no debe mezclarse automáticamente con la ventana temporal exigida.

### Decisión

Se mantienen los 533 registros Scopus como corpus PRISMA principal. Los 8 duplicados se documentan en la hoja Bibliografía local, sin duplicar el conteo. Los 61 candidatos no duplicados se incorporan a Candidatos locales con estado de lectura pendiente. La síntesis 2020-2026 deberá priorizar los 10 candidatos con año verificado y revisar los 15 con año N/R antes de decidir su elegibilidad.

## Fallos y limitaciones

- [Limitación 16](../../limitaciones/16-error-sintaxis-inventario-bibliografia.md): el primer intento del script terminó con un error de sintaxis y fue corregido antes de generar la salida final.
- [Limitación 15](../../limitaciones/15-falta-liblcms2-verificacion-soffice.md): el render visual del DOCX y la conversión alternativa con LibreOffice no pudieron ejecutarse porque falta liblcms2.so.2. La revisión estructural del DOCX sí se completó con python-docx.
- La clasificación se basó en metadatos, keyword y texto inicial extraíble. No se afirmó inclusión final.
- La pertenencia a Scopus o WOS de los candidatos locales no duplicados queda pendiente de verificación individual.
- La existencia de un PDF local no garantiza que corresponda a la versión editorial final ni que su licencia permita redistribución.

## Evidencias asociadas

- [Inventario completo](evidencias/inventario_bibliografia.csv)
- [Candidatos adicionales](evidencias/candidatos_adicionales.csv)
- [Duplicados frente a Scopus](evidencias/duplicados_scopus.csv)
- [Resumen de conteos](evidencias/resumen_revision.json)
- [Matriz PRISMA ampliada](../../outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_bibliografia_20260830.xlsx)
- [Script de inventario](scripts/inventariar_bibliografia.py)
- [Script de generación de matriz](scripts/crear_matriz_ampliada.mjs)

## Pendientes

- [ ] Verificar año, tipo documental e indexación de cada candidato local que se quiera usar en la síntesis 2020-2026.
- [ ] Leer a texto completo los candidatos directos priorizados.
- [ ] Extraer objetivo, metodología, variables, hallazgos, limitaciones y relación con Win2APK.
- [ ] Actualizar la tabla comparativa y el diagrama PRISMA únicamente después de las decisiones de inclusión.
