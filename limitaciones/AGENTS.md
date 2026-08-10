# Guía para `limitaciones/`

Esta carpeta contiene el informe detallado de cada error, fallo, bloqueo o restricción técnica. El formato de referencia es `01-error-coreclr-gc-winlator.md`.

## Cuándo crear un informe

Crear un archivo cuando una prueba no cumpla lo esperado, cuando exista un mensaje de error, cuando una configuración limite el alcance o cuando una corrección experimental cambie el resultado.

## Procedimiento

1. Leer `../AGENTS.md`, el último informe numerado y `../bitacora/AGENTS.md`.
2. Obtener el número siguiente sin reutilizar nombres.
3. Usar el formato `NN-descripcion-corta.md`.
4. Registrar el mensaje exacto, los pasos, el entorno, el dispositivo, Android/API, ABI, versiones, publicación y configuración disponible.
5. Distinguir la publicación o configuración que falló de la que funcionó después.
6. Actualizar `../bitacora/index.md` con un enlace y el estado.
7. Enlazar las ejecuciones y evidencias asociadas.

## Secciones mínimas

Conservar, como mínimo, estas secciones: `Descripción`, `Contexto técnico`, `Reproducción o evidencia`, `Impacto`, `Análisis técnico`, `Solución aplicada`, `Resultado`, `Limitaciones pendientes`, `Referencias` y `Ejecuciones asociadas`.

## Reglas de evidencia

- La observación debe preceder a la explicación causal.
- Una hipótesis debe identificarse como hipótesis hasta que exista una prueba que la confirme.
- Si la versión de Winlator, el contenedor, el tiempo o el log no fueron registrados, escribir `N/R`.
- No borrar un fallo histórico porque una versión posterior funcione en un único entorno.
- No afirmar que una solución funciona en todos los dispositivos o versiones.
- Mantener las referencias oficiales y los enlaces a los archivos del repositorio.