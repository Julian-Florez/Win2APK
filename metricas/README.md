# Métricas experimentales de Win2APK

Esta carpeta contiene datos tabulares producidos por
`$win2apk-medir-dispositivos`. Cada subcarpeta de `runs/` corresponde a una
ejecución histórica; los archivos de `catalogo/` reúnen sus metadatos y resultados
para análisis conjunto.

- `catalogo/runs.csv`: una fila por ejecución.
- `catalogo/devices.csv`: inventario técnico actualizado por alias de dispositivo.
- `catalogo/resultados.csv`: una fila resumida por ejecución y dispositivo.
- `runs/RUN-YYYYMMDD-NNN/`: muestras, instalación, eventos, capturas, logs y resumen.

Las columnas numéricas no disponibles quedan vacías para conservar el tipo de
dato. La causa se registra en columnas de estado o eventos; la documentación
Markdown usa `N/R`. Los seriales ADB sin procesar no se almacenan.

Consulte
[`esquema-datos.md`](../.codex/skills/win2apk-medir-dispositivos/references/esquema-datos.md)
para las unidades y contratos completos.

