import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "/home/julian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "/home/julian/Tesis/Win2APK";
const inputPath = root + "/outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_recuperacion_20260830.xlsx";
const inventoryPath = root + "/ejecuciones/22-revision-bibliografia-local-20260830/evidencias/inventario_bibliografia.csv";
const candidatesPath = root + "/ejecuciones/22-revision-bibliografia-local-20260830/evidencias/candidatos_adicionales.csv";
const summaryPath = root + "/ejecuciones/22-revision-bibliografia-local-20260830/evidencias/resumen_revision.json";
const outputPath = root + "/outputs/prisma_screening_union_20260830/Matriz_cribado_PRISMA_Win2APK_union_533_bibliografia_20260830.xlsx";

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (char === '"' && next === '"') { cell += '"'; i += 1; }
      else if (char === '"') quoted = false;
      else cell += char;
    } else if (char === '"') quoted = true;
    else if (char === ",") { row.push(cell); cell = ""; }
    else if (char === "\n") { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = ""; }
    else cell += char;
  }
  if (cell.length || row.length) { row.push(cell.replace(/\r$/, "")); rows.push(row); }
  const headers = rows.shift();
  return rows.filter((item) => item.length && item.some((value) => value !== ""))
    .map((item) => Object.fromEntries(headers.map((header, index) => [header, item[index] ?? ""])));
}

function asMatrix(rows, headers) {
  return [headers, ...rows.map((row) => headers.map((header) => row[header] ?? "N/R"))];
}

function writeMatrix(sheet, startRow, startCol, matrix) {
  if (matrix.length) sheet.getRangeByIndexes(startRow, startCol, matrix.length, matrix[0].length).values = matrix;
}

function clearSheet(sheet, maxRows, maxCols) {
  for (const table of [...sheet.tables.items]) table.delete();
  sheet.getRangeByIndexes(0, 0, maxRows, maxCols).clear({ applyTo: "contents" });
}

function ensureSheet(workbook, name) {
  return workbook.worksheets.items.find((item) => item.name === name) || workbook.worksheets.add(name);
}

function styleHeader(sheet, address) {
  sheet.getRange(address).format = {
    fill: "#1F406E",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
  };
}

function addTable(sheet, address, name) {
  const table = sheet.tables.add(address, true, name);
  table.style = "TableStyleMedium2";
  table.showFilterButton = false;
  table.showBandedRows = true;
}

function setWidths(sheet, widths) {
  for (const [column, width] of widths.entries()) {
    sheet.getRangeByIndexes(0, column, 1, 1).format.columnWidth = width;
  }
}

const inventory = parseCsv(await fs.readFile(inventoryPath, "utf8"));
const candidates = parseCsv(await fs.readFile(candidatesPath, "utf8"));
const stats = JSON.parse(await fs.readFile(summaryPath, "utf8"));
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const criteria = workbook.worksheets.getItem("Criterios");
criteria.getRange("C29").values = [["Conservar las 533 filas originales sin alteración."]];

const localHeaders = [
  "BIB-ID", "n lista", "Título", "Autor principal", "Año", "Ventana 2020-2026",
  "Keyword de origen", "Nivel de relevancia", "Clasificación", "Archivo local",
  "Ruta relativa", "Contenido local", "Páginas", "DOI", "Fuente PDF declarada",
  "Estado del manifest", "EID Scopus coincidente", "Año Scopus coincidente",
  "Método de coincidencia", "Candidato similar", "Similitud de título", "SHA-256",
  "Nota del manifest", "Error de lectura",
];
const localRows = inventory.map((row) => ({
  "BIB-ID": row.BIB_ID,
  "n lista": row.n_lista,
  "Título": row.titulo,
  "Autor principal": row.autores,
  "Año": row.ano,
  "Ventana 2020-2026": row.ventana_2020_2026,
  "Keyword de origen": row.keyword,
  "Nivel de relevancia": row.nivel_relevancia,
  "Clasificación": row.clasificacion,
  "Archivo local": row.archivo_existe,
  "Ruta relativa": row.ruta_relativa,
  "Contenido local": row.contenido_local,
  "Páginas": row.paginas,
  "DOI": row.doi,
  "Fuente PDF declarada": row.fuente_pdf,
  "Estado del manifest": row.estado_manifest,
  "EID Scopus coincidente": row.eid_scopus_coincidente,
  "Año Scopus coincidente": row.ano_scopus_coincidente,
  "Método de coincidencia": row.metodo_coincidencia,
  "Candidato similar": row.candidato_similar_eid,
  "Similitud de título": row.similitud_titulo,
  "SHA-256": row.sha256,
  "Nota del manifest": row.nota_manifest,
  "Error de lectura": row.error_pdf,
}));

const candidateHeaders = [
  "BIB-ID", "Título", "Autor principal", "Año", "Ventana 2020-2026", "DOI",
  "Keyword de origen", "Nivel de relevancia", "Clasificación", "Contenido local",
  "Ruta relativa", "Páginas", "EID Scopus coincidente", "Uso sugerido",
  "Decisión preliminar", "Estado de texto completo", "Limitación / nota",
];
const candidateRows = candidates.map((row) => {
  const direct = row.nivel_relevancia === "Directa";
  const window = row.ventana_2020_2026;
  const use = direct
    ? (window === "Sí" ? "Candidato para síntesis técnica 2020-2026"
      : window === "No" ? "Fundamento técnico fuera de la ventana PRISMA"
      : "Verificar año antes de incorporarlo a la síntesis")
    : (window === "Sí" ? "Complemento contextual 2020-2026"
      : window === "No" ? "Complemento contextual fuera de la ventana PRISMA"
      : "Complemento sujeto a verificación");
  const fullText = row.contenido_local === "Texto extraíble"
    ? "Disponible localmente; lectura pendiente"
    : "Marcador sin texto suficiente; recuperación pendiente";
  const note = row.clasificacion === "Candidato adicional directo"
    ? "Relación directa con compatibilidad, traducción binaria, emulación, migración o capa de ejecución."
    : "Aporta contexto sobre gráficos, seguridad, contenedores, virtualización o reproducibilidad.";
  return {
    "BIB-ID": row.BIB_ID,
    "Título": row.titulo,
    "Autor principal": row.autores,
    "Año": row.ano,
    "Ventana 2020-2026": row.ventana_2020_2026,
    "DOI": row.doi,
    "Keyword de origen": row.keyword,
    "Nivel de relevancia": row.nivel_relevancia,
    "Clasificación": row.clasificacion,
    "Contenido local": row.contenido_local,
    "Ruta relativa": row.ruta_relativa,
    "Páginas": row.paginas,
    "EID Scopus coincidente": row.eid_scopus_coincidente,
    "Uso sugerido": use,
    "Decisión preliminar": "Candidato; lectura completa pendiente",
    "Estado de texto completo": fullText,
    "Limitación / nota": note,
  };
});

const localSheet = ensureSheet(workbook, "Bibliografía local");
clearSheet(localSheet, 120, localHeaders.length);
writeMatrix(localSheet, 0, 0, asMatrix(localRows, localHeaders));
addTable(localSheet, "A1:X" + (localRows.length + 1), "BibliografiaLocal");
localSheet.showGridLines = false;
localSheet.freezePanes.freezeRows(1);
styleHeader(localSheet, "A1:X1");
localSheet.getRange("A2:X" + (localRows.length + 1)).format.wrapText = true;
setWidths(localSheet, new Map([
  [0, 12], [1, 9], [2, 62], [3, 24], [4, 10], [5, 16], [6, 24], [7, 18],
  [8, 30], [9, 14], [10, 62], [11, 32], [12, 10], [13, 28], [14, 70], [15, 18],
  [16, 24], [17, 16], [18, 22], [19, 24], [20, 16], [21, 70], [22, 70], [23, 48],
]));

const candidateSheet = ensureSheet(workbook, "Candidatos locales");
clearSheet(candidateSheet, 120, candidateHeaders.length);
writeMatrix(candidateSheet, 0, 0, asMatrix(candidateRows, candidateHeaders));
addTable(candidateSheet, "A1:Q" + (candidateRows.length + 1), "CandidatosLocales");
candidateSheet.showGridLines = false;
candidateSheet.freezePanes.freezeRows(1);
styleHeader(candidateSheet, "A1:Q1");
candidateSheet.getRange("A2:Q" + (candidateRows.length + 1)).format.wrapText = true;
setWidths(candidateSheet, new Map([
  [0, 12], [1, 62], [2, 24], [3, 10], [4, 16], [5, 28], [6, 24], [7, 18],
  [8, 32], [9, 32], [10, 62], [11, 10], [12, 24], [13, 50], [14, 34], [15, 42], [16, 68],
]));

const reconciliation = ensureSheet(workbook, "Reconciliación fuentes");
clearSheet(reconciliation, 80, 8);
const reconRows = [
  ["Reconciliación de fuentes para el estado del arte", "", ""],
  ["Campo", "Conteo / decisión", "Interpretación y uso"],
  ["Registros Scopus en la matriz principal", 533, "Corpus PRISMA principal de la consulta conjunta; se conserva sin alterar."],
  ["Referencias en LISTA_FINAL.csv", stats.registros_lista_final, "Registros bibliográficos locales declarados."],
  ["PDFs presentes en bibliografia/articulos", stats.archivos_pdf_presentes, "Archivos que pudieron inventariarse localmente."],
  ["Referencias sin archivo local", stats.registros_sin_archivo, "Se mantienen como referencias, pero no como textos disponibles."],
  ["PDFs con texto extraíble", stats.pdfs_con_texto_extraible, "Permiten lectura local posterior; todavía no se declara evaluación a texto completo."],
  ["PDFs sin texto suficiente o marcador", stats.pdfs_sin_texto_suficiente, "No deben tratarse como evidencia leída; requieren recuperación o fuente alternativa."],
  ["Duplicados frente a Scopus", stats.duplicados_scopus, "No se agregan otra vez al corpus principal; se conserva la correspondencia en Bibliografía local."],
  ["Candidatos adicionales directos", stats.candidatos_directos, "Relación directa con compatibilidad, emulación, traducción binaria, migración o ejecución."],
  ["Candidatos adicionales complementarios", stats.candidatos_complementarios, "Contexto útil sobre virtualización, seguridad, gráficos, contenedores o reproducibilidad."],
  ["Candidatos adicionales totales", stats.candidatos_adicionales, "Se agregan a Candidatos locales como preselección, no como inclusión final."],
  ["Candidatos con año verificado 2020-2026", stats.candidatos_en_ventana_2020_2026, "Únicos candidatos locales que pueden competir en la ventana temporal, sujetos a lectura."],
  ["Candidatos fuera de 2020-2026", stats.candidatos_fuera_ventana, "Pueden sostener antecedentes técnicos, pero no cumplen la ventana exigida para la síntesis principal."],
  ["Candidatos con año N/R", stats.candidatos_ventana_no_registrada, "No se cuentan como estudios 2020-2026 hasta verificar el año en una fuente bibliográfica."],
  ["Decisión de integración", "Admitir 61 candidatos a una hoja suplementaria", "No duplicar los 8 registros coincidentes; mantener el conteo PRISMA de Scopus separado del complemento local."],
  ["Criterio de clasificación", "Metadatos, keyword y texto inicial", "Es una preselección reproducible. La decisión final exige lectura completa y validación del investigador."],
];
writeMatrix(reconciliation, 0, 0, reconRows);
reconciliation.mergeCells("A1:C1");
reconciliation.getRange("A1:C1").format = { fill: "#16324F", font: { bold: true, color: "#FFFFFF", size: 14 }, wrapText: true };
styleHeader(reconciliation, "A2:C2");
reconciliation.getRange("A3:C" + reconRows.length).format.wrapText = true;
reconciliation.getRange("A1:C" + reconRows.length).format.verticalAlignment = "top";
reconciliation.showGridLines = false;
reconciliation.freezePanes.freezeRows(2);
setWidths(reconciliation, new Map([[0, 42], [1, 24], [2, 100]]));

const summary = workbook.worksheets.getItem("Resumen PRISMA");
summary.getRange("A32:C42").clear({ applyTo: "contents" });
summary.getRange("A32:C42").values = [
  ["Complemento por fuentes locales", "", ""],
  ["Indicador", "Conteo / decisión", "Uso en la revisión"],
  ["Referencias bibliográficas locales catalogadas", stats.registros_lista_final, "LISTA_FINAL.csv; no equivale a artículos incluidos."],
  ["PDFs locales presentes", stats.archivos_pdf_presentes, "Se verificó existencia y firma PDF durante el inventario."],
  ["Duplicados de Scopus", stats.duplicados_scopus, "Se conservan como correspondencias, sin duplicar el corpus PRISMA."],
  ["Candidatos locales adicionales", stats.candidatos_adicionales, "Se trasladan a la hoja Candidatos locales con lectura pendiente."],
  ["Directos / complementarios", String(stats.candidatos_directos) + " / " + String(stats.candidatos_complementarios), "Directos: mecanismo de compatibilidad o traducción. Complementarios: soporte contextual."],
  ["Año 2020-2026 / N/R", String(stats.candidatos_en_ventana_2020_2026) + " / " + String(stats.candidatos_ventana_no_registrada), "Solo los años verificados pueden competir con la ventana requerida."],
  ["Decisión metodológica", "Separar fuentes", "Scopus conserva el flujo PRISMA principal; bibliografia aporta candidatos y antecedentes sin inflar el conteo."],
  ["Limitación", "Lectura pendiente", "La clasificación por metadatos no constituye inclusión final ni tabla comparativa definitiva."],
  ["Evidencia", "EXEC-022", "Inventario, duplicados y candidatos están en ejecuciones/22-revision-bibliografia-local-20260830/evidencias/."],
];
summary.getRange("A32:C32").merge();
summary.getRange("A32:C32").format = { fill: "#16324F", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
styleHeader(summary, "A33:C33");
summary.getRange("A34:C42").format.wrapText = true;
summary.getRange("A32:C42").format.verticalAlignment = "top";
setWidths(summary, new Map([[0, 42], [1, 24], [2, 100]]));

for (const item of [
  ["Resumen PRISMA", "A30:H42", "resumen_bibliografia.png"],
  ["Bibliografía local", "A1:X8", "bibliografia_local.png"],
  ["Candidatos locales", "A1:Q8", "candidatos_locales.png"],
  ["Reconciliación fuentes", "A1:C18", "reconciliacion_fuentes.png"],
]) {
  const sheetName = item[0];
  const range = item[1];
  const fileName = item[2];
  const preview = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile("/tmp/win2apk-sheet/" + fileName, new Uint8Array(await preview.arrayBuffer()));
}

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
console.log(JSON.stringify({
  outputPath,
  localRows: localRows.length,
  candidateRows: candidateRows.length,
  duplicateRows: stats.duplicados_scopus,
  stats,
}, null, 2));
