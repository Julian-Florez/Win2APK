# Guion oral de la primera sustentación

Duración objetivo: **6:40**. Margen hasta el límite: **20 segundos**.

Los tiempos incluyen cambios de diapositiva. No se debe acelerar para añadir
detalles; use las diapositivas de respaldo durante preguntas.

## Preparación antes de entrar

1. Cargar el Redmi Note 8 por encima de 50 % y activar modo avión.
2. Confirmar que `com.win2apk.bombrushcyberfunk` abre hasta la pantalla de
   título. No reinstalar el día de la exposición salvo que se ejecute un run
   controlado nuevo.
3. Abrir la presentación con `presentar.sh` o `presentar.bat`.
4. Pulsar `F` y comprobar que el video funciona con `V`.
5. Dejar el teléfono desbloqueado, en horizontal y con brillo suficiente.
6. Tener abierto `presentacion-win2apk.pdf` como último respaldo.

## 0:00-0:20 · Diapositiva 1 · Presentador A

**Objetivo:** abrir con la tensión central sin vender una solución universal.

**Decir:**

> ¿Qué tendría que ocurrir para que una aplicación Windows dejara de ser una
> carpeta difícil de configurar y pudiera distribuirse como una experiencia
> Android repetible? Win2APK investiga esa ruta. No convierte el programa en
> Android nativo: empaqueta y prepara un entorno de compatibilidad para
> ejecutarlo en dispositivos ARM64.

**No explicar:** Wine, Box64 ni DirectX todavía.

**Cambio:** avanzar al terminar “ARM64”.

## 0:20-1:00 · Diapositiva 2 · Presentador A

**Objetivo:** hacer comprensible el problema a una persona no especializada.

**Decir:**

> Nuestra línea base demostró que una aplicación Windows podía abrir dentro de
> Winlator. Pero el usuario debía preparar el runtime, crear rutas, elegir
> gráficos, copiar archivos y lanzar el ejecutable. Además, el teléfono usa
> ARM64 y la aplicación puede usar x86-64; sus APIs y recursos tampoco siguen
> el modelo Android. Por eso el problema de investigación no es solo ejecutar:
> es integrar, distribuir y repetir el entorno con evidencia.

**No explicar:** cada ventana de la captura ni la historia completa de Winlator.

**Cambio:** al terminar “con evidencia”.

## 1:00-1:40 · Diapositiva 3 · Presentador A

**Objetivo:** definir la propuesta y reconocer la deuda documental formal.

**Decir:**

> La propuesta actual recibe una aplicación Windows ya preparada, junto con
> una configuración explícita. La CLI valida los archivos, decide cómo
> segmentarlos y produce un App Bundle, un conjunto de APK y reportes con
> hashes. Nuestro objetivo es reducir la configuración manual sin ocultar las
> condiciones de compatibilidad. La pregunta y la hipótesis formales todavía
> deben consolidarse en la documentación; por eso hoy defendemos el objetivo y
> los resultados observados, no una hipótesis presentada como concluida.

**No explicar:** sintaxis JSON ni comandos individuales.

**Cambio:** al terminar “concluida”.

## 1:40-2:20 · Diapositiva 4 · Presentador A

**Objetivo:** responder antes de que surja “¿por qué no usar Winlator?”.

**Decir:**

> Winlator y sus componentes aportan la capacidad base: el sistema Linux,
> Wine, Box64 y la ruta gráfica. Win2APK no pretende adjudicarse ese trabajo.
> Nuestra contribución está en transformar un proceso manual en una
> canalización: una CLI en Rust, identidad por aplicación, configuración Core,
> arranque directo, partición de payload, firma, limpieza, perfiles gráficos,
> interfaz adaptativa y medición. Dependemos de Winlator, pero resolvemos un
> problema distinto: cómo encapsular y validar una aplicación concreta.

**No explicar:** licencias ni comparación de forks; están en respaldo.

**Cambio y entrega de voz:** “Ahora B mostrará cómo se conectan esas piezas.”

## 2:20-3:15 · Diapositiva 5 · Presentador B

**Objetivo:** explicar la arquitectura sin mezclar construcción y ejecución.

**Acción:** la diapositiva inicia atenuada. Pulse una vez para revelar build
time y otra para revelar run time.

**Decir:**

> La arquitectura tiene dos momentos. Primero, en Linux x86-64, la CLI valida e
> inventaría, segmenta el payload, configura identidad y runtime, y genera
> artefactos firmados y reportes. [Avanzar]. Después, en Android ARM64, el
> paquete obtiene los recursos, prepara rootfs, contenedor y acceso directo.
> Box64 traduce el código x86-64 para el procesador ARM64. Wine implementa las
> interfaces de Windows sobre el entorno POSIX. Finalmente, DXVK o WineD3D y el
> driver llevan los gráficos a la GPU. [Avanzar]. Win2APK orquesta esta ruta;
> no reemplaza esas capas.

**No explicar:** Box86, VKD3D ni variantes Mali; responder si preguntan.

**Cambio:** avanzar después de “esas capas”.

## 3:15-3:55 · Diapositiva 6 · Presentador B

**Objetivo:** demostrar que existe un prototipo real y delimitar la medición.

**Decir:**

> Este es el estado actual observado en un Redmi Note 8 el 22 de septiembre.
> El paquete preinstalado inició la aplicación; el proceso del juego apareció a
> los 2,275 segundos y tanto la app como el juego permanecieron observables
> durante 120 segundos. A T+60 vimos la pantalla de título y el gamepad táctil.
> Esto valida esta instalación y este dispositivo. No valida una instalación
> fría ni compatibilidad universal.

**No explicar:** el FPS del menú. No es una medición de jugabilidad.

**Cambio:** avanzar mientras se dice “Ahora lo mostramos”.

## 3:55-4:40 · Diapositiva 7 · Presentador B

**Objetivo:** mostrar el prototipo sin convertir la demo en una operación larga.

### Ruta principal, máximo 30 segundos

1. Mostrar el Redmi Note 8 ya desbloqueado.
2. Tocar el icono de Bomb Rush Cyberfunk.
3. Mientras inicia, decir:

> El usuario abre un paquete con identidad propia. Winlator Core prepara el
> entorno sin mostrar su interfaz general y lanza el ejecutable configurado.

4. Cuando aparezca el título y el gamepad, decir:

> Aquí observamos la aplicación Windows y los controles táctiles integrados.
> Esta es la condición de salida de la demo.

5. Salir de la demo. No jugar ni entrar a menús.

### Contingencia inmediata

Si en 10 segundos no aparece una ruta conocida, no diagnosticar en vivo.
Decir:

> Para mantener el tiempo y las condiciones de la prueba, pasamos a la
> grabación local del mismo dispositivo y la misma instalación verificada.

Pulsar `V`. El video dura 18 segundos y funciona sin red. Al terminar, pulsar
`V` si no se detuvo y avanzar.

**No explicar:** ADB, resolución del video ni controles individuales.

## 4:40-5:20 · Diapositiva 8 · Presentador B

**Objetivo:** mostrar solidez metodológica sin leer una tabla grande.

**Decir:**

> El prototipo se evalúa con un protocolo reproducible. Cada run define estado
> esperado, artefacto y hash; mide con ADB; conserva captura T+60, procesos,
> métricas y logs; después separa observación, interpretación y decisión. Hay
> 75 ejecuciones documentadas de diferente alcance en cuatro dispositivos. Un
> caso exigente fue Cuphead: en EXEC-049 se entregaron 815 archivos y 5,847 GB.
> Esto demuestra distribución y preparación del payload; no demuestra que toda
> interacción del juego sea compatible.

**No explicar:** todas las métricas ni todas las ejecuciones.

**Cambio:** avanzar tras “compatible”.

## 5:20-5:55 · Diapositiva 9 · Presentador B

**Objetivo:** presentar el error CoreCLR como proceso de investigación.

**Decir:**

> El primer experimento .NET falló al inicializar el heap de CoreCLR. En vez de
> ocultarlo, conservamos el error, aislamos memoria, modo de publicación y GC,
> y cambiamos a una publicación self-contained con GC workstation no
> concurrente y un límite de heap. La ejecución posterior abrió Win2APKTest y
> respondió a interacción en Lenovo. Es una solución experimental para ese
> caso, no una garantía para cualquier aplicación .NET.

**No explicar:** todos los parámetros de GC.

**Cambio y entrega de voz:** “A cerrará con el estado real que esa metodología
nos obliga a reconocer.”

## 5:55-6:20 · Diapositiva 10 · Presentador A

**Objetivo:** mostrar honestidad sobre la variación actual.

**Decir:**

> La validación más reciente produjo dos resultados distintos. Redmi alcanzó
> el título y mantuvo los procesos durante 120 segundos. La instalación de
> Lenovo falló porque Play Core no encontró un pack de pruebas locales. El log
> localiza el fallo, pero todavía no distingue si proviene de datos residuales,
> una instalación incompleta o una variante. Por eso la demo usa Redmi y Lenovo
> queda como limitación reproducida, no como resultado descartado.

**No explicar:** intentar corregir la Lenovo durante la exposición.

## 6:20-6:35 · Diapositiva 11 · Presentador A

**Objetivo:** conectar objetivo, resultados e impacto sin inventar efectos.

**Decir:**

> El resultado coherente con el objetivo es técnico: ya automatizamos partes
> del empaquetado, distribución, arranque y validación. El potencial es reducir
> pasos especializados y facilitar la reutilización de software compatible.
> Aún no hemos medido adopción, ahorro económico ni impacto ambiental, así que
> no los presentamos como resultados.

**No explicar:** escenarios comerciales.

## 6:35-6:40 · Diapositiva 12 · Presentador A

**Objetivo:** cerrar con una respuesta, no con un resumen largo.

**Decir:**

> En síntesis, Win2APK ya es un sistema experimental que construye, distribuye,
> ejecuta y aprende de sus límites. Gracias. Escuchamos sus preguntas.

**Acción:** mantener la diapositiva. Si una pregunta requiere detalle, pulsar
`B` y navegar por respaldo.

## Control del tiempo

- Si a 4:00 aún no empieza la demo, usar directamente el video.
- Si a 5:30 sigue abierta la diapositiva 8, omitir la lectura del texto exacto
  de CoreCLR y resumir el caso en una frase.
- Si a 6:20 no se llegó a impacto, avanzar a la diapositiva 11, decir la frase
  de impacto observado frente a potencial y cerrar.
- Nunca superar 7:00 para “terminar una idea”.
