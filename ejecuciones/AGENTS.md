# Guía para `ejecuciones/`

Esta carpeta conserva una matriz Markdown por cada intento de prueba. Una ejecución es una observación histórica: no se reemplaza por una ejecución posterior que tenga mejor resultado.

## Estructura obligatoria

Crear una carpeta con dos dígitos y un nombre corto:

`ejecuciones/NN-descripcion-corta/`

Dentro de ella crear:

- `matriz.md`: registro principal de la ejecución;
- `evidencias/`: capturas, videos o archivos que realmente existan;
- `logs/`: logs exportados, si existen.

Usar `plantilla-metricas.md` como base de cada nueva matriz. El archivo de plantilla no es una ejecución y no debe aparecer como resultado experimental.

## Datos que deben registrarse

- ID `EXEC-NNN`, fecha y tipo de prueba;
- aplicación, versión, ejecutable, publicación y hash si se conoce;
- método manual o automatizado;
- entorno, versión de Winlator, contenedor y configuración;
- dispositivo, modelo/variante, Android/API, ABI y resolución;
- instalación, primer inicio, aperturas posteriores y operación básica;
- aislamiento/persistencia, tamaño, tiempos, tasa de éxito y pasos manuales;
- errores, logs, evidencias, decisión y pendientes.

## Valores incompletos

- `N/R`: el dato no fue registrado.
- `N/A`: el dato no aplica al método.
- No usar `0`, `éxito` o `fallo` como sustituto de una medición faltante.

En una línea base manual dentro de Winlator, instalación del APK, tamaño del APK y pasos eliminados normalmente son `N/A` o `N/R`, según el caso. No mezclarlos con una prueba del APK generado.

## Reglas de comparación

- Mantener una fila por dispositivo y por intento.
- No calcular una tasa si no están documentados numerador, denominador y condiciones.
- No usar una captura para inferir tiempos, versiones o configuraciones que no aparecen en ella.
- Enlazar cualquier fallo nuevo con `../limitaciones/` y `../bitacora/`.
- Un resultado positivo en un dispositivo solo demuestra ese caso experimental.