# Automatización del icono de launcher

- **Fecha:** 2026-09-19
- **Estado:** implementada y verificada en el build debug
- **Propósito:** permitir que cada empaquetado use una imagen suministrada por
  el usuario como icono de la aplicación generada.

## Comportamiento del empaquetador

El nombre de la carpeta sigue determinando la identidad de la aplicación cuando
`deriveApplicationIdFromFolder` está habilitado. Con `folderName: "Cuphead"`,
la normalización actual produce `com.cuphead`. El icono es una configuración
independiente: no cambia el `applicationId`, el rootfs ni el ejecutable.

La ruta puede definirse de dos formas:

1. En `config/win2apk.json`, mediante `android.iconPath` y opcionalmente
   `android.iconBackgroundColor`.
2. Como override por build, sin editar la configuración:

   ```bash
   cd winlator/app
   bash gradlew :app:assembleDebug \
     -Pwin2apkIcon="/ruta/al/icono.svg" \
     --no-daemon --console=plain
   ```

Se aceptan imágenes rasterizadas y formatos vectoriales que pueda leer
ImageMagick; los SVG se rasterizan con Inkscape cuando está disponible y se usa
ImageMagick como fallback. Si la ruta no existe, el build falla con un mensaje
explícito.

## Recursos generados

`tools/generate_android_icon.py` escribe recursos en
`winlator/app/app/build/generated/launcher-icon-res`, no sobreescribe los
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

- `:app:assembleDebug`: aprobado.
- El APK contiene `win2apk_launcher.xml`, sus PNG por densidad y las capas
  `foreground`/`monochrome`.
- El manifest fusionado declara `@mipmap/win2apk_launcher` y
  `@mipmap/win2apk_launcher_round`.
- `aapt2 dump badging` confirmó `package: name='com.cuphead'` y que la
  compilación sigue usando `versionCode=48` y `targetSdkVersion=28`.
- El task de preparación también fue probado con una imagen SVG suministrada
  mediante `-Pwin2apkIcon`.

## Pendientes

El recurso de Cuphead es un ejemplo de tesis y no una autorización general para
publicar la marca. El empaquetador no descarga imágenes automáticamente desde
Internet: recibe una ruta local, lo que mantiene el build reproducible y evita
que una fuente externa cambie el resultado sin registro.
