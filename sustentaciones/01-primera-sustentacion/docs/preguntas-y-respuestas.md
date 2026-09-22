# Preguntas difíciles y respuestas defendibles

Las respuestas están pensadas para 20 a 40 segundos. Si una pregunta exige
detalle, use `B` para abrir respaldo. No memorice cada frase: memorice la idea,
la evidencia y el límite.

## Propuesta y aporte

### 1. ¿Por qué no simplemente usar Winlator?

Porque Winlator resuelve la capacidad de ejecución, pero su flujo normal exige
que una persona prepare el contenedor, copie la aplicación, configure el acceso
directo, elija componentes y vuelva a repetir ese trabajo en cada dispositivo.
Win2APK usa esa base y automatiza una canalización por aplicación: configuración
declarativa, inventario, segmentación, identidad, firma, preparación Core,
arranque directo y evidencia. No negamos la dependencia; el aporte está en la
integración reproducible.

**Evidencia:** diapositiva 4, decisión CLI v2, especificación Core y código.

### 2. ¿Cuál es exactamente el aporte de Win2APK?

El aporte actual es un sistema de empaquetado e integración que convierte una
carpeta Windows preparada y una configuración explícita en artefactos Android,
configura el entorno de compatibilidad para esa aplicación y conserva reportes
y evidencia. También aporta una metodología de validación por dispositivo. No
aporta Wine, Box64 ni DXVK y no debe atribuirse su trabajo.

### 3. ¿Qué tiene de investigación y qué tiene de desarrollo?

El desarrollo produce la CLI, la variante Core, la entrega de datos, la UI y
los scripts. La investigación aparece al formular condiciones verificables,
comparar alternativas, medir en dispositivos, conservar fallos, aislar causas y
derivar decisiones. Por ejemplo, el límite del asset monolítico llevó a PAD; la
presión de memoria y pantallas negras llevaron a perfiles por GPU; el bloqueo
de ejecución con target moderno llevó a una decisión experimental documentada.

### 4. ¿Cuál es la novedad?

No defendemos novedad por “ejecutar x86 en ARM”, usar Wine o crear un paquete
autocontenido; la literatura ya cubre esas piezas. La brecha defendible dentro
del corpus revisado es integrar aplicación Windows, runtime, dependencias,
gráficos, almacenamiento, identidad Android y distribución en una canalización
reproducible y medible. Es una brecha del corpus de 48 estudios, no una prueba
de novedad mundial exhaustiva.

### 5. ¿Por qué crear un APK o un AAB?

Porque el formato Android aporta instalación, identidad de paquete, permisos,
firma, ciclo de vida y distribución. Para payloads grandes, el AAB permite
separar recursos en asset packs. El AAB es un formato de publicación; no es el
archivo ejecutable que se instala directamente, y no convierte el binario
Windows en código Android.

### 6. ¿Qué pasos manuales elimina hoy?

La CLI puede validar e inventariar, planear packs, preparar staging, configurar
identidad y runtime, generar artefactos, firmar, producir reportes e instalar
un APK set. En ejecución, Core puede preparar contenedor y acceso directo y
lanzar la aplicación sin exponer la interfaz general. Todavía son manuales la
preparación legal y técnica de la carpeta Windows, la elección inicial de
configuración y parte del diagnóstico cuando una aplicación falla.

### 7. ¿Win2APK es un conversor?

Solo en el sentido de convertir un conjunto de entrada en artefactos de
distribución. No traduce el código fuente a Kotlin ni produce una aplicación
Android nativa. La descripción académicamente correcta es “empaquetado,
distribución y ejecución mediante un entorno de compatibilidad”.

## Pregunta, hipótesis y objetivos

### 8. ¿Cuál es la pregunta de investigación?

La documentación actual todavía no contiene una pregunta formal aprobada. Esa
es una deuda que declaramos. La pregunta de trabajo que se deriva del objetivo,
pero que aún debe validarse con el equipo y la tutora, sería: “¿En qué medida
una canalización declarativa puede reducir la configuración manual necesaria
para empaquetar, distribuir y ejecutar aplicaciones Windows compatibles en
dispositivos Android ARM64?”. No la presentamos como formulación oficial.

### 9. ¿Cuál es la hipótesis?

Tampoco hay una hipótesis formal cerrada en el repositorio. Una formulación
operacional posible, todavía borrador, sería: “Si el runtime, las dependencias,
la configuración y la entrega de datos se preparan durante el build, entonces
aplicaciones compatibles podrán iniciar con menos pasos manuales y mayor
repetibilidad que en el flujo manual de línea base”. Para probarla haría falta
definir “menos pasos”, una muestra de aplicaciones y un criterio agregado de
éxito. Los resultados actuales son evidencia preliminar, no confirmación.

### 10. ¿Cómo se relacionan los resultados con la hipótesis de trabajo?

La CLI y Core demuestran que parte de la configuración puede trasladarse al
build. `EXEC-049` demuestra entrega de un payload grande y `EXEC-075` demuestra
arranque directo en un caso. `EXEC-074` demuestra que la repetibilidad todavía
depende del estado instalado. Por tanto, la evidencia apoya la viabilidad del
mecanismo, pero también muestra que aún no cumple un criterio amplio de éxito.

### 11. ¿Cuál sería el criterio para considerar exitoso Win2APK?

Debe definirse antes de la validación final. Como criterio defendible: para una
muestra predefinida de aplicaciones y dispositivos, construir artefactos
trazables, completar instalación fría, primer y segundo inicio, operación
básica, persistencia y limpieza sin configuración manual del runtime, dentro de
umbrales de tiempo, memoria y fallos previamente fijados. El proyecto ya mide
varias variables, pero no ha aprobado todavía ese criterio agregado.

## Arquitectura y conceptos

### 12. ¿Qué papel cumple Wine?

Wine implementa interfaces de Windows sobre sistemas POSIX. Traduce llamadas
de API Windows a servicios disponibles en el entorno; no ejecuta un kernel
Windows completo. En Win2APK, Wine resuelve la capa de compatibilidad del
programa, mientras Box64 resuelve la diferencia de arquitectura cuando el
binario y Wine son x86-64.

### 13. ¿Por qué Box64?

El hardware objetivo es ARM64 y muchas aplicaciones Windows y builds de Wine
son x86-64. Box64 ejecuta programas Linux x86-64 de espacio de usuario sobre
hosts ARM64 y puede usarse con Wine. El proyecto lo integra; no lo desarrolló.

### 14. ¿Por qué ARM64?

Es la arquitectura de los dispositivos Android usados y un objetivo frecuente
en teléfonos actuales. Elegirla también expone el reto central de reutilizar
software x86-64 sin recompilarlo. No afirmamos que el prototipo cubra todas las
ABI Android.

### 15. ¿Por qué Android?

Porque es el sistema de los dispositivos objetivo del proyecto, ofrece un
ecosistema de distribución y permite estudiar la reutilización de software en
hardware móvil. La justificación poblacional o de mercado todavía no fue
medida; la motivación actual es técnica y de accesibilidad potencial.

### 16. ¿Qué diferencia existe entre emulación, virtualización y traducción binaria?

- Virtualización ejecuta un sistema invitado con apoyo del hardware cuando las
  condiciones de arquitectura lo permiten.
- Emulación reproduce el comportamiento de otra máquina o arquitectura y es un
  término amplio.
- Traducción binaria transforma bloques de instrucciones de una ISA a otra,
  normalmente en tiempo de ejecución.

Win2APK combina una capa de compatibilidad de API, Wine, con traducción de
espacio de usuario, Box64. No inicia una máquina virtual Windows completa.

### 17. ¿Qué ocurre al cambiar de x86-64 a ARM64?

Las instrucciones, registros, banderas y modelo de memoria no son idénticos.
Box64 traduce bloques y envuelve llamadas a bibliotecas nativas cuando puede.
Eso introduce cobertura parcial y sobrecarga. La literatura de Box64 demuestra
viabilidad en plataformas concretas, pero sus cifras no predicen el rendimiento
de Android ni de una aplicación no evaluada.

### 18. ¿Qué papel cumple DXVK?

DXVK traduce Direct3D 8 a 11 a Vulkan para ejecutar aplicaciones 3D en Linux
con Wine. Es una opción de la ruta gráfica; algunas variantes usan WineD3D u
otros componentes. El driver y la GPU determinan si esa ruta funciona.

### 19. ¿Qué pasa con DirectX 12?

DXVK no cubre Direct3D 12. En ecosistemas Wine suele usarse VKD3D-Proton o
VKD3D, pero la presentación no afirma que la configuración actual de Win2APK
lo valide. Una aplicación D3D12 requeriría especificar y probar esa ruta.

### 20. ¿Qué papel cumplen Mesa, Turnip, Zink o VirGL?

Son opciones o componentes de la ruta gráfica. Turnip es un driver Vulkan de
Mesa para ciertas GPU Adreno; Zink implementa OpenGL sobre Vulkan; VirGL se
relaciona con renderizado virtualizado. Win2APK no usa todos al mismo tiempo ni
puede suponer que una configuración sirve para Mali y Adreno. Los experimentos
del Pixel demostraron esa necesidad de selección.

### 21. ¿Por qué no usar QEMU?

El proyecto heredó y validó una arquitectura Winlator basada en Box64 y Wine.
QEMU sería una alternativa que debe compararse bajo los mismos criterios de
compatibilidad, rendimiento, integración y tamaño antes de adoptarse. No se
descartó mediante un benchmark completo dentro de este proyecto, por lo que no
afirmamos que sea inferior en todos los casos.

## Compatibilidad y aplicaciones

### 22. ¿Esto realmente ejecuta aplicaciones Windows?

Sí, en el sentido de que binarios Windows concretos se han iniciado mediante
Wine y Box64 dentro del entorno Android. Se observaron Win2APKTest, Cuphead y
Bomb Rush Cyberfunk en estados documentados. No significa que Android ejecute
el binario directamente ni que todas las aplicaciones funcionen.

### 23. ¿Qué tan compatible es?

No existe una tasa de compatibilidad válida todavía. La compatibilidad depende
de arquitectura, APIs, runtime, gráficos, drivers, memoria y comportamiento de
la aplicación. El proyecto reporta por aplicación, build y dispositivo. La
respuesta correcta hoy es “compatibilidad experimental y específica”.

### 24. ¿Pueden afirmar compatibilidad universal?

No. Los resultados de un dispositivo o juego no se extrapolan. Incluso el mismo
paquete reciente llegó al título en Redmi y falló antes del contenedor en la
instalación de Lenovo.

### 25. ¿Qué aplicaciones han probado?

- Win2APKTest, una aplicación .NET de prueba controlada.
- Cuphead, usado para payload grande, PAD y ejecución.
- Bomb Rush Cyberfunk, usado para flujo actual, UI y gamepad.

No todas las ejecuciones cubren el mismo nivel de operación. Debe mencionarse el
ID de ejecución cuando se afirma un resultado.

### 26. ¿Qué pasa con aplicaciones .NET?

Depende de su publicación y runtime. La primera prueba de CoreCLR falló al
inicializar el heap. Una publicación self-contained con ajustes de GC funcionó
para Win2APKTest en Lenovo. Eso demuestra una estrategia para ese caso, no que
todo .NET sea compatible.

### 27. ¿Qué pasa con aplicaciones de 32 bits?

La arquitectura actual y la documentación se concentran en arm64-v8a y cargas
x86-64. Box86, Box32 o Wine WOW64 pueden cubrir rutas de 32 bits, pero su soporte
debe verificarse en la configuración concreta. No se presenta como resultado
principal validado.

### 28. ¿Funciona sin Internet?

La presentación y el video sí. El paquete puede operar sin red después de tener
el payload local, según la estrategia. La distribución real por PAD depende de
Google Play; las pruebas locales usan APK set y packs instalados con bundletool.
Por eso “sin Internet” debe referirse al estado posterior a la entrega, no al
proceso completo de publicación.

## Validación y métricas

### 29. ¿Cuál es la validación técnica realizada?

Hay ejecuciones numeradas con artefacto, hash, dispositivo, método, duración,
procesos, captura T+60, logs y métricas. Incluyen construcción de APK/AAB/APKS,
instalación, entrega de packs, primer inicio, relanzamiento, gráficos, memoria,
UI, gamepad y errores. Son 75 ejecuciones de distinto alcance; no deben contarse
como 75 pruebas completas equivalentes.

### 30. ¿Cuál es la muestra de dispositivos y por qué esos?

Pixel 9a, Redmi Note 8, Xiaomi Mi A3 y Lenovo TB-J606F. La muestra aporta
teléfono y tablet, familias Mali y Adreno, y distintas versiones Android. Fue
una muestra disponible y orientada a encontrar variación, no una muestra
estadística del mercado.

### 31. ¿Qué métricas usan?

Instalación, tiempo de lanzamiento, primer frame observado, presencia de
procesos, CPU, RSS/PSS, memoria disponible, GPU cuando es accesible, FPS,
temperatura, almacenamiento, captura T+60, resultado y notas. Cada métrica debe
leerse con sus condiciones. Por ejemplo, FPS en un menú no mide jugabilidad.

### 32. ¿Por qué T+60?

Es un punto canónico que permite comparar runs y evita seleccionar solo una
captura favorable. No reemplaza una serie temporal ni garantiza que el estado
posterior sea estable. Por eso también se conservan muestras, logs y capturas
suplementarias cuando hay interacción.

### 33. ¿Cómo saben que la solución de CoreCLR funciona?

Porque después del cambio se observó el proceso, la ventana de Win2APKTest y
respuestas al botón, con registro de consola, en `EXEC-001`. Sabemos que funciona
para esa publicación y ese entorno. No sabemos todavía su tasa de éxito sobre
otras aplicaciones .NET.

### 34. ¿Qué ocurrió con el payload de Cuphead?

Un asset único de 4,782,573,186 bytes produjo `Required array size too large`.
El diseño cambió a AAB y varios asset packs. Después la CLI produjo artefactos
multigigabyte y `EXEC-049` observó 815 archivos y 5.847 GB entregados, con el
proceso `Cuphead.exe` activo. Esto valida entrega y arranque, no operación total.

### 35. ¿Por qué el resumen dice `failed_install` en la demo exitosa?

Es una limitación conocida del agregador. En modo
`preinstalled-no-reinstall` no existe una fila de instalación porque instalar
no forma parte del experimento. El agregador interpreta la ausencia como fallo.
Los CSV históricos se conservan y la matriz corrige la interpretación con la
evidencia de procesos y pantalla. Es la limitación 37.

### 36. ¿Por qué no corrigen el CSV?

Porque es una salida histórica generada. Reescribirla borraría la traza del
defecto. La práctica del proyecto es conservarla, documentar la revisión en la
matriz y corregir el agregador en una versión futura con una prueba automática.

### 37. ¿Qué ocurrió en la Lenovo antes de la sustentación?

La app abrió, pero Play Core no encontró
`win2apk_payload_002` en el proveedor de pruebas locales. El diálogo indicó que
no podía crear contenedor o acceso directo. El log localiza el punto de fallo;
no demuestra aún por qué el pack falta. Se requiere una instalación fría con
todos los splits y packs. Por eso Lenovo no es el dispositivo de demo.

### 38. ¿Qué significa “aprobado experimentalmente”?

Que se cumplió el estado esperado bajo las condiciones registradas de esa
ejecución. No significa apto para producción, compatible con todo dispositivo o
validado por usuarios.

## Android, distribución y seguridad

### 39. ¿Por qué usan target SDK 28?

En los experimentos con target 36, SELinux bloqueó la ejecución de Box64 desde
datos de la app. Volver a target 28 restauró esa ruta en la matriz v48. Es una
decisión experimental para mantener la ejecución, no una solución de
publicación. La versión actual no cumple los requisitos modernos de Google Play
y esa tensión es una limitación central.

### 40. ¿Está listo para Google Play?

No. Aunque el proyecto genera AAB y usa conceptos de PAD, el target actual y
otras exigencias de publicación requieren trabajo. También deben revisarse
tamaño, licencias, derechos sobre el software empaquetado, políticas de código
ejecutable y pruebas de distribución real.

### 41. ¿Qué diferencia hay entre AAB, APKS y APK?

- AAB: formato de publicación que contiene módulos y recursos.
- APKS: archivo producido por bundletool con el conjunto de APK que corresponde
  a una distribución o prueba.
- APK: unidad instalable específica.

La CLI conserva AAB y APKS porque cumplen funciones distintas.

### 42. ¿Qué es Play Asset Delivery?

Es el mecanismo de Google Play para entregar asset packs asociados a un App
Bundle mediante modos como install-time, fast-follow y on-demand. Win2APK lo
usa como arquitectura de distribución de datos grandes y lo prueba localmente
con bundletool. La entrega real de Play todavía debe validarse.

### 43. ¿Qué riesgos de seguridad existen?

Se integran código nativo, un entorno Linux, traducción binaria y aplicaciones
de terceros. Los riesgos incluyen bibliotecas desactualizadas, permisos,
procedencia de binarios, aislamiento, código no confiable y superficie de
compatibilidad. El paquete no debe incluir claves privadas ni software sin
derechos. Una evaluación de seguridad completa aún es trabajo pendiente.

### 44. ¿Qué partes son desarrolladas por ustedes?

La CLI, sus esquemas y reportes; la integración de configuración y paquete
dinámicos; adaptaciones de Winlator Core; entrega y limpieza de payload;
selección gráfica experimental; UI adaptativa y gamepad; scripts de medición;
matrices, limitaciones y documentación. La lista exacta puede auditarse en los
commits del repositorio raíz y de `winlator/app`.

### 45. ¿Qué tecnologías de terceros utilizan?

Winlator, Wine, Box64, Mesa y drivers, DXVK o WineD3D, componentes Android y
bundletool, además de bibliotecas específicas documentadas en
`third_party/README.md`. No todas se activan para toda configuración.

### 46. ¿Qué implicaciones tienen las licencias?

La variante local conserva LGPL 2.1 en el repositorio Winlator y hay componentes
con licencias propias, como MIT u otras. Antes de distribuir se requiere un
inventario por binario, conservar avisos, publicar fuentes o cambios cuando la
licencia lo exija y verificar que la aplicación Windows pueda redistribuirse.
La investigación no sustituye revisión jurídica.

## Impacto y trabajo futuro

### 47. ¿Qué problema real resuelve?

Reduce la barrera técnica de repetir un entorno de compatibilidad por aplicación
y dispositivo. El problema está demostrado como complejidad de integración. La
magnitud del problema para usuarios finales todavía no se midió mediante un
estudio de campo.

### 48. ¿Cuál es el impacto del proyecto?

El impacto observado es técnico: automatización, trazabilidad y conocimiento
sobre límites. El impacto potencial es facilitar reutilización de software
Windows compatible y reducir pasos especializados. No se ha medido impacto
social, económico ni ambiental; por eso no se presenta como resultado.

### 49. ¿Qué falta para completar el proyecto?

Formalizar pregunta, hipótesis y criterio agregado de éxito; ampliar la muestra
de aplicaciones; ejecutar instalaciones frías y segundos inicios; resolver la
tensión entre target moderno y ejecución; fortalecer compatibilidad gráfica;
automatizar clasificación correcta de runs preinstalados; hacer pruebas de
usuarios, seguridad, licencias y distribución real.

### 50. ¿Cuál sería el siguiente experimento más valioso?

Una matriz predefinida de aplicaciones y dispositivos, con instalación fría,
primer y segundo inicio, operación básica y criterios de salida iguales. Para el
problema inmediato, repetir Lenovo con todos los splits y packs y comparar el
estado de Play Core antes y después. Para la arquitectura, probar una ruta
compatible con un target moderno sin ejecutar binarios desde ubicaciones
restringidas.

## Respuestas de seguridad cuando falta evidencia

Use estas fórmulas sin improvisar:

- “Ese resultado no está medido todavía; lo tratamos como hipótesis.”
- “La evidencia permite afirmar X en este dispositivo, pero no generalizar Y.”
- “El log localiza el fallo en esta capa; falta una prueba que aísle la causa.”
- “La decisión es experimental y conserva una deuda de publicación.”
- “No tengo una cifra defendible para eso. El siguiente experimento sería...”
