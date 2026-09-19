# Clasificación visual de la captura T+60

La captura canónica se toma una sola vez cuando el reloj monótono alcanza 60
segundos desde el lanzamiento. Se conserva lo que esté realmente en pantalla;
el script no navega, descarta ni reemplaza la imagen por no coincidir con el
estado esperado.

## Clases primarias

| Clase | Criterio observable |
|---|---|
| `gameplay` | El usuario o personaje parece estar participando en la acción principal. |
| `title_screen` | Pantalla inicial con título y una invitación a comenzar. |
| `loading` | Indicador o mensaje de carga/progreso sin interacción principal. |
| `menu` | Menú de selección, pausa, perfil o navegación interna. |
| `cutscene` | Secuencia narrativa o cinematográfica sin HUD de juego dominante. |
| `settings` | Opciones o ajustes de la aplicación o juego. |
| `compatibility_ui` | Interfaz del entorno de compatibilidad, contenedor o launcher interno. |
| `android_dialog` | Permiso, selector, aviso o diálogo del sistema Android. |
| `error_screen` | Mensaje visible de fallo, cierre o imposibilidad de continuar. |
| `black_screen` | Pantalla esencialmente negra sin contenido funcional visible. |
| `android_home` | Launcher, pantalla de inicio o interfaz general de Android. |
| `other` | Estado visible identificable que no pertenece a las clases anteriores. |
| `unknown` | La evidencia no permite identificar razonablemente el estado. |

`pending` es un estado técnico temporal y no una clasificación final.

## Procedimiento de IA

1. Abrir la imagen original con capacidad visual, sin reescalarla para el análisis.
2. Describir literalmente la pantalla antes de inferir su función.
3. Elegir una sola clase primaria y, si aporta información, una secundaria.
4. Transcribir solo el texto claramente legible; no completar palabras dudosas.
5. Asignar confianza `high`, `medium` o `low`; no inventar una probabilidad numérica.
6. Guardar el nombre real del modelo si está disponible; en caso contrario usar `N/R`.
7. Dejar `human_review_status=unreviewed` hasta una revisión humana.

La descripción debe diferenciar observación de interpretación. Una imagen negra,
por sí sola, no demuestra un crash: se clasifica `black_screen` y la conclusión
sobre el proceso se obtiene de `muestras.csv` y `eventos.csv`.

