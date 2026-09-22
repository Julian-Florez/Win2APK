# Revisión contra la rúbrica

Esta revisión busca huecos. No asigna una nota estimada.

## Diseño del prototipo, maqueta, simulación o propuesta

### Evidencia visible

- Diapositiva 3: entrada, transformación y salidas definidas.
- Diapositiva 4: frontera entre componentes de terceros y trabajo propio.
- Diapositiva 5: arquitectura dividida entre build time y run time.
- Diapositiva 6: prototipo real en dispositivo.
- Diapositiva 7: demostración real y respaldo grabado.
- Backup B2: responsabilidades por capa.

### Coherencia

El diseño responde a la barrera expuesta: reemplaza decisiones manuales por una
configuración declarativa y una canalización que produce artefactos y evidencia.

### Hueco reconocido

La pregunta y la hipótesis formales no están consolidadas. No bloquean la
demostración del prototipo, pero deben definirse antes de una entrega de tesis
que las exija.

## Validación técnica o metodológica

### Evidencia visible

- Diapositiva 8: protocolo de cinco pasos, cuatro dispositivos y caso de
  payload grande.
- Diapositiva 9: iteración CoreCLR con observación, cambio y resultado.
- Diapositiva 10: contraste de resultados actuales.
- Backup B3: criterios y reglas de interpretación.
- Backup B4: muestra de dispositivos.
- Backup B5 y B7: cifra de payload y log exacto.

### Evidencia documental

- 75 ejecuciones numeradas de distinto alcance.
- 43 limitaciones numeradas.
- Runs con CSV, logs, captura T+60 y, cuando aplica, video.
- Pruebas de CLI y lint ejecutadas para esta entrega.

### Huecos reconocidos

- La cantidad de ejecuciones no reemplaza una tasa de éxito agregada.
- Falta una matriz final de criterios aprobados por aplicación y dispositivo.
- No hay muestra estadística representativa del ecosistema Android.

## Coherencia entre objetivos, resultados e impacto

### Cadena explícita

| Elemento | Evidencia en la presentación |
|---|---|
| Problema | Diapositiva 2: configuración especializada y repetibilidad. |
| Objetivo | Diapositiva 3: automatizar empaquetado y preparación. |
| Diseño | Diapositivas 4 y 5: aporte y arquitectura. |
| Validación | Diapositivas 6 a 10: demo, método, error y variación. |
| Resultado | CLI, artefactos, Core, payload y ejecución en casos concretos. |
| Impacto | Diapositiva 11: técnico observado y adopción potencial. |

### Qué puede afirmarse

- Existe una canalización experimental y reproducible.
- Se redujeron pasos manuales del flujo técnico en el prototipo.
- Se demostró empaquetado y entrega de payloads grandes en condiciones
  documentadas.
- Se localizaron limitaciones por runtime, GPU, Android y estado instalado.

### Qué no puede afirmarse

- Ahorro económico cuantificado.
- Reducción ambiental.
- Accesibilidad validada con usuarios.
- Compatibilidad universal.
- Preparación para publicación general.

## Dominio del tema

### Material preparado

- Guion con tiempos, alcance de cada afirmación y acciones de demo.
- Documento de preguntas con conceptos, arquitectura, método, límites y
  licencias.
- Backup de arquitectura, criterios, logs y fuentes.
- Respuestas preparadas para reconocer incertidumbre sin improvisar una causa.

### Conocimiento mínimo que ambos deben dominar

1. Diferencia entre Wine, Box64, DXVK y Winlator.
2. Qué automatiza Win2APK y qué sigue siendo dependencia.
3. Por qué AAB/PAD aparece en la arquitectura.
4. Qué demuestran y qué no demuestran `EXEC-049`, `EXEC-074` y `EXEC-075`.
5. Por qué target 28 es una solución experimental con deuda de publicación.
6. Por qué una captura negra o un FPS de menú requieren contexto.

## Calidad de la presentación

### Hilo conductor

La secuencia avanza de barrera a propuesta, sistema, evidencia, aprendizaje,
estado e impacto. No introduce teoría que no se use después.

### Calidad operativa

- HTML, CSS, JS, imágenes, SVG y video locales.
- Navegación por teclado, fullscreen, overview y salto a backup.
- Video de 18 segundos con póster.
- Scripts Linux y Windows.
- PDF 16:9 y capturas de QA.

### Riesgos a revisar antes de presentar

- Ensayar los dos revelados de arquitectura.
- Confirmar audio del sistema silenciado; el video no contiene audio.
- Evitar que la demo exceda 30 segundos.
- No decir “convertir a APK” sin aclarar compatibilidad y empaquetado.
- No llamar “fallo de instalación” a los runs preinstalados 074 y 075.

## Decisión de cierre

El material cubre las dimensiones de la rúbrica con evidencia identificable y
reconoce los huecos que todavía requieren trabajo. La exposición debe mantener
ese mismo alcance: sistema experimental en validación, no producto universal.
