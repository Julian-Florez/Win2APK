# Comparación de perfiles gráficos para Pixel Tensor/Mali

- **Versión de plantilla:** 1.0
- **ID:** `EXEC-020`
- **Fecha:** `2026-08-25`
- **Tipo:** comparación manual y diagnóstico automatizado
- **Resultado general:** parcial
- **Método:** comparación aislada de wrapper Direct3D, transcodificación de texturas BCn y ajustes visuales en un Pixel 9a. Después de cada variante se observaron inicio, imagen, memoria y motivo de salida. Al terminar se restauró el perfil ETC2 que había permitido jugar con audio y control.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead empaquetado con entorno de compatibilidad (`com.cuphead`) | Paquete ya instalado mediante el flujo AAB local del proyecto |
| Versión | N/R | La versión del juego no se consultó durante esta ejecución |
| Ejecutable | `C:\\Cuphead\\Cuphead.exe` | [salida de Wine](./logs/cuphead-salida-etc2.txt) |
| Publicación/hash | App `versionName=11.1-direct-files`, `versionCode=29`; hash del APK/AAB N/R | `dumpsys package com.cuphead` |
| Método | Inicio visible y monitorización por ADB; validación de juego con control físico por el usuario | No se usaron ventanas silenciosas |
| Entorno | Wine/Box64 dentro del fork de Winlator; Box64 `0.4.0` | [preferencias](./logs/preferencias-dispositivo.xml) |
| Versión de Winlator | Fork con `versionName=11.1-direct-files`; versión upstream exacta N/R | Paquete instalado |
| Contenedor/configuración final | Vortek 2.1 + Gladio 1.0; DXVK-Sarek 1.13.0; `maxDeviceMemory=1024`; ALSA; Box64 `INTERMEDIATE` | [contenedor final](./logs/contenedor-final.json) |
| Dispositivo/variante | Google Pixel 9a (`tegu`), GPU Mali-G715 | Propiedades del dispositivo y [preferencias](./logs/preferencias-dispositivo.xml) |
| Android/API | Android 17 beta / API 37; compilación `CP41.260731.005.B1` | `getprop ro.build.version.*` |
| ABI | `arm64-v8a` | `getprop ro.product.cpu.abilist` |
| Resolución | Juego 1280x720; pantalla física 1080x2424 a 420 dpi | Contenedor y `wm size`/`wm density` |
| Fecha y hora de inicio | 2026-08-25; hora inicial del conjunto N/R | Las muestras individuales conservan hora ISO local |

## Variantes observadas

| Variante | Observación | Memoria/salida | Decisión |
|---|---|---|---|
| Turnip en Pixel | No produjo una ruta gráfica utilizable en la GPU Mali | Mensaje exacto N/R | Descartada para este perfil; Turnip se conserva para Adreno |
| Vortek + DXVK 2.4.1 | Direct3D 11 no inició correctamente | Mensaje exacto N/R | Sustituida por DXVK-Sarek |
| Vortek + DXVK-Sarek 1.13.0 + capa BCn ETC2 | Inicio, audio, control y juego aceptables según la prueba del usuario; se observó un borde borroso/pixelado en ciertas transparencias | Durante juego: `ION_heap=2649560 kB`, GPU entre `620060` y `637180 kB`; proceso vivo durante las cinco muestras | **Perfil restaurado y seleccionado provisionalmente** |
| ETC2 a 1080p y efecto cromático desactivado | El defecto visual permaneció | Sin mejora visual confirmada | Descartada; se restauró 1280x720 y la configuración previa |
| Transcodificación ASTC | El defecto visual permaneció | Salida posterior `reason=9 (EXCESSIVE RESOURCE USAGE)`, `subreason=7 (EXCESSIVE CPU USAGE)` | Descartada |
| Capa Fcharan, ASTC alta calidad y omisión de texturas pequeñas | Aparecieron texturas ausentes, stuttering, menor velocidad y crash | `reason=3 (LOW_MEMORY)`, `rss=3,1GB` | Descartada |
| ETC2 con BC3 preservado como RGBA | El usuario confirmó que la imagen todavía se veía borrosa | En título tardío: Graphics `1323300 kB`, RSS `1482540 kB`; cierre voluntario | Descartada |

Las mediciones de título, inicio y gameplay no se comparan como si fueran el mismo punto de carga. Se conservan para describir cada observación, no como benchmark de rendimiento.

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación | N/A | N/A | El paquete ya estaba instalado | N/A | Esta ejecución comparó perfiles gráficos |
| M-02 | Primer inicio con perfil final | Aprobado | Pantalla de título visible | ETC2 restaurado, 1280x720 | [captura](./evidencias/07-etc2-restaurado.png) | No se observaron errores de inicio en la ventana monitorizada |
| M-03 | Aperturas posteriores | Parcial | Al menos un relanzamiento final observado | Conteo total N/R | [memoria](./logs/memoria-etc2-restaurado.txt) | Se requiere repetición de larga duración |
| M-04 | Operación básica | Parcial | Audio, control y gameplay funcionales; fidelidad visual no equivalente | Control físico; observación del usuario | [gameplay](./evidencias/01-etc2-gameplay.png), [borde](./evidencias/02-etc2-bordes-transparentes.png) | La limitación no apareció de la misma forma en la referencia Mi A3 |
| M-05 | Aislamiento de archivos | N/A | N/A | No era objetivo de esta ejecución | N/A | El mecanismo sin duplicación no fue modificado |
| M-06 | Persistencia de archivos | Parcial | Perfil y registro restaurados antes del relanzamiento | Hash y contenido comprobados en el dispositivo | [contenedor](./logs/contenedor-final.json) | Persistencia a largo plazo N/R |
| M-07 | Tamaño del APK | N/R | N/R | No se reconstruyó el AAB/APK | N/A | |
| M-08 | Tiempo de instalación | N/A | N/A | No hubo instalación | N/A | |
| M-09 | Tiempo de primer inicio | N/R | N/R | `am start -W` midió la actividad Android, no el tiempo hasta gameplay | N/A | |
| M-10 | Tiempo de aperturas posteriores | N/R | N/R | No se tomó un cronómetro de extremo a extremo | N/A | |
| M-11 | Tasa de éxito | N/R | N/R | Un dispositivo y una secuencia de variantes | N/A | No se calcula una tasa sin repeticiones equivalentes |
| M-12 | Pasos manuales | Parcial | Control físico y selección diagnóstica por ADB | Prototipo todavía no autónomo | N/A | La detección automática queda pendiente de integración |

## Métricas por dispositivo

| Dispositivo | Instalación | Primer inicio | Segundo inicio | Operación | Persistencia | Tamaño APK | Tiempos | Tasa de éxito | Pasos manuales |
|---|---|---|---|---|---|---|---|---|---|
| Pixel 9a (`tegu`) | N/A | Aprobado con ETC2 | Parcial | Parcial: jugable con defecto visual | Parcial | N/R | N/R | N/R | Control físico; ADB para el prototipo |
| Xiaomi Mi A3 | N/A | N/R en esta ejecución | N/R | Solo referencia visual previa | N/R | N/R | N/R | N/R | N/R |

## Restauración final

El Pixel quedó con los siguientes binarios, comprobados después de detener la variante BC3:

| Componente | SHA-256 |
|---|---|
| `libbcn_layer.so` ETC2 | `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2` |
| `libVkLayer_BCN_BCnLayer.so` | `053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565` |

El registro de Wine se restauró desde el respaldo anterior a las pruebas de resolución. El hash cambia cuando Unity actualiza su contador o identificador de sesión; por ello el hash posterior al relanzamiento no se usa como identificador inmutable de configuración.

## Fallos y decisiones

- **Limitación relacionada:** [Limitación 14](../../limitaciones/14-fidelidad-texturas-pixel-tensor-mali.md).
- **Mensajes exactos:**

  ```text
  reason=9 (EXCESSIVE RESOURCE USAGE) subreason=7 (EXCESSIVE CPU USAGE)
  description=Caused by child process: excessive cpu 236490 during 300034 dur=209108 limit=25
  ```

  ```text
  reason=3 (LOW_MEMORY) subreason=0 (UNKNOWN)
  importance=100 pss=0,00 rss=3,1GB
  ```

- **Decisión:** aceptar provisionalmente en Pixel 9a el perfil Vortek/Gladio + DXVK-Sarek + ETC2 porque fue el único de los comparados que conservó juego, audio, control, texturas y estabilidad suficiente para la sesión manual. El borde visual se registra como limitación del dispositivo/perfil. No se habilitan automáticamente ASTC, Fcharan ni preservación BC3.

## Evidencias

- [Gameplay ETC2](./evidencias/01-etc2-gameplay.png)
- [Detalle del defecto en bordes](./evidencias/02-etc2-bordes-transparentes.png)
- [Referencia del Mi A3](./evidencias/03-mi-a3-referencia.png)
- [Variante ASTC](./evidencias/04-astc-720p.png)
- [Pantalla tras el crash Fcharan](./evidencias/05-fcharan-tras-crash.png)
- [Variante BC3 preservada](./evidencias/06-bc3-preservado.png)
- [Perfil ETC2 restaurado](./evidencias/07-etc2-restaurado.png)
- [ApplicationExitInfo de las variantes](./logs/application-exit-info-variantes.txt)
- [Memoria ETC2 durante gameplay](./logs/memoria-etc2-gameplay.txt)
- [Memoria ASTC](./logs/memoria-astc-inicio.txt)
- [Memoria BC3](./logs/memoria-bc3-preservado.txt), [muestra tardía](./logs/memoria-bc3-titulo-tardio.txt)
- [Memoria del ETC2 restaurado](./logs/memoria-etc2-restaurado.txt)
- [Formatos observados con ETC2](./logs/formatos-bcn-etc2.csv), [BC3 preservado](./logs/formatos-bcn-bc3-preservado.csv)
- [Inventario de metadatos Texture2D](./logs/inventario-texturas-unity.csv)

## Repetibilidad y pendientes

- [x] Restaurar el perfil ETC2 jugable y comprobar sus hashes.
- [x] Confirmar que 1080p, desactivar el efecto cromático, ASTC y preservar BC3 no corrigieron el defecto observado.
- [x] Rechazar la variante Fcharan que produjo texturas ausentes, stuttering y `LOW_MEMORY`.
- [ ] Integrar la selección por capacidades sin depender de ajustes ADB globales.
- [ ] Repetir una sesión de duración definida con telemetría comparable y el binario final integrado.
- [ ] Verificar el perfil en una versión estable de Android; esta prueba usó Android 17 beta/API 37.
