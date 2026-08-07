# 00. Contexto general del proyecto Win2APK

- **Proyecto:** Win2APK
- **Tipo:** tesis de pregrado en Ingeniería de Sistemas
- **Producto:** aplicación de escritorio tipo builder para el empaquetado automatizado de aplicaciones Windows en paquetes APK para dispositivos Android
- **Duración prevista:** aproximadamente cuatro meses
- **Estado:** definición del alcance y validación inicial de viabilidad
- **Fecha de actualización:** 2026-08-07

Este documento establece el contexto base del proyecto. Los documentos posteriores pueden ampliar o corregir estas definiciones cuando existan resultados experimentales, decisiones de arquitectura o evidencias nuevas.

## 1. Resumen del proyecto

Win2APK propone diseñar e implementar una aplicación de escritorio orientada a desarrolladores. La aplicación recibirá como entrada una carpeta que contenga una aplicación Windows ya preparada para funcionar, incluyendo, según corresponda:

- archivo ejecutable;
- librerías;
- recursos;
- imágenes y demás assets;
- archivos de configuración;
- dependencias redistribuibles;
- estructura de carpetas necesaria para su ejecución.

El builder automatizará la preparación y el empaquetado de esa aplicación junto con un entorno de compatibilidad para generar un APK instalable en Android.

El usuario final debería poder instalar y abrir el APK sin instalar Winlator por separado, crear contenedores manualmente ni realizar la configuración técnica del entorno de compatibilidad. El resultado seguirá siendo una aplicación Windows ejecutada mediante una capa de compatibilidad; no será una aplicación Android nativa.

## 2. Problema central

Actualmente existen mecanismos para ejecutar aplicaciones Windows en dispositivos Android, pero normalmente exigen que el usuario final:

- instale una solución de compatibilidad;
- gestione manualmente los archivos de la aplicación;
- cree y configure un contenedor;
- seleccione versiones y controladores;
- ajuste variables, rutas o parámetros;
- resuelva dependencias y errores específicos de cada aplicación.

Este proceso dificulta la distribución de aplicaciones Windows existentes en Android, especialmente en casos de software legado, herramientas especializadas, aplicaciones empresariales o programas cuya reescritura completa para Android no sea viable.

El problema se refiere a la complejidad del proceso de preparación, configuración y distribución. No implica que actualmente sea imposible ejecutar aplicaciones Windows en Android.

## 3. Solución propuesta

La solución propuesta es una aplicación de escritorio tipo builder que traslade la complejidad técnica desde el usuario final hacia el desarrollador o encargado de preparar la distribución.

El flujo esperado es:

`@text
Desarrollador
    ↓
Prepara y valida la aplicación Windows
    ↓
Utiliza Win2APK
    ↓
Obtiene un APK configurado y firmado

Usuario final
    ↓
Instala el APK
    ↓
Abre la aplicación
`@

El builder deberá encargarse progresivamente de actividades como:

1. validar la carpeta de entrada;
2. localizar o confirmar el ejecutable principal;
3. registrar la configuración del caso;
4. incorporar la aplicación y sus recursos al proyecto Android;
5. preparar el entorno de compatibilidad;
6. personalizar los datos básicos del APK;
7. construir y firmar el paquete;
8. verificar la salida;
9. generar información del proceso y de los errores.

La implementación inicial se limitará a un flujo controlado. No se asumirá que todas las aplicaciones Windows pueden ser empaquetadas o ejecutadas correctamente.

## 4. Diferenciador

El proyecto no considera novedoso el hecho de ejecutar aplicaciones Windows en Android, porque esa capacidad ya existe mediante diferentes soluciones de compatibilidad.

El diferenciador de Win2APK es la automatización del empaquetado y la configuración previa:

> La complejidad que normalmente debe resolver el usuario final se incorpora al proceso de preparación realizado por el desarrollador.

Por tanto, el aporte principal estará en el flujo de validación, configuración, encapsulación y generación del APK, no en crear una nueva capa de compatibilidad desde cero.

## 5. Tipo y límites del producto

Win2APK debe describirse principalmente como:

> Aplicación de escritorio tipo builder para el empaquetado automatizado de aplicaciones Windows en paquetes APK para dispositivos Android.

No se define como:

- framework;
- SDK;
- plataforma;
- reemplazo de Winlator;
- conversor de código Windows a código Android;
- sistema de compatibilidad desarrollado desde cero.

Puede existir una interfaz de línea de comandos como componente interno para automatizar tareas, pero el producto principal será la aplicación de escritorio.

El alcance debe ser pequeño, verificable y realizable durante el periodo de la tesis. La demostración inicial se basará en una aplicación Windows propia y, posteriormente, en un conjunto limitado de aplicaciones adicionales si el tiempo, las dependencias y las licencias lo permiten.

## 6. Base tecnológica y supuestos que deben verificarse

Winlator y sus componentes pueden utilizarse como base tecnológica o referencia para el prototipo. En este proyecto se consideran tecnologías habilitadoras, no el aporte investigativo principal.

Antes de basar decisiones definitivas en ellos se debe verificar:

- la arquitectura interna de Winlator;
- la forma en que se crean y almacenan los contenedores;
- los recursos incluidos en el APK;
- la preparación del sistema de archivos;
- el arranque del ejecutable Windows;
- la posibilidad de iniciar directamente una aplicación preconfigurada;
- el proceso de compilación y generación del APK;
- las restricciones de almacenamiento y ejecución de Android;
- el comportamiento sobre dispositivos ARM64;
- el tamaño final del paquete;
- las licencias de Winlator y de cada componente redistribuido.

La arquitectura conceptual contempla un ejecutable Windows x64 ejecutado mediante un entorno de compatibilidad sobre dispositivos Android con ABI principal `arm64-v8a`. Esta relación debe validarse experimentalmente y no se considera garantizada únicamente por la arquitectura declarada.

La tecnología para la aplicación de escritorio todavía debe confirmarse durante la implementación. La opción inicialmente considerada es .NET 8 con WPF para Windows, acompañada de Gradle, Android SDK y un JDK para construir el APK. Estas tecnologías son decisiones de implementación sujetas a la viabilidad del repositorio base.

## 7. Aplicación Windows mínima de referencia

La primera prueba utilizará una aplicación propia, portable y controlada llamada **Win2APK Test**.

| Elemento | Definición |
|---|---|
| Nombre | Win2APK Test |
| Ejecutable | `Win2APKTest.exe` |
| Versión inicial | 0.1 |
| Arquitectura inicial | Windows x64 |
| Distribución | Carpeta portable, sin instalador |
| Interfaz | Una ventana, un texto y un botón |
| Dependencias | Mínimas, conocidas y documentadas |

### Comportamiento esperado

1. Al iniciar, muestra una ventana con el texto **“Hola mundo”**.
2. Incluye un botón visible e interactivo.
3. Al activar el botón, cambia el texto a **“Texto cambiado”**.
4. Al activarlo nuevamente, devuelve el texto a **“Hola mundo”**.
5. El ciclo puede repetirse sin reiniciar la aplicación.
6. La ventana puede cerrarse mediante los controles normales.

La aplicación no incluirá inicialmente instalador, red, persistencia, audio, video, base de datos, servicios, drivers, funciones específicas de Android ni permisos de administrador.

Su objetivo es proporcionar un caso reproducible para separar dos preguntas:

- **Compatibilidad:** si la aplicación puede ejecutarse mediante el entorno de compatibilidad.
- **Empaquetado:** si Win2APK puede reproducir automáticamente la configuración y generar un APK autónomo.

La especificación detallada se encuentra en [`../especificaciones/app-minima.md`](../especificaciones/app-minima.md).

## 8. Dispositivos físicos objetivo

La matriz inicial de pruebas físicas es la siguiente:

| Dispositivo | Android | API | ABI reportadas | Resolución reportada | Papel en la prueba |
|---|---:|---:|---|---:|---|
| Google Pixel 9a | 17 | 37 | `arm64-v8a` | 1080×2424 | Equipo Android moderno de comparación |
| Lenovo Tab P11, TB-J606F | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 1200×2000 | Validación en tableta y pantalla grande |
| Redmi Note 8 | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 1080×2340 | Dispositivo de referencia con recursos limitados |
| Xiaomi Mi A3 | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 720×1560 | Comparación en teléfono antiguo |

La arquitectura Android objetivo inicial será `arm64-v8a`. Las resoluciones corresponden a los valores lógicos reportados mediante `wm size`, no necesariamente al tamaño físico de las pantallas.

Los emuladores de Android Studio se utilizarán como pruebas complementarias para instalación, inicio y repetición de escenarios controlados. Un emulador `x86_64` no sustituye la evidencia obtenida en hardware ARM64 y sus resultados deben registrarse por separado.

## 9. Criterio técnico de éxito inicial

La primera prueba vertical será satisfactoria si:

- la aplicación Windows funciona en un entorno de referencia;
- Win2APK puede procesar la carpeta de entrada;
- se genera un APK instalable y firmado;
- el APK se instala en los dispositivos definidos;
- no es necesario instalar Winlator por separado;
- la aplicación se abre desde el APK generado;
- aparece “Hola mundo”;
- el botón cambia el texto a “Texto cambiado”;
- una segunda activación restaura “Hola mundo”;
- el ciclo se repite sin cierre inesperado;
- se registra el resultado en cada dispositivo;
- se conservan evidencias de instalación, ejecución y errores.

Se medirán, como mínimo:

- tiempo de construcción;
- tamaño del APK;
- tiempo de instalación;
- tiempo del primer inicio;
- tiempo de inicios posteriores;
- resultado de cada interacción;
- errores y cierres inesperados;
- diferencias entre dispositivos;
- configuración utilizada para producir el APK.

## 10. Enfoque de desarrollo y evaluación

El desarrollo comenzará con una prueba vertical pequeña:

1. compilar y ejecutar la aplicación mínima en Windows;
2. comprobar manualmente su ejecución mediante el entorno de compatibilidad;
3. registrar la configuración necesaria;
4. construir un APK independiente que inicie directamente la aplicación;
5. automatizar el proceso mediante el motor de Win2APK;
6. añadir la interfaz de escritorio;
7. probar el resultado en la matriz física y en emuladores;
8. consolidar las métricas y evidencias.

La línea base manual es importante porque permite diferenciar un problema de compatibilidad de un problema introducido por el empaquetador. La comparación inicial será entre:

- preparación y ejecución manual del entorno;
- preparación y generación automatizada mediante Win2APK.

El método de evaluación será experimental y aplicado, con casos de prueba controlados, matriz de dispositivos, criterios de aceptación y métricas reproducibles. La pregunta de investigación, la hipótesis y el conjunto final de aplicaciones adicionales se cerrarán después de confirmar la viabilidad técnica inicial.

## 11. Entregables académicos y cronograma

El trabajo técnico y académico debe terminar a más tardar el **31 de octubre de 2026**. Desde el **1 hasta el 16 de noviembre** se reservará el tiempo para ensayos, correcciones menores y preparación de la sustentación. La presentación final está prevista para el **17 de noviembre de 2026**.

Las fechas oficiales de presentación de avances son:

- 11 de agosto;
- 20 de agosto;
- 3 de septiembre;
- 17 de septiembre;
- 13 de octubre;
- 27 de octubre.

Cada entrega debe mostrar simultáneamente:

- avance del texto de tesis o artículo;
- avance funcional o verificable del programa;
- evidencias del trabajo realizado;
- problemas encontrados y correcciones aplicadas.

Para conservar tiempo de contingencia, se utilizarán cierres internos anteriores a las fechas oficiales:

| Entrega o hito | Cierre interno | Reserva principal |
|---|---:|---:|
| Entrega del 11 de agosto | 9 de agosto | 10 de agosto |
| Entrega del 20 de agosto | 17 de agosto | 18–19 de agosto |
| Entrega del 3 de septiembre | 29 de agosto | 30 de agosto–2 de septiembre |
| Entrega del 17 de septiembre | 13 de septiembre | 14–16 de septiembre |
| Entrega del 13 de octubre | 8 de octubre | 9–12 de octubre |
| Entrega del 27 de octubre | 22 de octubre | 23–26 de octubre |
| Cierre técnico y académico | 27 de octubre | 28–30 de octubre |
| Material para sustentación | 12 de noviembre | 13–16 de noviembre |

Durante las reservas no se deben agregar funcionalidades nuevas salvo que sean indispensables. El objetivo es corregir, recompilar, repetir pruebas, organizar evidencias y reducir justificadamente el alcance si aparece un bloqueo crítico.

## 12. Hitos técnicos de referencia

La ruta crítica provisional contempla:

- **29 de agosto:** APK autónomo de la aplicación mínima;
- **13 de septiembre:** motor automatizado de empaquetado;
- **8 de octubre:** MVP con pruebas iniciales;
- **22 de octubre:** prototipo funcional congelado;
- **27 de octubre:** cierre de nuevas funcionalidades;
- **31 de octubre:** cierre total del texto, prototipo, pruebas y documentación;
- **1–16 de noviembre:** ensayos y preparación de sustentación;
- **17 de noviembre:** presentación final.

Estos hitos son objetivos de planificación. Su cumplimiento debe respaldarse con evidencias técnicas y académicas, no solamente con la existencia de archivos en el repositorio.

## 13. Exclusiones y restricciones

El proyecto no busca:

- convertir el código Windows en código Android nativo;
- prometer compatibilidad universal;
- reemplazar Winlator;
- desarrollar una capa de compatibilidad desde cero;
- soportar cualquier aplicación Windows existente;
- incorporar inteligencia artificial sin una necesidad técnica real;
- publicar inicialmente en tiendas de aplicaciones;
- resolver automáticamente todas las dependencias de cualquier aplicación;
- agregar nube, microservicios, blockchain u otras tecnologías que no aporten al problema;
- llamar al resultado una aplicación Android nativa.

La expresión “convertir EXE a APK” puede utilizarse de manera informal para explicar la idea, pero la terminología académica preferida es:

- empaquetado;
- encapsulación;
- distribución;
- aplicación Windows preparada;
- entorno de compatibilidad;
- generación de APK.

## 14. Riesgos que deben controlarse

Los principales riesgos iniciales son:

1. **Compatibilidad:** la aplicación de referencia podría no funcionar con la configuración elegida.
2. **Arquitectura:** el ejecutable Windows x64 y el dispositivo Android ARM64 requieren una combinación de componentes compatible.
3. **Empaquetado:** el entorno podría depender de archivos o rutas que no puedan incorporarse directamente al APK.
4. **Android:** pueden existir restricciones de almacenamiento, permisos, ejecución, instalación o tamaño.
5. **Rendimiento:** el primer inicio y la preparación del entorno podrían ser demasiado lentos.
6. **Tamaño:** el entorno de compatibilidad puede producir APK grandes.
7. **Licencias:** Winlator y sus componentes pueden tener obligaciones diferentes de redistribución.
8. **Dispositivos:** una configuración que funcione en un equipo puede fallar en otro por diferencias de GPU, sistema o firmware.
9. **Tiempo:** una dificultad temprana puede consumir el margen destinado a las entregas.

Las puertas de decisión del proyecto deben detener o reducir el alcance cuando una de estas condiciones impida demostrar el flujo mínimo.

## 15. Licencias y redistribución

No se asumirá que todos los componentes de Winlator pueden redistribuirse bajo una única licencia. Se debe elaborar un inventario que identifique, como mínimo:

- componente;
- versión;
- repositorio de origen;
- licencia;
- obligaciones de redistribución;
- avisos requeridos;
- código fuente que deba acompañar la distribución;
- compatibilidad con el uso dentro de un APK generado.

La redistribución de un APK basado en estos componentes solo se considerará después de revisar individualmente las licencias y las condiciones aplicables.

## 16. Estructura documental del repositorio

La documentación inicial se organiza así:

`@text
documentacion/
├── index.md
├── 00-contexto-del-proyecto.md
└── 01-app-minima-y-dispositivos-objetivo.md

especificaciones/
└── app-minima.md
`@

El paso `00` funciona como referencia general. El paso `01` registra la decisión del caso de prueba y los dispositivos. La carpeta `especificaciones/` contiene requisitos más detallados que deben utilizarse durante la construcción y las pruebas.

## 17. Decisiones aún abiertas

Después de este documento todavía deben cerrarse mediante investigación o experimentación:

- versión exacta de Winlator o de los componentes reutilizados;
- método para iniciar directamente el ejecutable dentro del APK;
- estructura final del proyecto Android plantilla;
- configuración mínima del contenedor;
- herramienta de compilación de la aplicación Windows;
- herramienta definitiva para la interfaz de escritorio;
- emuladores y sus ABI;
- inventario completo de licencias;
- lista final de aplicaciones adicionales;
- métricas definitivas del experimento;
- pregunta de investigación e hipótesis;
- estrategia de firma y manejo del `keystore`.

Estas decisiones no deben resolverse por suposiciones. Cada una debe quedar respaldada por una prueba, una fuente oficial, una decisión técnica justificada o una delimitación explícita del alcance.
