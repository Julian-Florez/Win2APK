# Guía de trabajo para Codex en Win2APK

Este archivo define cómo debe trabajar Codex dentro del repositorio. Antes de editar una carpeta, leer este archivo y el `AGENTS.md` más cercano a la ruta que se va a modificar.

## Selección de flujo

| Situación | Guías que se deben leer | Acción obligatoria | Skill relacionada |
|---|---|---|---|
| Aparece un error, fallo o limitación | `limitaciones/AGENTS.md`, `bitacora/AGENTS.md` | Crear o actualizar el informe numerado y el índice | `$win2apk-registrar-fallos` |
| Se realiza una prueba o intento | `ejecuciones/AGENTS.md` | Crear una carpeta numerada con `matriz.md` y evidencias | `$win2apk-metricas-ejecucion` |
| Se toma una decisión del proyecto | `documentacion/AGENTS.md` | Añadir o actualizar un documento numerado | Ninguna específica |
| Se define un requisito o criterio | `especificaciones/AGENTS.md` | Actualizar la especificación con IDs y trazabilidad | Ninguna específica |

Si una misma actividad contiene una prueba y un error, aplicar las dos skills: primero registrar la ejecución y después el fallo, enlazando ambos documentos.

## Reglas generales

- Trabajar preferentemente con Markdown y conservar la navegación mediante enlaces relativos.
- No inventar versiones, tiempos, hashes, configuraciones, pasos o resultados. Usar `N/R` para no registrado y `N/A` para no aplica.
- Separar en cada registro la observación, la interpretación, la decisión y la evidencia.
- No convertir un resultado de un dispositivo o una versión en una afirmación de compatibilidad universal.
- No modificar una matriz histórica para corregir retrospectivamente una medición; crear una nueva ejecución o una revisión explícita.
- Mantener la terminología académica: empaquetado, distribución y ejecución mediante entorno de compatibilidad. No describir el resultado como una aplicación Android nativa.
- Conservar los mensajes de error exactamente cuando existan y enlazar la fuente original.
- No guardar claves, contraseñas, tokens, keystores privados ni datos personales en el repositorio.

## Estructura de carpetas

- `documentacion/`: contexto, decisiones y avances del proyecto.
- `especificaciones/`: requisitos, criterios de aceptación y contratos verificables.
- `limitaciones/`: informes detallados de errores y restricciones técnicas.
- `bitacora/`: índice cronológico de las limitaciones.
- `ejecuciones/`: matrices versionadas y evidencias de cada intento.

## Verificación antes de entregar

Comprobar que los nombres sigan la numeración, que los enlaces relativos funcionen, que cada métrica tenga condiciones de prueba y que el resultado no exceda la evidencia disponible.