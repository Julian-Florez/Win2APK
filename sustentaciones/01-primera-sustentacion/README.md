# Presentación vigente de Win2APK

La versión vigente es [presentacion-vigente.html](presentacion-vigente.html):
10 diapositivas creadas a partir del guion compartido en esta conversación. El
deck de 12 diapositivas y su PDF anterior fueron retirados.

## Abrir la presentación

En Linux, ejecuta `./presentar.sh`. Se inicia un servidor local y se abre la
presentación en el navegador. En Windows, abre `presentar.bat`.

También puedes abrir `presentacion-vigente.html` directamente. El video de la
demostración y las imágenes de evidencia se cargan desde `assets/`.

## Controles

| Acción | Tecla |
|---|---|
| Diapositiva siguiente | `→`, `Espacio`, `Enter`, `Page Down` |
| Diapositiva anterior | `←`, `Backspace`, `Page Up` |
| Primera / última diapositiva | `Home` / `End` |
| Pantalla completa | `F` |
| Reproducir o pausar la demo | `V` |

La tipografía Google Sans Flex se carga desde Google Fonts, por lo que requiere
conexión a Internet. Las imágenes y el video son locales.

## Exportar a PDF

No se incluye un PDF desactualizado. Si necesitas exportar esta versión,
ejecuta `./scripts/exportar-pdf.sh`; el script renderiza las 10 diapositivas de
`presentacion-vigente.html` y crea `presentacion-vigente.pdf`.
