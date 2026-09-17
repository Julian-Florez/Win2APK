# Ejecución 18: prototipo STORAGE_FILES y árbol de enlaces

- **ID:** `EXEC-018`
- **Fecha:** 2026-08-24
- **Tipo:** prueba reducida de acceso directo y almacenamiento
- **Resultado general:** aprobado para el mecanismo; ejecución completa de Cuphead pendiente en esta matriz
- **Método:** pack `on-demand` con archivos anidados, lectura directa y prefijo de enlaces simbólicos

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Direct Files Probe | Paquete temporal `com.win2apk.directfiles.probe` |
| Versión | `versionCode=3` | Build final de la prueba reducida |
| AAB | `2.316.159` bytes | Build aislado |
| APK set | `9.650.226` bytes | bundletool `--local-testing` |
| Dispositivo/variante | Pixel 9a, serial ADB de red | Dispositivo físico |
| Android/API | API 37 | `getprop` |
| ABI | `arm64-v8a` | `getprop ro.product.cpu.abilist` |
| Resolución | `1080x2424` física | `wm size` |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Obtener una ruta POSIX del pack | Aprobado | `storageMethod=0` | Pack `on-demand` completado | [registro](./logs/direct-files.md) | `assetsPath` no fue nulo |
| M-02 | Leer archivos anidados | Aprobado | 4/4 | API de archivos estándar | [registro](./logs/direct-files.md) | Rutas y tamaños enumerados |
| M-03 | Lectura aleatoria y mmap | Aprobado | 1 archivo de muestra | `FileChannel` | [registro](./logs/direct-files.md) | `seek` y `mmap` devolvieron datos |
| M-04 | Crear prefijo sin copiar contenidos | Aprobado | 4 enlaces; `copiedBytes=0` | Misma UID de la aplicación | [registro](./logs/direct-files.md) | Los enlaces fueron legibles |
| M-05 | Sobrevivir reinicio | Aprobado | 1/1 | `force-stop` y reapertura | [registro](./logs/direct-files.md) | Pack y enlaces siguieron disponibles |
| M-06 | Detectar cambio de versión del pack | Aprobado | ruta `/1/1/` a `/2/2/` | Actualización del probe | [registro](./logs/direct-files.md) | El árbol debe reconstruirse tras actualizar |
| M-07 | Medir la fuente local de bundletool | Aprobado | `7.240.952` bytes, 77 archivos | Después de `COMPLETED` | [registro](./logs/direct-files.md) | Era una copia temporal adicional |
| M-08 | Eliminar sólo la fuente local | Aprobado | `local_testing` ausente | Después de validar enlaces | [registro](./logs/direct-files.md) | No invalidó el pack interno |
| M-09 | Ejecutar Cuphead completo | N/R | N/R | Fuera de la prueba reducida | N/A | Se registrará como ejecución separada |

## Interpretación

PAD `on-demand` cambió el resultado de `EXEC-015`: en este Pixel el pack fue `STORAGE_FILES` y sí ofreció una carpeta utilizable por Wine. Esto no contradice el diagnóstico anterior, que correspondía a packs `install-time` instalados como `APK_ASSETS`.

La actualización cambió la ruta física del pack; por ello Win2APK debe resolver `assetsPath()` y validar o reconstruir los enlaces en cada arranque. La fuente que bundletool deja en `local_testing` también debe limpiarse después de `COMPLETED` y de validar el árbol.

Cuphead contiene 815 archivos por `5.847.372.363` bytes en la instalación legal local, y el mayor archivo observado mide `218.959.588` bytes. La prueba reducida apoya repartir archivos completos entre varios packs, pero todavía no demuestra el arranque del juego completo.

