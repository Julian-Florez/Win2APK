# Falta de biblioteca lcms2 para verificación alternativa con soffice

- **Proyecto:** Win2APK
- **Estado:** en investigación
- **Fecha de registro:** 2026-08-30

## Descripción

Durante la verificación opcional de la matriz de cribado y del documento de Word actualizado mediante LibreOffice, el binario `soffice` disponible en el runtime no pudo iniciar por una biblioteca compartida ausente.

## Contexto técnico

| Campo | Valor |
|---|---|
| Herramienta | `soffice` del runtime local |
| Archivos de entrada | `Estado_del_Arte_Win2APK_Preliminar.docx`; libros XLSX de `review_output/` |
| Dispositivo | N/A |
| Android/API | N/A |
| Versión de Winlator | N/A |
| Configuración | Conversión headless a XLSX para forzar recálculo alternativo |

## Reproducción o evidencia

El intento de conversión headless produjo exactamente el mensaje:

`soffice.bin: error while loading shared libraries: liblcms2.so.2: cannot open shared object file: No such file or directory`

La matriz sí fue exportada y revisada mediante el flujo de `artifact-tool`, con fórmulas, valores, tablas y hojas inspeccionadas. El documento de Word fue verificado estructuralmente con `python-docx`. El intento de renderizar el DOCX con `render_docx.py` volvió a fallar por la misma dependencia ausente. El fallo se limita a la verificación visual mediante `soffice`.

## Impacto

No impidió generar la matriz ni el documento de Word. Impide usar este binario local para comprobar de forma independiente el recálculo de fórmulas, la conversión de la hoja de cálculo y el render visual del DOCX.

## Análisis técnico

La causa observada es la ausencia de `liblcms2.so.2` en las bibliotecas disponibles para el binario de LibreOffice. No se confirmó si la biblioteca puede añadirse al runtime sin alterar otras dependencias.

## Solución aplicada

Se conservó la verificación realizada con `artifact-tool`, que inspeccionó las fórmulas, valores, tablas y hojas del libro. No se instaló ninguna biblioteca del sistema durante esta ejecución.

## Resultado

La limitación queda registrada como `en investigación`. La entrega no depende de la conversión con `soffice`.

## Limitaciones pendientes

- Instalar o habilitar una versión de LibreOffice con sus dependencias completas si se requiere una segunda herramienta de recálculo.
- Repetir la conversión y comparar los valores de las fórmulas una vez disponible `liblcms2.so.2`.

## Referencias

- [Matrices XLSX](../review_output/)
- [Documento Word preliminar](../review_output/Estado_del_Arte_Win2APK_Preliminar.docx)

## Ejecuciones asociadas

- [EXEC-021](../ejecuciones/21-recuperacion-textos-oa-20260830/matriz.md)
- [EXEC-022](../ejecuciones/22-revision-bibliografia-local-20260830/matriz.md)
- [EXEC-023](../ejecuciones/23-revision-prisma-multiagente-20260829/matriz.md)
