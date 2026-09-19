# EXEC-030: Comparación de memoria entre Pixel y tres dispositivos Adreno

## Identificación

- ID: `EXEC-030`
- Fecha: 2026-09-18
- Tipo: medición comparativa de memoria Android por proceso
- Objetivo: determinar si el consumo del Pixel 9a durante el render de Cuphead está dentro del rango observado en Lenovo TB-J606F, Redmi Note 8 y Xiaomi Mi A3.
- Herramienta: `adb shell dumpsys meminfo <pid>` para `com.cuphead` y `Cuphead.exe`, más `/proc/meminfo` para memoria global.

## Condiciones

| Dispositivo | GPU / perfil | Publicación | Estado al medir |
|---|---|---|---|
| Pixel 9a | Mali-G715, Vortek + Gladio, DXVK 1.7.2, BCn Fcharan auto | v42 | relanzado y medido a los 30 s |
| Lenovo TB-J606F | Adreno 610, Turnip + Gladio, DXVK | v41 | sesión de Cuphead ya viva |
| Redmi Note 8 | Adreno 610, Turnip + Gladio, DXVK | v41 | sesión de Cuphead ya viva |
| Xiaomi Mi A3 | Adreno 610, Turnip + Gladio, DXVK | v41 | sesión de Cuphead ya viva |

El código del perfil Adreno no cambió entre v41 y v42. No obstante, los tiempos desde el arranque no son equivalentes y la versión instalada difiere; la tabla es diagnóstica y no un benchmark controlado de rendimiento.

## Resultados

Valores en KiB. El total combinado es la suma de los cortes PSS/RSS de `com.cuphead` y `Cuphead.exe`; puede incluir páginas compartidas contadas en cada proceso, por lo que se usa sólo para comparación bajo el mismo método.

| Dispositivo | PSS app | PSS juego | PSS combinado | RSS combinado | Gráficos combinados | RAM disponible del sistema |
|---|---:|---:|---:|---:|---:|---:|
| Pixel 9a | `2317273` | `374018` | `2691291` | `2814404` | `2228492` | `536388` |
| Lenovo TB-J606F | `118751` | `1720308` | `1839059` | `1900812` | `1019412` | `1185504` |
| Redmi Note 8 | `121222` | `1721672` | `1842894` | `1215764` | `1029604` | `296692` |
| Xiaomi Mi A3 | `91556` | `1720647` | `1812203` | `1199904` | `1000516` | `295028` |

## Comparación

- El PSS combinado del Pixel fue entre `46,0 %` y `48,5 %` mayor que el de los tres Adreno.
- La memoria gráfica del Pixel fue entre `2,16` y `2,23` veces la observada en los Adreno.
- En los Adreno, la mayor parte del consumo aparece en `Cuphead.exe`; en el Pixel, Vortek concentra `2228492 KiB` gráficos en el proceso Android.
- El Pixel tenía `536388 KiB` disponibles en el corte. En una corrida anterior de la misma v42, el proceso Android llegó a PSS `2816620 KiB` a los 40 s y terminó con `reason=3 (LOW_MEMORY)` aproximadamente a los 82 s.

## Interpretación

El consumo del Pixel no está en el rango de los otros dispositivos. La diferencia principal no es el árbol de datos del juego, que es el mismo payload directo, sino la memoria gráfica de la ruta Vortek/BCn/DXVK para Mali. La medición no permite separar cuánto corresponde a DXVK, Vortek o la representación de texturas BCn; sí justifica enfocar las siguientes variantes en esa ruta y no en el empaquetado.

## Decisión

- Descartar DXVK 1.7.2 como perfil estable del Pixel, aunque recupere imagen.
- Mantener sin cambios el perfil Adreno, cuyo consumo es consistente entre los tres dispositivos bajo este corte.
- Probar una variante Mali que conserve el comportamiento de memoria de DXVK 2.x sin reproducir la pantalla negra.

## Evidencia

- [Captura Pixel v42 a los 30 s](./evidencias/pixel-v42-30s.png)
- [Valores crudos](./logs/medicion.md)
- Relación: [EXEC-029](../29-pantalla-negra-dxvk241-pixel/matriz.md)

