# Ejecución 17: extracción y limpieza autónoma con PAD on-demand

- **ID:** `EXEC-017`
- **Fecha:** 2026-08-24
- **Tipo:** compilación, instalación y prueba de almacenamiento
- **Resultado general:** aprobado experimentalmente en Mi A3
- **Método:** solicitar packs, extraer en staging, confirmar marcador, retirar packs y limpiar la fuente local de bundletool
- **Rama de integración:** `codex/no-duplicate-game-data`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | Paquete `com.cuphead` |
| Versión | `11.1-core`, `versionCode=28` | Configuración de build |
| Ejecutable | `C:\\Cuphead\\Cuphead.exe` | Shortcut de Winlator Core |
| AAB | `5.043.892.907` bytes; SHA-256 `c7ff8987aa39255099a1921357d0c11d022a26e1608b4b5f6131540c29a27030` | Build del worktree aislado |
| APK set | `5.052.952.798` bytes; SHA-256 `d919bd4f025bded6fa5f1dfc274bf4a3f9740431b6ae4a73c41fb2e4c65074e4` | bundletool `--local-testing` |
| Bundletool | `1.18.3` | Instalación local |
| Entorno | Winlator Core + Asset Delivery `2.3.0` | Packs `on-demand` |
| Dispositivo/variante | Xiaomi Mi A3, serial `51c803a01206` | Dispositivo físico |
| Android/API | API 36 | Inventario previo a la prueba |
| ABI | N/R | No registrado durante esta ejecución |
| Resolución | N/R | No registrada durante esta ejecución |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Compilar Java y AAB | Aprobado | `BUILD SUCCESSFUL` | JDK 17 | [build y dispositivo](./logs/resultado.md) | El primer intento accidental con JDK 21 no corresponde a un fallo del código |
| M-02 | Descargar tres packs | Aprobado | 3/3, `status=4`, `error=0` | bundletool local testing | [build y dispositivo](./logs/resultado.md) | Se abrió cada parte desde `assetsPath()` |
| M-03 | Extracción transaccional | Aprobado | rootfs `6.732.416` KiB | Directorio staging + marcador posterior | [build y dispositivo](./logs/resultado.md) | El marcador sólo se escribió tras extraer y renombrar |
| M-04 | Retirar packs descargados | Aprobado | `files/assetpacks=28` KiB | Después del marcador | [build y dispositivo](./logs/resultado.md) | `removePack()` devolvió finalización para los tres packs |
| M-05 | Eliminar fuente local de bundletool | Aprobado | `local_testing` ausente; datos externos `7` KiB | Sólo directorio propio de la app | [build y dispositivo](./logs/resultado.md) | No se borró `assetsPath` antes de terminar la extracción |
| M-06 | Conservar una sola copia persistente del juego | Aprobado experimentalmente | copia en rootfs; fuentes PAD retiradas | Medición posterior | [build y dispositivo](./logs/resultado.md) | Resultado limitado a este dispositivo y build |
| M-07 | Relanzar sin descargar ni extraer | Aprobado | 1/1 | Marcador presente, packs ausentes | [build y dispositivo](./logs/resultado.md) | Log: `skipping asset extraction` |
| M-08 | Ejecutar Cuphead | Aprobado experimentalmente | proceso `Cuphead.exe` iniciado | Segundo arranque | [build y dispositivo](./logs/resultado.md) | Llegó a `XServerDisplayActivity` |

## Almacenamiento observado

| Etapa | Espacio libre `/data` | Fuente externa | Packs internos | Rootfs |
|---|---:|---:|---:|---:|
| Antes de instalación limpia | `33.169.560` KiB | `4` KiB | N/A | N/A |
| Tras bundletool, antes de abrir | `27.967.396` KiB | `4.939.376` KiB | N/R | N/R |
| Packs descargados | N/R | `4.939.376` KiB observados antes de limpieza | `4.675.307` KiB | extracción en curso |
| Final, tras limpieza y relanzamiento | `26.257.908` KiB | `7` KiB | `28` KiB | `6.732.416` KiB |

El pico máximo exacto no se registró en una sola lectura simultánea. Sí se observó coexistencia temporal de la fuente externa, los packs internos y la extracción; por ello este enfoque requiere espacio temporal adicional aunque termine con una sola copia persistente.

## Decisión

Integrar este modo como solución funcional de una sola copia final. Mantener la variante de archivos directos como comparación porque puede evitar extraer el juego al prefijo, pero no presentar esa variante como completa hasta probar Cuphead a escala real.

## Fallos y decisiones

- **Limitación relacionada:** [Limitación 13](../../limitaciones/13-fuente-bundletool-local-testing-duplicada.md)
- **Mensaje exacto del intento previo corregido:** N/A en esta ejecución final.
- **Decisión:** aceptar el modo `on-demand` con marcador y limpieza; documentar el pico temporal.

