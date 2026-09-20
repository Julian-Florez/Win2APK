# Win2APK

📖 **[Abrir el manual HTML en GitHub Pages](https://julian-florez.github.io/Win2APK/)**

**Win2APK** es un proyecto de investigación y desarrollo orientado a facilitar la distribución de aplicaciones desarrolladas para Windows en dispositivos Android.

El proyecto propone un **CLI de empaquetado** capaz de recibir una aplicación Windows previamente preparada —incluyendo su ejecutable, librerías, recursos y dependencias— y generar un AAB y un APK set que incorporen un entorno de compatibilidad configurado para su ejecución en Android.

## Objetivo

Reducir la complejidad asociada con la configuración y distribución de aplicaciones Windows en Android, trasladando gran parte de este proceso desde el usuario final hacia el desarrollador.

El flujo esperado es:

```text
Aplicación Windows
        ↓
     Win2APK
        ↓
Configuración y empaquetado
        ↓
       APK
        ↓
      Android
```

El usuario final debería poder instalar y ejecutar el APK generado sin tener que configurar manualmente herramientas de compatibilidad.

## CLI Linux

La configuración completa vive en un JSON con esquema v2. El ejemplo actual es
[`config/win2apk.json`](config/win2apk.json); Cuphead sólo es el caso de prueba,
no una condición del empaquetador.

```bash
cargo build --release --package win2apk
./target/release/win2apk setup
./target/release/win2apk doctor --engine /ruta/al/winlator/app
./target/release/win2apk validate config/win2apk.json
./target/release/win2apk plan config/win2apk.json
./target/release/win2apk build config/win2apk.json --engine /ruta/al/winlator/app
./target/release/win2apk install config/dist/cuphead-<version>.apks --device SERIAL
```

`setup` instala el JDK, Android SDK/NDK/CMake, platform-tools y bundletool en
los directorios XDG del usuario; muestra la aceptación de licencias de Android.
El motor Winlator se mantiene en su repositorio separado y se indica con
`--engine` o `WIN2APK_ENGINE_DIR`. Después de compilar el binario release, el
usuario final no necesita Rust. El contrato completo está en la
[`especificación del CLI`](especificaciones/cli-empaquetado.md).

## Icono personalizado

El campo obligatorio `android.icon` acepta una imagen rasterizada o SVG. El CLI
genera internamente el icono adaptativo, la capa monocromática y los PNG de
compatibilidad, sin depender de Python, ImageMagick o Inkscape:

```json
"android": {
  "icon": "../assets/icono.svg",
  "iconBackgroundColor": "#202124"
}
```

La implementación y sus lineamientos están documentados en
[`11-automatizacion-iconos-launcher`](documentacion/11-automatizacion-iconos-launcher.md).

## Alcance

Win2APK se encuentra actualmente en fase de investigación y prototipado.

El proyecto **no busca convertir aplicaciones Windows en aplicaciones Android nativas** ni garantizar compatibilidad con cualquier software de Windows. Su propósito es explorar y validar un mecanismo automatizado de empaquetado y distribución utilizando tecnologías de compatibilidad existentes.

## Tecnologías

El prototipo estudiará la integración y reutilización de componentes de proyectos de código abierto como **Winlator** y las tecnologías que conforman su entorno de ejecución.

## Estado

🚧 **En desarrollo — Proyecto de tesis de Ingeniería de Sistemas**

Actualmente se trabaja en:

* Análisis de la arquitectura de Winlator.
* Definición del proceso de generación de APK.
* Evaluación de licencias y dependencias.
* Desarrollo del primer prototipo funcional.

## Licencia

La licencia definitiva de Win2APK aún está por definirse. Los componentes de terceros utilizados mantienen sus respectivas licencias.
