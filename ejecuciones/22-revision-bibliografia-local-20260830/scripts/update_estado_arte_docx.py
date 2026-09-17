from pathlib import Path

from docx import Document


ROOT = Path("/home/julian/Tesis/Win2APK")
SOURCE = ROOT / "Estado_del_arte_Win2APK_actualizado.docx"
OUTPUT = ROOT / "Estado_del_arte_Win2APK_integrado.docx"


def set_text(paragraph, text):
    paragraph.text = text


doc = Document(SOURCE)

# Update the source description without changing the surrounding document structure.
set_text(
    doc.paragraphs[2],
    "Corte de los archivos analizados: 30 de agosto de 2026",
)
set_text(
    doc.paragraphs[5],
    "La búsqueda principal se ejecutó en Scopus y se complementó con una revisión de la carpeta bibliografia. Para el flujo PRISMA se conservaron los 533 registros de la exportación conjunta de Scopus; la bibliografía local se trató como fuente suplementaria para recuperar antecedentes, detectar duplicados y proponer candidatos adicionales. Se consideraron publicaciones en inglés y español dentro del periodo 2020-2026 para la síntesis principal.",
)
set_text(
    doc.paragraphs[17],
    "Los archivos de consulta individual contienen 28 registros en S1, 20 en S2, 105 en S3 y 394 en S4. La consulta conjunta utilizada para la matriz principal devuelve 533 registros Scopus y se conserva como el corpus PRISMA de trabajo. Esta decisión evita sumar resultados de consultas solapadas y permite rastrear la procedencia de cada registro.",
)
set_text(
    doc.paragraphs[18],
    "En el corpus conjunto no se confirmaron duplicados por DOI; los 27 registros sin DOI se controlan mediante EID y título. La matriz conserva además cuatro coincidencias de título normalizado para validación manual. La revisión de la bibliografía local se reporta por separado para no mezclar sus duplicados con el conteo PRISMA.",
)
set_text(
    doc.paragraphs[26],
    "El cribado preliminar de la matriz vigente registra 458 exclusiones por título y resumen, 50 registros incluidos provisionalmente y 25 registros en duda. Estos valores son trazables en la hoja Cribado, pero requieren validación del investigador antes de convertirse en decisiones finales. La figura definitiva deberá indicar los documentos excluidos en cada fase y sus motivos, conforme al diagrama PRISMA 2020.",
)

# Insert the local-source integration subsection before the critical comparison.
anchor = doc.paragraphs[27]
heading = anchor.insert_paragraph_before("3.1. Integración de la bibliografía local")
heading.style = "Heading 2"
paragraph = anchor.insert_paragraph_before(
    "La fuente suplementaria contiene 72 referencias declaradas en LISTA_FINAL.csv y 69 PDFs presentes en bibliografia/articulos; tres referencias no tienen archivo local. La comprobación por DOI o título normalizado identificó ocho duplicados de registros Scopus, que se mantienen como correspondencias y no se agregan nuevamente al corpus principal. Los 61 registros no duplicados se incorporaron a la hoja Candidatos locales de la matriz ampliada: 43 presentan relación técnica directa con compatibilidad, emulación, traducción binaria, arquitecturas ARM/x86, QEMU, LLVM, Wine o migración de software, y 18 aportan contexto sobre contenedores, seguridad de código nativo, gráficos, virtualización y reproducibilidad."
)
paragraph.style = "Normal"
paragraph = anchor.insert_paragraph_before(
    "La disponibilidad de un archivo tampoco se interpretó como inclusión automática. En el inventario, 51 PDFs tienen texto extraíble y 18 son marcadores o no contienen texto suficiente; entre los candidatos no duplicados, 47 tienen texto extraíble y 14 requieren recuperación o una fuente alternativa. Diez candidatos tienen año verificado dentro de 2020-2026, 36 están fuera de la ventana temporal y 15 conservan el año como N/R. Por eso, los trabajos anteriores pueden apoyar los fundamentos técnicos, pero no sustituyen los artículos requeridos para la síntesis principal. La lectura completa, la verificación de indexación en Scopus o WOS y la decisión final permanecen pendientes."
)
paragraph.style = "Normal"

# Add the joint-query row to the existing query table.
query_table = doc.tables[0]
new_row = query_table.add_row()
values = [
    "SJ",
    "Consulta conjunta para el corpus principal",
    "533",
    "Exportación conjunta; consulta literal y archivo conservados en la matriz.",
]
for cell, value in zip(new_row.cells, values):
    cell.text = value

# Refresh the compact PRISMA count tables.
set_text(doc.tables[1].cell(0, 0).paragraphs[0], "Registros identificados en Scopus: 533")
set_text(doc.tables[2].cell(0, 0).paragraphs[0], "Duplicados confirmados por DOI en el corpus conjunto: 0")
set_text(doc.tables[3].cell(0, 0).paragraphs[0], "Registros Scopus conservados para cribado: 533")
set_text(doc.tables[4].cell(0, 0).paragraphs[0], "Cribado preliminar por título y resumen: 458 excluidos; 50 incluidos; 25 en duda")
set_text(doc.tables[5].cell(0, 0).paragraphs[0], "Textos completos evaluados: 0; lectura pendiente")
set_text(doc.tables[6].cell(0, 0).paragraphs[0], "Estudios incluidos finalmente: 0; decisión pendiente")

# Add traceable local evidence to the references block.
extra = doc.add_paragraph(
    "Matriz ampliada de fuentes: outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_bibliografia_20260830.xlsx. Inventario local y criterios: ejecuciones/22-revision-bibliografia-local-20260830/."
)
extra.style = "Normal"

doc.save(OUTPUT)
print(OUTPUT)
