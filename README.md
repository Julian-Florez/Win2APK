# Win2APK

**Win2APK** es un proyecto de investigación y desarrollo orientado a facilitar la distribución de aplicaciones desarrolladas para Windows en dispositivos Android.

El proyecto propone una aplicación de escritorio tipo **builder** capaz de recibir una aplicación Windows previamente preparada —incluyendo su ejecutable, librerías, recursos y dependencias— y generar un paquete APK que incorpore un entorno de compatibilidad previamente configurado para su ejecución en Android.

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

## Icono personalizado

El empaquetador acepta una ruta local de imagen o SVG mediante la propiedad
`win2apkIcon`. También puede configurarse `android.iconPath` en
`config/win2apk.json`. El build genera automáticamente el icono adaptativo,
la capa monocromática y los PNG de compatibilidad:

```bash
cd winlator/app
bash gradlew :app:assembleDebug \
  -Pwin2apkIcon="/ruta/al/icono.svg" \
  --no-daemon --console=plain
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
