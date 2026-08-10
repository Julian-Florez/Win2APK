# Guía para `especificaciones/`

Usar esta carpeta para requisitos, comportamiento esperado, criterios de aceptación y condiciones que puedan comprobarse mediante una prueba.

## Procedimiento

1. Leer `../AGENTS.md` y la especificación relacionada antes de modificarla.
2. Mantener identificadores estables como `RF-01`, `RNF-01` o un prefijo específico del componente.
3. Escribir cada requisito con una condición verificable y un resultado observable.
4. Enlazar cada criterio con la matriz de ejecución que lo comprueba cuando exista.
5. Si el alcance o el comportamiento cambian, registrar la versión, la fecha, la justificación y las consecuencias.

## Reglas técnicas

- No agregar persistencia, red, audio, video, instaladores o dependencias nuevas sin justificar su necesidad para la tesis.
- No presentar como requisito una capacidad que todavía solo sea una hipótesis técnica.
- Mantener explícitas las exclusiones de la aplicación mínima.
- Separar la especificación de `Win2APKTest.exe` de la especificación del builder y del APK.
- Usar `N/R` o una sección de decisiones pendientes cuando falte información; no completar el requisito por inferencia.

## Trazabilidad

Cada cambio relevante debe poder relacionarse con una decisión en `../documentacion/`, una limitación en `../limitaciones/` o una ejecución en `../ejecuciones/`. Los criterios deben evitar expresiones como compatibilidad universal o funcionamiento garantizado en todos los dispositivos.