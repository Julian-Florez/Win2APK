# Esquema de datos de ejecución

## Organización

Cada experimento tiene una carpeta inmutable `metricas/runs/RUN-YYYYMMDD-NNN/`. Los
catálogos de `metricas/catalogo/` permiten analizar todos los experimentos sin
recorrer manualmente cada carpeta.

```text
metricas/
├── catalogo/
│   ├── runs.csv
│   ├── devices.csv
│   └── resultados.csv
└── runs/RUN-YYYYMMDD-NNN/
    ├── run.csv
    ├── dispositivos.csv
    ├── instalaciones.csv
    ├── muestras.csv
    ├── eventos.csv
    ├── capturas.csv
    ├── resumen.csv
    ├── screenshots/<device_id>/t060.png
    └── logs/<device_id>/
```

La misma ejecución se registra en `ejecuciones/NN-metricas-.../matriz.md`, que
enlaza la carpeta de métricas y las evidencias originales.

## Identificadores

- `run_id`: identificador técnico e inmutable, por ejemplo `RUN-20260918-001`.
- `exec_id`: identificador documental, por ejemplo `EXEC-032`.
- `device_id`: alias legible y estable; no se guarda el serial ADB sin procesar.
- `sample_index`: contador desde cero dentro de cada par `run_id/device_id`.
- `elapsed_ms`: reloj monótono desde el lanzamiento de la aplicación.

## Valores ausentes

Las columnas numéricas no disponibles quedan vacías para conservar su tipo al
importarlas en pandas, R o una hoja de cálculo. `metric_status`, `fps_source` y
los eventos explican la ausencia; en la matriz Markdown el valor equivalente es
`N/R`. `N/A` se reserva para una métrica que no aplica al escenario.

## Tiempo y unidades

- Fechas: UTC en ISO 8601.
- Duraciones: segundos o milisegundos según el sufijo de la columna.
- Memoria y almacenamiento: KiB.
- Frecuencias: Hz o kHz según el sufijo.
- Temperaturas: grados Celsius.
- Porcentajes: rango 0–100; la CPU de proceso representa fracción de la capacidad
  total del dispositivo, no porcentaje de un único núcleo.

`delivery_to_first_frame_seconds` comienza inmediatamente antes de invocar
`bundletool install-apks` y termina cuando, con el proceso del juego presente,
SurfaceFlinger expone el primer timestamp de presentación de su superficie. Incluye
preparación de bundletool, transferencia, instalación, inicialización del payload y
arranque; si no hay timestamps verificables se registra como N/R.

## Alcance de FPS y GPU

`fps_presented` solo se completa cuando SurfaceFlinger expone timestamps de la
superficie correspondiente. No se sustituye por `gfxinfo`, porque ese valor puede
medir la interfaz Android y no los fotogramas del juego. GPU se obtiene únicamente
de nodos legibles sin root; si el fabricante no los expone, queda sin valor y se
registra la causa.
