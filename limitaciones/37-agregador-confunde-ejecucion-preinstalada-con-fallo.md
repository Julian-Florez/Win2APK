# 37. El agregador confunde una ejecución preinstalada con un fallo de instalación

## Descripción

La síntesis automática de métricas marcó `failed_install` en una ejecución que
declaraba `install_mode=preinstalled-no-reinstall` y que abrió correctamente la
aplicación. En ese modo no existe una fila de instalación porque instalar no
forma parte del experimento.

## Contexto técnico

- Fecha: 2026-09-20.
- Ejecución: [EXEC-050](../ejecuciones/50-metricas-ui-base-nocore-redmi-horizontal-20260920/matriz.md).
- Run: `RUN-20260920-001`.
- Dispositivo: Xiaomi Redmi Note 8, Android 16/API 36, `arm64-v8a`.
- Paquete: `com.winlator`, versión `11.1-core`, preinstalado.
- Método: `preinstalled-no-reinstall`, sin root.

## Reproducción o evidencia

El monitor registró la aplicación visible a 1227 ms y conservó 36 muestras. La
captura T+60 muestra Win2APKTest dentro del entorno de compatibilidad. Sin
embargo, `resumen.csv` y los catálogos produjeron exactamente:

```text
failed_install
```

No hubo comando de instalación ni error de ADB durante el run.

## Impacto

Las ejecuciones de inspección sobre aplicaciones ya instaladas pueden aparecer
como fallidas aunque el lanzamiento y la medición sean válidos. Esto afecta la
lectura del índice y cualquier comparación automática basada solo en el campo
de resultado.

## Análisis técnico

El agregador usa la ausencia de un resultado de instalación como condición de
fallo y no distingue que, para `preinstalled-no-reinstall`, esa ausencia es
esperada. La evidencia de lanzamiento se conserva correctamente; el defecto se
limita a la clasificación final.

## Solución aplicada

La matriz de EXEC-050 y su entrada en el índice se corrigieron mediante una
revisión explícita, sin reescribir los CSV históricos. La corrección del
agregador queda pendiente para aceptar una ejecución preinstalada cuando exista
evidencia de lanzamiento o muestras válidas.

## Resultado

Limitación detectada y documentada. EXEC-050 se interpreta como una observación
válida del flujo Core, no como una instalación fallida.

## Limitaciones pendientes

- Añadir una regla específica para `preinstalled-no-reinstall`.
- Incorporar una prueba automatizada que cubra lanzamiento exitoso sin fila de
  instalación.
- Regenerar catálogos solo mediante una revisión explícita que conserve la
  trazabilidad del resultado histórico.

## Referencias

- [Matriz de EXEC-050](../ejecuciones/50-metricas-ui-base-nocore-redmi-horizontal-20260920/matriz.md)
- [Run estructurado](../metricas/runs/RUN-20260920-001/)

## Ejecuciones asociadas

- [EXEC-050](../ejecuciones/50-metricas-ui-base-nocore-redmi-horizontal-20260920/matriz.md)
