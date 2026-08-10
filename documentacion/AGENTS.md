# Guía para `documentacion/`

Usar esta carpeta para registrar el contexto, las decisiones y los avances académicos de Win2APK. No usarla como sustituto de una matriz experimental ni como bitácora detallada de errores.

## Cuándo editar

- Añadir una decisión de alcance, arquitectura, metodología o planificación.
- Registrar un avance que cambie la interpretación del proyecto.
- Documentar una conclusión respaldada por una o más ejecuciones, fuentes oficiales o decisiones justificadas.

## Procedimiento

1. Leer `../AGENTS.md` y `index.md`.
2. Crear el siguiente documento numerado cuando se trate de una decisión nueva; no renumerar documentos históricos.
3. Indicar fecha, estado, propósito, decisión, justificación, evidencia y decisiones pendientes.
4. Enlazar las especificaciones, limitaciones y ejecuciones relacionadas.
5. Actualizar `index.md` con el enlace y una descripción breve.

## Reglas de redacción

- Distinguir problema, solución propuesta, supuesto y resultado observado.
- No afirmar que Win2APK funciona para todas las aplicaciones Windows.
- No convertir una prueba manual en evidencia de que el empaquetado automático ya está resuelto.
- Mantener separadas las decisiones académicas de los detalles de implementación.
- Si una decisión cambia por una prueba, conservar la decisión anterior como contexto y explicar el motivo del cambio.

## Evidencias

Las métricas y capturas deben vivir en `../ejecuciones/`. Los informes completos de fallos deben vivir en `../limitaciones/`. Esta carpeta solo debe enlazarlos y explicar su relación con el proyecto.