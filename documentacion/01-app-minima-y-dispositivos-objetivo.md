# 01. Aplicación mínima y dispositivos objetivo

- **Proyecto:** Win2APK
- **Tipo de documento:** definición del caso de prueba inicial
- **Estado:** aprobado para la primera prueba de viabilidad
- **Fecha:** 2026-08-07

## 1. Propósito

Definir la aplicación Windows de referencia y los dispositivos Android en los que se validará inicialmente el proceso de empaquetado automatizado de Win2APK.

Esta definición limita el primer experimento a un caso controlado. La ejecución exitosa de esta aplicación no implica compatibilidad universal con aplicaciones Windows.

## 2. Aplicación Windows de referencia

La aplicación mínima será una aplicación propia, portable y deliberadamente sencilla.

| Elemento | Definición |
|---|---|
| Nombre | Win2APK Test |
| Ejecutable principal | `Win2APKTest.exe` |
| Arquitectura inicial | Windows x64 |
| Forma de distribución | Carpeta portable, sin instalador |
| Dependencias iniciales | Mínimas y conocidas |
| Interfaz | Una ventana con un texto y un botón |

### Comportamiento esperado

1. Al iniciar, la ventana muestra el texto **“Hola mundo”**.
2. La ventana contiene un botón.
3. Al pulsar el botón, el texto cambia a **“Texto cambiado”**.
4. Al pulsar nuevamente el botón, el texto vuelve a **“Hola mundo”**.
5. El ciclo puede repetirse varias veces sin cerrar ni reiniciar la aplicación.

### Exclusiones de la primera versión

La aplicación no incluirá inicialmente:

- instalador;
- conexión de red;
- lectura o escritura de archivos;
- audio o video;
- base de datos;
- servicios de Windows;
- drivers;
- permisos de administrador;
- dependencias gráficas o de ejecución que no sean necesarias para la prueba.

La especificación detallada se encuentra en [`especificaciones/app-minima.md`](../especificaciones/app-minima.md).

## 3. Objetivo técnico de la prueba

La prueba debe comprobar el flujo mínimo completo:

```text
Win2APKTest.exe
        ↓
Preparación y empaquetado con Win2APK
        ↓
APK generado y firmado
        ↓
Instalación en Android
        ↓
Inicio directo de la aplicación Windows
```

El APK generado debe incorporar o preparar el entorno de compatibilidad requerido. El usuario final no debería tener que instalar Winlator por separado ni configurar manualmente un contenedor para ejecutar esta aplicación.

La arquitectura objetivo del APK será inicialmente `arm64-v8a`. La relación entre el ejecutable Windows x64 y la ejecución mediante el entorno de compatibilidad sobre Android ARM64 debe validarse experimentalmente.

## 4. Dispositivos físicos objetivo

Los datos fueron obtenidos mediante las propiedades reportadas por los dispositivos y `wm size`.

| Dispositivo | Android | API | ABI reportadas | Resolución reportada | Papel inicial |
|---|---:|---:|---|---:|---|
| Google Pixel 9a | 17 | 37 | `arm64-v8a` | 1080×2424 | Equipo Android moderno de comparación |
| Lenovo Tab P11, TB-J606F | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 1200×2000 | Validación en tableta y pantalla grande |
| Redmi Note 8 | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 1080×2340 | Dispositivo de referencia inicial con recursos limitados |
| Xiaomi Mi A3 | 16 | 36 | `arm64-v8a`, `armeabi-v7a`, `armeabi` | 720×1560 | Comparación en teléfono antiguo y pantalla de menor resolución |

La resolución corresponde al valor lógico reportado por el sistema mediante `wm size`; no representa necesariamente el tamaño físico de la pantalla en pulgadas.

## 5. Emuladores de Android Studio

Los emuladores se utilizarán como pruebas complementarias de:

- instalación del APK;
- inicio de la actividad;
- comportamiento básico de la interfaz;
- repetición de pruebas en una configuración controlada.

Un emulador con ABI `x86_64` no sustituye la evidencia obtenida en los dispositivos físicos ARM64. Su resultado deberá registrarse por separado. Si se utiliza un emulador ARM64, también se documentarán su API, ABI e imagen del sistema.

## 6. Criterios iniciales de aceptación

La prueba se considerará satisfactoria si:

- el APK se instala en los cuatro dispositivos físicos;
- el dispositivo no necesita tener Winlator instalado previamente;
- la aplicación puede abrirse desde el APK generado;
- aparece la ventana con **“Hola mundo”**;
- el botón cambia el texto a **“Texto cambiado”**;
- una segunda pulsación restaura **“Hola mundo”**;
- el comportamiento se repite sin cierre inesperado;
- se registran los resultados por dispositivo;
- se conservan evidencias de instalación, ejecución y errores.

Además de aprobar o fallar, se registrarán como mínimo:

- versión de Android y API;
- ABI;
- tiempo de instalación;
- tiempo del primer inicio;
- tiempo de inicios posteriores;
- tamaño del APK;
- resultado de cada interacción;
- mensajes de error y capturas de pantalla cuando corresponda.

## 7. Alcance de esta decisión

Esta aplicación constituye el primer caso de prueba de Win2APK y sirve para validar la viabilidad del flujo de empaquetado. Después de demostrar este caso, se podrá evaluar un conjunto limitado de aplicaciones adicionales, siempre que sus dependencias y condiciones de redistribución estén documentadas.
