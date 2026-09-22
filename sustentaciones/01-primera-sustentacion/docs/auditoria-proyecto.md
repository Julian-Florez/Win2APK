# Auditoría del proyecto para la primera sustentación

Fecha de corte: **22 de septiembre de 2026**.

## Resumen ejecutivo

Win2APK es hoy un proyecto de investigación y desarrollo con tres piezas
materiales:

1. Una CLI en Rust para validar, planear, construir, firmar e instalar
   artefactos derivados de una carpeta de aplicación Windows preparada.
2. Una variante de Winlator Core que recibe configuración por aplicación,
   prepara el entorno, oculta la interfaz general y lanza el acceso directo.
3. Un protocolo versionado de experimentación con dispositivos Android, CSV,
   logs, captura T+60, clasificación visual y matrices narrativas.

El sistema no convierte código Windows a una aplicación Android nativa. Integra
empaquetado, distribución y ejecución mediante un entorno de compatibilidad.
La evidencia permite afirmar viabilidad experimental en casos concretos, pero
no compatibilidad universal, publicación moderna resuelta ni impacto de usuario
medido.

## Alcance auditado

Se revisaron:

- `README.md`, archivos raíz, configuración Cargo y ejemplos.
- Los 15 documentos numerados de `documentacion/` y sus índices.
- Las especificaciones de CLI, Winlator Core, distribución, aplicación mínima
  e interfaz adaptativa.
- Las matrices `EXEC-001` a `EXEC-073` y, durante esta preparación,
  `EXEC-074` y `EXEC-075`.
- Los informes numerados de `limitaciones/`; el nuevo resultado generó el
  informe 43.
- `metricas/`, sus catálogos, scripts y runs estructurados.
- La CLI en `cli/src/`.
- La variante Android en `winlator/app` y su diferencia frente al upstream.
- La revisión PRISMA, matrices de evidencia e informes de artículos.
- Historial, ramas, submódulos, remotos y estado de Git.
- Dispositivos visibles por ADB, paquetes instalados, propiedades, procesos,
  capturas, logs y grabaciones.

## Estado de Git al iniciar

- Repositorio raíz: limpio, rama
  `codex/no-duplicate-game-data`, commit `ee401d8` del 20 de septiembre,
  “Publish Material 3 gamepad and adaptive UI (Win2APK)”.
- Repositorio de la app: limpio, rama `codex/no-duplicate-game-data`, commit
  `0fb7c1f` del 20 de septiembre.
- Superproyecto Winlator: limpio, rama
  `agent/winlator-core-dynamic-package`, commit `718d67e`.
- No se encontraron tags en el repositorio raíz.

La rama actual contiene la evolución de CLI, validación en dispositivos y
Material 3 que no estaba consolidada en la rama local `main`. Por eso se usó la
rama actual como estado técnico reciente y no se retrocedió a `main`.

## Problema, objetivo, pregunta e hipótesis

### Problema respaldado

Los documentos de contexto y la línea base muestran que ejecutar una aplicación
Windows en Android con Winlator requiere decisiones especializadas: publicar o
preparar la aplicación, copiar dependencias, configurar contenedor y acceso
directo, seleccionar traducción gráfica, resolver la diferencia x86-64/ARM64 y
distribuir archivos que pueden ser muy grandes.

### Objetivo recuperado

El objetivo coherente con el código reciente es automatizar el empaquetado y la
preparación de un entorno de compatibilidad para distribuir y ejecutar
aplicaciones Windows compatibles en Android ARM64, reduciendo configuración
manual y conservando trazabilidad.

### Hallazgo documental

No se encontró una pregunta de investigación formal ni una hipótesis final
aprobada en los documentos actuales. `documentacion/00-contexto-del-proyecto.md`
reconoce que ambas deben formularse. Por eso la presentación no inventa una
redacción oficial. La deuda se declara en la diapositiva 3 y se prepara una
respuesta académica en el documento de preguntas.

## Arquitectura reconstruida

### Build time, Linux x86-64

1. La CLI carga y valida un JSON de esquema v2.
2. Inventaría archivos, tamaños y hashes.
3. Planea la segmentación entre módulo base y asset packs.
4. Prepara configuración del runtime, identidad, iconos y staging.
5. Ejecuta Gradle y herramientas Android.
6. Firma externamente el AAB cuando corresponde.
7. Genera AAB, APKS, reporte, manifiesto, checksums y copia de configuración.

Comandos implementados: `setup`, `doctor`, `validate`, `plan`, `build`,
`install`, `keys` y `clean`.

### Run time, Android ARM64

1. La app recibe o encuentra el payload entregado por módulos o pruebas
   locales.
2. Winlator Core prepara rootfs, contenedor y acceso directo.
3. El payload se mueve de forma transaccional y se limpia la fuente para dejar
   una copia final cuando la estrategia lo permite.
4. Box64 ejecuta código de espacio de usuario x86-64 sobre ARM64.
5. Wine resuelve interfaces Windows sobre el entorno POSIX.
6. DXVK o WineD3D, junto con drivers Mesa u otras rutas integradas, llevan la
   salida gráfica a la GPU.

## Diferencia defendible frente a Winlator

Winlator aporta la base de compatibilidad y ejecución. Win2APK aporta la
canalización por aplicación:

- configuración declarativa;
- inventario y validación previa;
- identidad y paquete propios;
- segmentación y entrega del payload;
- configuración Core y arranque directo;
- perfiles gráficos por capacidades observadas;
- interfaz adaptativa y gamepad táctil;
- firma, reportes y checksums;
- pruebas reproducibles y documentación de fallos.

La contribución no es inventar Wine, Box64 o DXVK. La revisión de literatura
también rechaza la novedad basada solo en traducción binaria o paquetes
autocontenidos. La brecha defendible es integrar esas piezas en una unidad
distribuible y verificable para Android.

## Cronología técnica resumida

| Etapa | Evidencia | Aprendizaje |
|---|---|---|
| Línea base manual | Limitación 01 y `EXEC-001` | CoreCLR requiere una publicación y un GC adecuados al entorno. |
| APK inicial | `EXEC-003` a `EXEC-008` | Se puede construir, instalar, crear contenedor y lanzar una app de prueba. |
| Payload grande | `EXEC-012` a `EXEC-018` | Un asset monolítico de 4.45 GiB falla; PAD y múltiples packs son necesarios. |
| Gráficos por dispositivo | `EXEC-020`, `EXEC-024` a `EXEC-031` | Mali y Adreno no comparten una configuración gráfica segura. |
| Compatibilidad Android moderna | `EXEC-038` a `EXEC-044` | `targetSdk 36` bloqueó experimentalmente la ejecución desde datos; 28 restauró el flujo, con una deuda de publicación. |
| CLI declarativa | `EXEC-047` a `EXEC-049` | Limpieza por build y firma externa resolvieron artefactos obsoletos y memoria de AGP. |
| Interfaz adaptativa | `EXEC-051` a `EXEC-065` | La interfaz y el panel se ajustaron para teléfono y tablet. |
| Gamepad | `EXEC-068` a `EXEC-073` | Se observaron controles Material 3 y feedback visual, con resultados distintos por dispositivo. |
| Preparación de sustentación | `EXEC-074` y `EXEC-075` | Redmi es la ruta de demo; Lenovo reproduce un pack local ausente. |

## Evidencia cuantitativa seleccionada

- `EXEC-003`: APK debug arm64-v8a de aproximadamente 150 MB, firma verificada.
- `EXEC-005`: 463 archivos y publicación Windows de 161 MB copiados para la
  aplicación de prueba.
- `EXEC-047`: TestApp AAB de 490,787,881 bytes y APKS de 744,602,045 bytes;
  Cuphead AAB de 5,494,326,036 bytes y APKS de 6,424,836,814 bytes.
- `EXEC-049`: 815 archivos y 5.847 GB entregados; `Cuphead.exe` observable en
  el Mi A3.
- `EXEC-075`: app visible a 2.274 s, juego visible a 2.275 s, primer frame
  observado a 6.353 s, ambos procesos observables durante 120 s, pantalla de
  título a T+60.

El valor de FPS de `EXEC-075` se conserva en el CSV, pero no se usa como
jugabilidad porque la ventana observó carga y título.

## Errores y decisiones relevantes

### CoreCLR / GC

- Observación: `GC heap initialization failed with error 0x8007000E` y
  `Failed to create CoreCLR, HRESULT: 0x8007000E`.
- Cambio: publicación .NET self-contained, GC workstation no concurrente,
  límite de heap y diagnóstico por consola.
- Evidencia posterior: `EXEC-001` muestra Win2APKTest abierto e interactivo.
- Alcance: solución experimental para esa publicación y dispositivo.

### Asset de Cuphead demasiado grande

- Observación: `Required array size too large` al intentar un asset único de
  4,782,573,186 bytes.
- Cambio: AAB y varios asset packs con entrega configurada.
- Evidencia posterior: `EXEC-049` conserva inventario, entrega y proceso.

### Gradle reutilizó un AAB anterior

- Observación: una configuración podía recibir un artefacto de otra.
- Cambio: limpieza por build.
- Evidencia: limitación 35 y `EXEC-047`.

### Memoria de AGP con AAB multigigabyte

- Observación: el firmador integrado agotó memoria.
- Cambio: firma externa con herramientas JDK.
- Evidencia: limitación 36 y `EXEC-047`.

### Ejecución y target SDK

- Observación: la variante moderna con target 36 recibió denegaciones SELinux
  al ejecutar Box64 desde datos de app.
- Cambio experimental: target 28 restauró ejecución en la matriz v48.
- Límite: no satisface los requisitos modernos de publicación de Google Play.

### Pack local-testing ausente en Lenovo

- Observación visible: `Unable to create the configured container or shortcut.`
- Log exacto: `No APKs available for pack 'win2apk_payload_002'.`
- Decisión: conservar el estado, no reinstalar, documentar limitación 43 y usar
  Redmi para la demo.
- Pendiente: instalación fría controlada con todos los splits y packs.

## Pruebas ejecutadas para esta entrega

### CLI

- `cargo test --workspace --all-targets`: 2 pruebas superadas.
- `cargo clippy --workspace --all-targets -- -D warnings`: superado.
- `cargo run -- validate config/example.testapp.json`: configuración válida,
  463 archivos, 167,479,464 bytes, un pack.
- `cargo run -- plan config/example.testapp.json`: plan escrito y coherente con
  el inventario anterior.

### Dispositivos

Se detectaron Redmi Note 8 y Lenovo TB-J606F. En ambos existía
`com.win2apk.bombrushcyberfunk`, versionCode 1, versionName
`gog-56774571391351451`, targetSdk 28.

No se reinstaló ni borró información. Se extrajo el APK base instalado como
artefacto de referencia, se lanzó el paquete, se monitoreó 120 s, se capturó
T+60 y se grabaron 45 s. Los runs estructurados son:

- `RUN-20260922-001` / `EXEC-074`: Lenovo, `error_screen`.
- `RUN-20260922-002` / `EXEC-075`: Redmi, `title_screen`.

## Revisión bibliográfica

La revisión local reconstruyó 98 PDF físicos, eliminó 6 duplicados, evaluó 75
textos completos e incluyó 48 estudios. Los resultados apoyan cinco familias:
traducción binaria, capas de compatibilidad, gráficos, empaquetado reproducible
y seguridad/reproducibilidad.

La literatura demuestra que varias piezas ya existen y tienen investigación
propia. No se encontró en el corpus una demostración directa de un builder que
produzca la unidad completa aplicación Windows + runtime + dependencias +
distribución Android como la que investiga Win2APK. Esta es una brecha del
corpus revisado, no una prueba mundial de novedad.

## Contradicciones y decisiones de trazabilidad

1. **Idea inicial de aplicación de escritorio frente a CLI actual.** Los
   documentos tempranos describen un builder de escritorio. La decisión 13 y
   el código reciente establecen una CLI Rust para Linux x86-64 como alcance
   v0.1. La presentación usa el estado reciente.
2. **Ejecución manual frente a Core oculto.** `EXEC-001` es línea base manual.
   `EXEC-007` y posteriores documentan arranque directo. Se usan como etapas,
   no como descripciones simultáneas.
3. **`failed_install` en runs preinstalados.** El agregador marca fallo si no
   hay fila de instalación. La limitación 37 demuestra que esto es incorrecto
   para `preinstalled-no-reinstall`. Los CSV se conservan; las matrices 074 y
   075 corrigen la interpretación explícitamente.
4. **Objetivo de publicación moderna frente a target 28.** El prototipo actual
   ejecuta con target 28 por una restricción observada. La publicación en
   Google Play moderno no se presenta como resuelta.
5. **Pregunta e hipótesis.** Están pendientes en la documentación y se muestran
   como deuda, no se reconstruyen retroactivamente.

## Estado real al corte

### Implementado

- CLI declarativa y comandos principales.
- Generación de AAB, APKS, reportes, checksums y configuración.
- Winlator Core con paquete, rootfs y acceso directo variables.
- Arranque directo y UI adaptativa.
- Distribución segmentada y limpieza de payload.
- Perfiles gráficos experimentales y gamepad táctil condicional.
- Protocolo reproducible de métricas y registros de limitaciones.

### Validado con alcance limitado

- Aplicación .NET de prueba.
- Cuphead en varias etapas de distribución y ejecución.
- Bomb Rush Cyberfunk con título y controles visibles en dispositivos
  concretos.
- Teléfonos y tablet, GPUs Adreno y Mali, versiones Android diversas.

### Pendiente

- Pregunta e hipótesis formales.
- Compatibilidad con una muestra mayor de aplicaciones y rutas de instalación.
- Publicación compatible con requisitos modernos sin bloquear Box64.
- Corrección de limitaciones por GPU y estado de asset packs.
- Pruebas de usuario y medición de impacto.
- Criterio agregado de éxito del producto.

## Conclusión de auditoría

La sustentación puede defender un diseño coherente y un prototipo real porque
existen código, artefactos, ejecuciones y evidencia visual. La afirmación
correcta es que Win2APK ha demostrado una canalización experimental en casos
concretos. La afirmación incorrecta sería que ya convierte cualquier programa
Windows o que está listo para publicación general.
