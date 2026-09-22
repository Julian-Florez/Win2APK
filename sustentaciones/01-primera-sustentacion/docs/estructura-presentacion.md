# Estructura de la presentación

## Narrativa

La presentación sigue una investigación aplicada, no una lista de capítulos:

> Existe una barrera de integración → se define una propuesta → se delimita el
> aporte frente a Winlator → se explica el sistema → se muestra el prototipo →
> se demuestra → se expone cómo se valida → un error revela aprendizaje → la
> variación reciente fija el estado actual → se delimita el impacto → se
> responde qué se ha demostrado.

## Diseño del tiempo

| # | Diapositiva | Mensaje principal | Tiempo acumulado |
|---:|---|---|---:|
| 1 | Portada | La investigación busca una ruta reproducible entre plataformas. | 0:20 |
| 2 | La barrera | Ejecutar manualmente no resuelve distribución ni repetibilidad. | 1:00 |
| 3 | La propuesta | La CLI convierte decisiones técnicas en artefactos verificables. | 1:40 |
| 4 | Win2APK y Winlator | El aporte está en integrar y automatizar, no en reemplazar las dependencias. | 2:20 |
| 5 | Arquitectura | El sistema se divide entre build time y run time. | 3:15 |
| 6 | Prototipo actual | Existe un paquete que llega a la aplicación objetivo y muestra controles. | 3:55 |
| 7 | Demo | Se observa la ruta real o el video local de respaldo. | 4:40 |
| 8 | Validación | Cada afirmación tiene ejecución, condiciones y evidencia. | 5:20 |
| 9 | Error y aprendizaje | El fallo CoreCLR cambió el diseño de empaquetado .NET. | 5:55 |
| 10 | Estado actual | Redmi funciona en el estado observado; Lenovo reproduce un límite. | 6:20 |
| 11 | Coherencia e impacto | El impacto técnico es observado; la adopción sigue siendo potencial. | 6:35 |
| 12 | Qué demostramos | Existe un sistema experimental y una agenda de validación real. | 6:40 |

El cierre oficial ocurre en la diapositiva 12. La sección Backup / Preguntas no
forma parte del tiempo principal.

## Criterio de selección

Se conservaron en el cuerpo principal únicamente afirmaciones necesarias para
responder cuatro preguntas:

1. ¿Cuál es la barrera?
2. ¿Qué hace Win2APK que no hace el uso manual de Winlator?
3. ¿Qué evidencia demuestra que el prototipo existe y fue investigado?
4. ¿Qué se puede afirmar hoy sin exceder los datos?

Las tablas completas, conceptos, licencias, logs, restricciones de publicación
y detalles por dispositivo pasaron a respaldo.

## Mapa de evidencia

| Afirmación | Evidencia principal |
|---|---|
| La línea base exigía operación manual | `EXEC-001` |
| La CLI genera artefactos y reportes | Código `cli/`, especificación CLI y `EXEC-047` |
| El payload grande se segmenta y entrega | `EXEC-047` y `EXEC-049` |
| El prototipo abre Bomb Rush con gamepad | `EXEC-075`, captura T+60 y video |
| El flujo varía por dispositivo y estado | `EXEC-074` frente a `EXEC-075` |
| El error CoreCLR produjo un cambio verificable | Limitación 01 y `EXEC-001` |
| La validación no es universal | Matrices de ejecución y limitaciones numeradas |

## Backup

- B1: separador.
- B2: arquitectura ampliada y frontera del trabajo propio.
- B3: criterios y reglas de interpretación.
- B4: muestra de cuatro dispositivos.
- B5: payload grande y cambio de estrategia.
- B6: limitaciones vigentes.
- B7: log exacto del fallo más reciente.
- B8: conceptos y licencias.
- B9: fuentes principales.
