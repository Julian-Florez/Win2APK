---
name: win2apk-medir-dispositivos
description: >-
  Registra pruebas reales de Win2APK en uno o varios dispositivos Android
  mediante ADB. Úsala siempre que se instale, inicie, compare, depure o mida una
  compilación en Pixel 9a, Redmi Note 8, Xiaomi Mi A3, Lenovo TB-J606F u otro
  dispositivo; crea un run reproducible, inventaría hardware y sistema, mide
  instalación, CPU, RAM, GPU, FPS, temperatura y almacenamiento, captura la
  pantalla en T+60, clasifica visualmente su estado y consolida CSV, logs,
  capturas y la matriz documental de la ejecución.
---

# Medir dispositivos Win2APK

## Objetivo

Crear evidencia experimental comparable sin depender de observación manual
continua. Tratar cada run como inmutable y no convertir el resultado de un
dispositivo en una afirmación universal.

## Antes de medir

1. Leer `AGENTS.md` y `ejecuciones/AGENTS.md` del repositorio.
2. Si la prueba puede borrar una instalación, confirmar que el usuario autorizó
   explícitamente la desinstalación y pérdida de datos de la aplicación.
3. Verificar `adb devices -l`, que los alias sean únicos y que cada transporte
   esté en estado `device`. No persistir seriales ADB; los CSV guardan un hash.
4. Identificar el artefacto exacto y calcular su SHA-256. Para AAB con asset packs,
   generar una colección APKS completa con `scripts/build_apks.py`.
5. Definir el escenario sin anticipar el resultado: descripción, estado esperado,
   duración, intervalo y segundo de captura.

Usar `title_screen`, `gameplay`, `loading`, etc. como `expected_state` cuando el
estado esperado corresponda a la taxonomía visual.

## Elegir el flujo

### Instalación fría y medición

Usar `scripts/run_experiment.py`. El orquestador crea el run, inventaría todos los
dispositivos y procesa cada dispositivo de forma secuencial: desinstalación,
instalación completa con bundletool, lanzamiento y monitoreo. Exigir literalmente
`--confirm-delete-all ELIMINAR-COMPLETO`; no omitir esta barrera.

```bash
python3 .codex/skills/win2apk-medir-dispositivos/scripts/run_experiment.py \
  --repo "$PWD" \
  --apks /ruta/publicacion.apks \
  --bundletool tools/bundletool-all-1.18.3.jar \
  --device pixel-9a=SERIAL_ADB \
  --scenario titulo-5-min \
  --description "Primer inicio observado durante cinco minutos" \
  --expected-state title_screen \
  --duration 300 --interval 1 --screenshot-second 60 \
  --confirm-delete-all ELIMINAR-COMPLETO
```

No escribir el comando completo con seriales en logs versionados.

### Medición sin reinstalar

Ejecutar `create_run.py`, `inventory_devices.py` y `monitor_device.py` por separado.
Usar `--no-launch` solo si la aplicación ya está en el estado que debe observarse.
Registrar en `install_mode` que no se midió una instalación; no fabricar un tiempo.

### Construcción de APKS

`build_apks.py` recibe contraseñas únicamente mediante variables de entorno y usa
archivos temporales con permisos restringidos. No guardar keystores ni contraseñas
en el repositorio. La ruta APKS usada al crear el run debe ser la misma que instala
`cold_install.py`, y el hash debe coincidir.

## Durante la medición

- Mantener la pantalla encendida y el dispositivo conectado; no navegar para
  forzar el estado esperado.
- La captura canónica ocurre en T+60 mediante un hilo independiente del muestreo.
- Medir sin root. Dejar numéricos ausentes vacíos y explicar la causa en
  `metric_status` o `eventos.csv`; en Markdown representar lo ausente como `N/R`.
- Considerar `fps_presented` válido solo con `fps_source=surfaceflinger_latency`.
- Calcular `delivery_to_first_frame_seconds` desde el inicio de
  `bundletool install-apks` hasta `first_game_frame_observed`; no sustituirlo por
  el tiempo de aparición del proceso.
- GPU puede quedar N/R cuando el fabricante no expone contadores legibles.
- Conservar mensajes de error exactos en los logs. Si aparece un fallo nuevo,
  después del run leer `limitaciones/AGENTS.md` y `bitacora/AGENTS.md`, registrar
  la limitación y enlazarla con la ejecución.

Consultar [esquema-datos.md](references/esquema-datos.md) para las unidades y la
estructura de carpetas.

## Clasificar la captura T+60

El programa captura la pantalla, pero la clasificación semántica la realiza el
agente con capacidad visual; los scripts no requieren una API ni almacenan claves.

Por cada dispositivo:

1. Abrir el PNG original indicado en `capturas.csv` con la herramienta visual.
2. Describir primero lo literalmente visible y después escoger la clase que mejor
   lo representa según [clasificacion-pantallas.md](references/clasificacion-pantallas.md).
3. Ejecutar `classify_screenshot.py` con una primaria, secundaria opcional,
   descripción, texto visible, confianza cualitativa y nombre real del modelo.
4. No inferir un crash solo por una pantalla negra; contrastar procesos, eventos y
   `exit-info.txt`.

Ejemplo:

```bash
python3 .codex/skills/win2apk-medir-dispositivos/scripts/classify_screenshot.py \
  --run-dir metricas/runs/RUN-YYYYMMDD-NNN \
  --device-id pixel-9a \
  --primary title_screen \
  --description "Se observa el título y la invitación para comenzar" \
  --visible-text "PRESS ANY BUTTON" \
  --confidence high \
  --model N/R
```

No usar `confirmed` salvo revisión humana explícita; una clasificación inicial de
IA queda `unreviewed`.

## Cerrar el run

1. Ejecutar `summarize_run.py` después de clasificar todas las capturas.
2. Ejecutar `validate_dataset.py` sin `--allow-pending-classification`.
3. Revisar `resumen.csv`, `eventos.csv`, la matriz y los logs antes de redactar una
   conclusión. Separar observación, interpretación y decisión.
4. Comprobar que `ejecuciones/index.md` contiene el `EXEC-NNN` y que sus enlaces
   relativos funcionan.
5. No modificar retrospectivamente un run para representar una nueva prueba;
   crear otro run.

## Scripts

- `build_apks.py`: genera una colección APKS de prueba local sin persistir secretos.
- `create_run.py`: reserva IDs y crea los CSV, directorios y matriz inicial.
- `inventory_devices.py`: extrae identidad técnica estable y capacidades sin guardar el serial ADB.
- `cold_install.py`: desinstala, verifica el borrado e instala con bundletool midiendo tiempos reales.
- `monitor_device.py`: lanza y muestrea el sistema durante el periodo definido, incluida la captura T+60.
- `classify_screenshot.py`: valida y guarda la descripción y las clases producidas por visión.
- `summarize_run.py`: calcula agregados, actualiza catálogos y reconstruye la matriz documental.
- `validate_dataset.py`: detecta esquemas rotos, huecos temporales, duplicados y evidencias faltantes.
- `run_experiment.py`: coordina de principio a fin la instalación y medición secuencial de varios dispositivos.
- `common.py`: concentra esquemas CSV y utilidades compartidas para evitar divergencias.
