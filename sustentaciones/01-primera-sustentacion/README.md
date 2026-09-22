# Primera sustentación oficial de Win2APK

Material autocontenido para la exposición del 29 de septiembre de 2026. La
presentación principal dura aproximadamente 6:40; las diapositivas posteriores
al cierre son material de respaldo para preguntas.

## Inicio rápido

### Linux

Desde esta carpeta:

```bash
chmod +x presentar.sh
./presentar.sh
```

El script inicia un servidor local en `http://127.0.0.1:8765/` y trata de abrir
el navegador. Para detenerlo, vuelva a la terminal y pulse `Ctrl+C`.

### Windows

Haga doble clic en `presentar.bat`. Requiere Python disponible como `py` o
`python`. También se puede abrir `index.html` directamente, pero el servidor
local ofrece un comportamiento más uniforme para el video.

### Apertura manual

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Después abra `http://127.0.0.1:8765/`.

## Controles

| Acción | Tecla |
|---|---|
| Siguiente paso o diapositiva | `→`, `Espacio`, `Enter`, `Page Down` |
| Paso o diapositiva anterior | `←`, `Backspace`, `Page Up` |
| Primera / última | `Home` / `End` |
| Ir al inicio de Backup / Preguntas | `B` |
| Reproducir o pausar el video de demo | `V` |
| Pantalla completa | `F` |
| Vista general | `O` |

La arquitectura tiene dos revelados. Avance una vez para mostrar la fase de
construcción y otra para mostrar la fase de ejecución.

## Demo

- Dispositivo principal: Redmi Note 8 con
  `com.win2apk.bombrushcyberfunk` ya instalado.
- Estado esperado: pantalla de título de Bomb Rush Cyberfunk con el gamepad
  táctil visible.
- Respaldo local: `assets/video/demo-redmi-bomb-rush-18s.mp4`.
- En la diapositiva Demo, pulse `V` para reproducir o pausar.
- No use la Lenovo TB-J606F como ruta principal: `EXEC-074` reprodujo un fallo
  por un pack de pruebas locales ausente.

El protocolo completo está en [docs/guion.md](docs/guion.md).

## PDF

El respaldo generado está en `presentacion-win2apk.pdf`. Para regenerarlo:

```bash
./scripts/exportar-pdf.sh
```

El script usa Google Chrome o Chromium en modo headless y abre la variante de
impresión `index.html?print=1`. Cada diapositiva se exporta como una página
16:9. No se requiere Internet.

## Actualizar evidencia

1. No sobrescriba una ejecución histórica.
2. Cree una nueva ejecución con la skill de medición del proyecto.
3. Copie solo la evidencia seleccionada a `assets/images/` o `assets/video/`.
4. Añada la ruta de origen, el run, la fecha y el alcance en
   [docs/fuentes.md](docs/fuentes.md).
5. Vuelva a ejecutar las pruebas con `./scripts/verificar.sh` y regenere el
   PDF.

## Dependencias

- Presentación: navegador moderno; HTML, CSS y JavaScript locales.
- Servidor: Python 3.
- PDF y pruebas: Google Chrome o Chromium.
- Video: H.264 dentro de MP4, sin audio.

No hay CDN, telemetría, llamadas de red ni fuentes remotas.

## Documentos de preparación

- [Guion de 7 minutos](docs/guion.md)
- [Preguntas y respuestas](docs/preguntas-y-respuestas.md)
- [Auditoría del proyecto](docs/auditoria-proyecto.md)
- [Estructura de la presentación](docs/estructura-presentacion.md)
- [Fuentes y trazabilidad](docs/fuentes.md)
- [Revisión contra la rúbrica](docs/revision-rubrica.md)
- [Decisiones de diseño](docs/diseno.md)

## Evidencia de calidad

La carpeta `qa/` conserva capturas automatizadas y reportes de verificación.
Estos archivos sirven para revisar el material, no se muestran durante la
exposición.
