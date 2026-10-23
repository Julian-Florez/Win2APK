# 51. Primer frame tardío de Bomb Rush Cyberfunk en Redmi Note 8 tras instalación fría

## Descripción

En cinco instalaciones frías consecutivas de Bomb Rush Cyberfunk en el Redmi
Note 8, la instalación terminó correctamente. Las capturas T+60 mostraron la
pantalla de Winlator `Preparing application…`; aun así, el proceso y el primer
frame del juego aparecieron dentro de la observación de 300 s. El tiempo desde
el inicio de Bundletool hasta el primer frame osciló entre 200.586 s y 209.573
s. En las segundas aperturas el primer frame apareció entre 13.044 s y 15.836 s;
las capturas T+60 mostraron el título en dos ensayos y la introducción en tres.
No se observó un cierre durante estas fases. Es una demora de arranque frío
reproducida en este dispositivo y artefacto; la causa queda pendiente.

## Contexto técnico

- Dispositivo: Xiaomi Redmi Note 8, Android 16/API 36, ABI `arm64-v8a`, SoC
  Qualcomm SM6125, GPU Adreno 610; inventario en
  [dispositivos.csv](../metricas/runs/RUN-20261023-042/dispositivos.csv).
- Aplicación: paquete `com.win2apk.bombrushcyberfunk`; proceso
  `Bomb Rush Cyberfunk.exe`.
- Artefacto: `bomb-rush-cyberfunk-gog-56774571391351451.apks`.
- SHA-256: `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54`.
- Método: desinstalación e instalación limpia con Bundletool 1.18.3; monitoreo
  durante 300 s tras la instalación y otros 300 s en la segunda apertura.
  Winlator y la configuración del contenedor: N/R en estas ejecuciones.

## Reproducción o evidencia

| Ejecución / run | Instalación | Desde inicio de Bundletool a primer frame | Proceso del juego observado desde el inicio del monitor | Second-open a primer frame | Captura fría T+60 | Captura second-open T+60 |
|---|---:|---:|---:|---:|---|---|
| [EXEC-121 / RUN-042](../ejecuciones/121-metricas-bomb-rush-cold-second-open-trial-01-20261023/matriz.md) | 89.828 s | 209.573 s | 116.141 s | 13.721 s | `loading` / preparación | `cutscene` |
| [EXEC-122 / RUN-043](../ejecuciones/122-metricas-bomb-rush-cold-second-open-trial-02-20261023/matriz.md) | 75.808 s | 200.586 s | 122.570 s | 15.836 s | `loading` / preparación | `title_screen` |
| [EXEC-123 / RUN-044](../ejecuciones/123-metricas-bomb-rush-cold-second-open-trial-03-20261023/matriz.md) | 75.799 s | 201.934 s | 122.637 s | 13.056 s | `loading` / preparación | `cutscene` |
| [EXEC-124 / RUN-045](../ejecuciones/124-metricas-bomb-rush-cold-second-open-trial-04-20261023/matriz.md) | 75.125 s | 207.948 s | 128.165 s | 13.756 s | `loading` / preparación | `cutscene` |
| [EXEC-125 / RUN-046](../ejecuciones/125-metricas-bomb-rush-cold-second-open-trial-05-20261023/matriz.md) | 75.526 s | 204.327 s | 125.164 s | 13.044 s | `loading` / preparación | `title_screen` |

Las cinco capturas frías contienen `Preparing application…` y fueron revisadas
como pantalla de carga/interfaz de compatibilidad. La columna «desde inicio de
Bundletool» conserva la métrica extremo a extremo del resumen; la columna del
proceso del juego corresponde al reloj de la fase de monitorización, que empieza
después de instalar. En todas las fases frías hubo primer frame antes de T+300;
por eso `partial` describe que la captura canónica T+60 no coincide con el estado
esperado `title_screen`, no una ausencia de frame.

Las cinco segundas aperturas registraron el proceso y el primer frame. Las
capturas de EXEC-121, EXEC-123 y EXEC-124 muestran la pantalla de introducción;
EXEC-122 y EXEC-125 muestran `Press Any Key`. Los resúmenes indican que la app y
el juego permanecieron activos durante la mayor parte de cada ventana. Las
capturas, CSV, eventos y logs originales se conservan en las carpetas RUN-042 a
RUN-046 enlazadas arriba.

## Impacto

En este Redmi Note 8, la instalación limpia no llega a la pantalla de título en
el instante T+60: Winlator continúa preparando la aplicación. Sin embargo, el
primer frame del juego sí se detecta entre aproximadamente 116 s y 128 s desde
el inicio del monitoreo posterior a la instalación, siempre dentro de los 300 s
observados. Las segundas aperturas son mucho más rápidas en cuanto al primer
frame, pero su estado a T+60 varía entre introducción y título.

## Análisis técnico

La demora se repitió con el mismo dispositivo, artefacto y protocolo; las
segundas aperturas fueron consistentemente más rápidas. No se observó un crash
concluyente ni una caída del proceso durante el muestreo. Una inicialización o
preparación del entorno en el primer arranque podría explicar la diferencia,
pero es una hipótesis: estas mediciones no identifican el mecanismo causal.

## Solución aplicada

No se modificaron ajustes de Winlator, del contenedor ni del juego. Se conservó
la instalación entre la fase fría y la segunda apertura, y se mantuvo el mismo
protocolo de 300 s en los cinco ensayos.

## Resultado

Demora de primer arranque reproducida en cinco ensayos válidos del Redmi Note 8.
Los cinco alcanzaron un primer frame dentro de 300 s; las cinco capturas frías
T+60 aún mostraban preparación de la aplicación. No es evidencia de
compatibilidad universal ni permite atribuir la demora a una causa específica.

## Limitaciones pendientes

- Confirmar cuánto tarda cada ensayo en alcanzar el título interactivo; la
  captura protocolaria T+60 no documenta ese estado posterior.
- Comparar este patrón con los resultados de Bomb Rush en los demás dispositivos
  sin extrapolar desde el Redmi Note 8.
- Investigar la etapa de preparación solo si se autoriza una prueba diagnóstica
  que cambie el protocolo o la configuración.

## Referencias

- [RUN-20261023-042](../metricas/runs/RUN-20261023-042/)
- [RUN-20261023-043](../metricas/runs/RUN-20261023-043/)
- [RUN-20261023-044](../metricas/runs/RUN-20261023-044/)
- [RUN-20261023-045](../metricas/runs/RUN-20261023-045/)
- [RUN-20261023-046](../metricas/runs/RUN-20261023-046/)

## Ejecuciones asociadas

- [EXEC-121](../ejecuciones/121-metricas-bomb-rush-cold-second-open-trial-01-20261023/matriz.md)
- [EXEC-122](../ejecuciones/122-metricas-bomb-rush-cold-second-open-trial-02-20261023/matriz.md)
- [EXEC-123](../ejecuciones/123-metricas-bomb-rush-cold-second-open-trial-03-20261023/matriz.md)
- [EXEC-124](../ejecuciones/124-metricas-bomb-rush-cold-second-open-trial-04-20261023/matriz.md)
- [EXEC-125](../ejecuciones/125-metricas-bomb-rush-cold-second-open-trial-05-20261023/matriz.md)
