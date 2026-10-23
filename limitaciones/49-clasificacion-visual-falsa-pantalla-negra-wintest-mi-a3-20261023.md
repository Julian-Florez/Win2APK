# 49. Revisión de falsos positivos `black_screen` en capturas WinTest del Mi A3

## Observación

La revisión inicial de algunas capturas T+60 de WinTest a resolución completa no
detectó una ventana pequeña centrada. Tres fases se clasificaron inicialmente
como `black_screen`: RUN-017 second-open, RUN-018 second-open y RUN-019 cold.
La etiqueta se corrigió a `other` después de inspeccionar la región de la
interfaz.

## Evidencia y método de revisión

- Las seis capturas de RUN-017, RUN-018 y RUN-019 tienen 1560×720 píxeles.
- El recorte central de 480×240 píxeles en `(550,240)` de las seis capturas tiene
  la misma firma de píxeles de ImageMagick:
  `2a0280c4a24e69a56a3ee31bc2eea5b197983098be3974573a96e7245edeebab`.
- OCR del recorte recupera “Hola mund[o]” y “Cambiar tex[t]o”; la inspección
  ampliada muestra la ventana Win2APK Test con “Hola mundo” y su botón.
- Etiquetas revisadas: RUN-017 second-open `black_screen` → `other`; RUN-018
  second-open `black_screen` → `other`; RUN-019 cold `black_screen` → `other`.
  Las demás tres capturas de esos pares ya estaban clasificadas `other`.
- Los seis datasets (tres fases frías y tres second-open) pasaron
  `validate_dataset.py` tras la revisión. No se alteraron las muestras de CPU,
  memoria, FPS, instalación, procesos, ni los PNG originales.

## Interpretación

El fondo alrededor de la ventana es negro, pero la aplicación sí está visible.
`black_screen` no describe correctamente una pantalla que contiene la interfaz
del juego o aplicación, aunque el área visible sea pequeña. La captura a tamaño
completo por sí sola no bastó para distinguir ambas cosas en este caso.

## Solución y estado

Se corrigieron las tres clasificaciones, se regeneraron los resúmenes y matrices
y se actualizó la guía para revisar el área de la aplicación ampliada, con OCR
como comprobación auxiliar. Corrección experimental; el clasificador sigue
siendo asistido por IA y debe apoyarse en la captura original.

## Referencias

- [RUN-017 captura fría](../metricas/runs/RUN-20261023-017/screenshots/mi-a3/t060.png) / [second-open](../metricas/runs/RUN-20261023-017/second-open/screenshots/mi-a3/t060.png)
- [RUN-018 captura fría](../metricas/runs/RUN-20261023-018/screenshots/mi-a3/t060.png) / [second-open](../metricas/runs/RUN-20261023-018/second-open/screenshots/mi-a3/t060.png)
- [RUN-019 captura fría](../metricas/runs/RUN-20261023-019/screenshots/mi-a3/t060.png) / [second-open](../metricas/runs/RUN-20261023-019/second-open/screenshots/mi-a3/t060.png)
- [Matriz EXEC-096](../ejecuciones/96-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md)
- [Matriz EXEC-097](../ejecuciones/97-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md)
- [Matriz EXEC-098](../ejecuciones/98-metricas-wintest-cold-second-open-trial-03-20261023/matriz.md)
