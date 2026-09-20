# Automatización del icono de launcher

- **Fecha:** 2026-09-19
- **Estado:** implementada y verificada en el build debug
- **Propósito:** permitir que cada empaquetado use una imagen suministrada por
  el usuario como icono de la aplicación generada.

## Comportamiento del empaquetador

El CLI recibe la ruta del icono en el campo obligatorio `android.icon`. El
icono es una configuración independiente: no cambia el `applicationId`, el
rootfs ni el ejecutable. Las rutas relativas se resuelven respecto al JSON.

```json
{
  "android": {
    "applicationId": "org.ejemplo.app",
    "versionCode": 1,
    "versionName": "1.0.0",
    "icon": "../assets/icono.svg",
    "iconBackgroundColor": "#202124"
  }
}
```

El build se ejecuta con `win2apk build CONFIG`. Se aceptan PNG, JPEG, WebP y
SVG; la implementación Rust del CLI decodifica o rasteriza el recurso dentro
del staging. Si la ruta no existe o el formato no se puede leer, el build
termina con un mensaje explícito. No se requiere Python, ImageMagick ni
Inkscape en el computador que empaqueta.

## Recursos generados

`cli/src/icon.rs` escribe recursos en el staging del build, no sobreescribe los
recursos fuente ni modifica la imagen original. Produce:

- icono adaptativo de color con foreground y background;
- capa `monochrome` para iconos temáticos de Android moderno;
- `mipmap-*` PNG para compatibilidad con dispositivos anteriores a API 26;
- variantes normal y redonda, declaradas mediante `android:icon` y
  `android:roundIcon`.

La composición usa un lienzo de 108×108 dp y limita el contenido a la zona
segura central de 66×66 dp. Estas dimensiones, la separación foreground/background
y la capa monocromática siguen las recomendaciones de
[Adaptive icons de Android](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive)
y de [iconos temáticos de Android](https://developer.android.com/distribute/aep/aep-req-theme-app-icons).

## Ejemplo Cuphead

El ejemplo del repositorio usa `assets/icons/cuphead-promo-logo.png`, descargado
desde [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cuphead_promo_logo_ddwtd.png).
La fuente identifica a Studio MDHR como autor y advierte que pueden existir
restricciones de marca, aunque la página clasifica el texto/logo como dominio
público por umbral de originalidad. La procedencia, hash y advertencia legal
están en [assets/icons/README.md](../assets/icons/README.md). Para distribuir
otra aplicación se debe reemplazar el recurso por una imagen propia o
debidamente autorizada.

## Verificación realizada

- `win2apk build config/example.testapp.json`: aprobado.
- El AAB de prueba contiene únicamente `win2apk_payload_001`, sin heredar los
  asset packs de una compilación anterior de Cuphead.
- El APK contiene `win2apk_launcher.xml`, sus PNG por densidad y las capas
  `foreground`/`monochrome`.
- El manifest generado declara `@mipmap/win2apk_launcher` y
  `@mipmap/win2apk_launcher_round`.
- La compilación de Cuphead también fue probada con una imagen PNG y generó el
  AAB/APKS completo.

## Pendientes

El recurso de Cuphead es un ejemplo de tesis y no una autorización general para
publicar la marca. El empaquetador no descarga imágenes automáticamente desde
Internet: recibe una ruta local, lo que mantiene el build reproducible y evita
que una fuente externa cambie el resultado sin registro.
