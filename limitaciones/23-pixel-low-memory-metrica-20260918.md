# Cierre del Pixel 9a por presión de memoria durante la medición

- **Proyecto:** Win2APK
- **Aplicación:** Cuphead mediante entorno de compatibilidad
- **Estado:** resuelta experimentalmente en v44 mediante capa BCn Android; autonomía y sesión prolongada pendientes
- **Fecha de registro:** 2026-09-18

## Descripción

Durante una medición controlada del Pixel 9a (`4A021JEBF06953`), `Cuphead.exe` apareció aproximadamente cinco segundos después del lanzamiento, permaneció observable durante unos 67,5 s y el proceso Android terminó con `LOW_MEMORY`. En la misma instantánea, Redmi Note 8, Mi A3 y Lenovo TB-J606F mantenían `Cuphead.exe` activo; esto es una diferencia observada entre esos casos, no una prueba de compatibilidad universal.

## Contexto técnico

| Campo | Valor |
|---|---|
| Dispositivo | Google Pixel 9a, `tegu` |
| Android/API | Android 17 / API 37 |
| ABI | `arm64-v8a` |
| Publicación observada | `versionCode=34`, `11.1-direct-files-auto-gpu-recovery-v4` |
| Resolución física | 1080x2424 |
| Payload | Marcador de 815 archivos y 5847372363 bytes |
| Perfil gráfico efectivo en esta captura | N/R; no se conserva log runtime completo del selector |

## Reproducción o evidencia

1. Consultar el estado del paquete sin desinstalarlo.
2. Ejecutar `am force-stop com.cuphead` para comenzar desde un estado conocido.
3. Ejecutar `monkey -p com.cuphead 1`.
4. Sondear `pidof Cuphead.exe` durante 150 s.
5. Consultar `dumpsys activity exit-info com.cuphead`.

Mensaje exacto:

```text
reason=3 (LOW_MEMORY) subreason=0 (UNKNOWN) status=0
```

La evidencia completa está en [EXEC-025](../ejecuciones/25-metricas-multidispositivo-20260918/matriz.md), [pixel-arranque-150s.txt](../ejecuciones/25-metricas-multidispositivo-20260918/logs/pixel-arranque-150s.txt) y [procesos-memoria-cpu.md](../ejecuciones/25-metricas-multidispositivo-20260918/logs/procesos-memoria-cpu.md).

## Impacto

- El Pixel no cumplió la permanencia de la ventana de observación.
- La matriz no puede declarar estabilidad de la versión `v4` en este dispositivo.
- El cierre no se atribuye causalmente a una resolución, wrapper o driver concreto porque esa configuración runtime no quedó registrada en esta medición.

## Análisis técnico

La observación demuestra un cierre clasificado por Android como `LOW_MEMORY`, pero no identifica qué asignación o componente lo provocó. Existen antecedentes en [EXEC-020](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md) de presión de memoria en variantes gráficas del Pixel, pero no deben mezclarse como si fueran la misma corrida o publicación.

La ejecución posterior [EXEC-024](../ejecuciones/24-investigacion-forks-pixel/matriz.md) repitió el cierre con `versionCode=35` y un perfil registrado: Vortek 2.1 + Gladio 1.0, DXVK-Sarek 1.11.1, capa `bcn_layer` shader-v3 con ETC2 y `1280x720`. La capa se cargó y `Cuphead.exe` inició, pero `dumpsys activity exit-info` volvió a registrar `reason=3 (LOW_MEMORY)` a las 19:43:52.957, aproximadamente 71 segundos después del lanzamiento. La variante redujo la muestra intermedia de memoria, pero no alcanzó permanencia estable.

Las variantes Fcharan con DXVK-Sarek 1.12.1 también terminaron por `LOW_MEMORY`: v36, v37, v38 y v39 cerraron cerca de la misma ventana de 70 a 72 s. v40, que alineó BCn con `BCN_COMPUTE_AUTO=1` y calidad `auto`, redujo el primer corte de memoria, pero terminó a las 20:38:49.639 con `reason=3 (LOW_MEMORY)`. Estos resultados están separados en [EXEC-026](../ejecuciones/26-validacion-v38-cuatro-dispositivos/matriz.md) y [EXEC-027](../ejecuciones/27-variante-bcn-auto-pixel/matriz.md).

La variante v41 cambió únicamente el DXVK del perfil Mali a `2.4.1`, mantuvo BCn automático y no incluyó `largeHeap`. El Pixel conservó `Cuphead.exe` vivo desde las 20:44:07.140 hasta el corte de 20:48:38, con PSS `555304 KiB`, RSS `681212 KiB` y sin un nuevo registro `LOW_MEMORY`. Es una resolución experimental en la ventana observada, no un cierre definitivo de la limitación. La matriz y los logs están en [EXEC-028](../ejecuciones/28-dxvk241-pixel/matriz.md).

[EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md) aisló la ubicación de la capa con los binarios históricos exactos. DXVK-Sarek 1.13.0 y Leegao BCn ETC2 dentro del rootfs recuperaron la imagen, pero elevaron el PSS combinado a aproximadamente `2742906 KiB`, `ION_heap` superó `4.4 GiB` y Android terminó la aplicación antes de 90 s con `LOW_MEMORY`. Los mismos binarios, cargados como capa Vulkan Android externa mediante el shim histórico, mantuvieron `ION_heap` alrededor de `1.324 GiB`, dejaron aproximadamente `1.28–1.32 GiB` disponibles durante doce muestras y conservaron `com.cuphead` y `Cuphead.exe` vivos más allá de 90 s. No apareció un nuevo cierre por memoria durante esa ventana.

## Solución aplicada

En [EXEC-024](../ejecuciones/24-investigacion-forks-pixel/matriz.md) se probó una solución experimental con DXVK-Sarek y BCn compute. [EXEC-028](../ejecuciones/28-dxvk241-pixel/matriz.md) incorporó DXVK 2.4.1 y evitó el cierre dentro de la ventana observada, pero una revisión visual posterior mostró pantalla negra. [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md) recuperó DXVK-Sarek 1.13.0, Leegao BCn ETC2 y el shim Android históricos. Esta ruta es la primera de la serie actual que combina imagen visible, memoria estabilizada y permanencia superior a 90 s en el Pixel.

## Resultado

La limitación queda reproducida para las variantes Sarek con BCn dentro del rootfs y para v40. Queda resuelta experimentalmente en el Pixel probado cuando la capa BCn histórica se carga por Android. El resultado no se generaliza a otros modelos Mali y todavía depende de configuración ADB, por lo que no se considera cerrada.

## Limitaciones pendientes

- Integrar la ruta de capa Android de v44 sin ajustes manuales de depuración GPU.
- Confirmar v44 con control y audio durante una sesión real prolongada, no solo con la presencia de los procesos y la pantalla de título.
- Comparar sólo publicaciones idénticas entre los cuatro dispositivos.
- Obtener telemetría FPS real del juego; `gfxinfo` no es suficiente.

## Referencias

- [EXEC-025: matriz multidispositivo](../ejecuciones/25-metricas-multidispositivo-20260918/matriz.md)
- [EXEC-020: comparación histórica de Pixel Tensor/Mali](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md)

## Ejecuciones asociadas

- [EXEC-025](../ejecuciones/25-metricas-multidispositivo-20260918/matriz.md)
- [EXEC-024](../ejecuciones/24-investigacion-forks-pixel/matriz.md)
- [EXEC-026](../ejecuciones/26-validacion-v38-cuatro-dispositivos/matriz.md)
- [EXEC-027](../ejecuciones/27-variante-bcn-auto-pixel/matriz.md)
- [EXEC-028](../ejecuciones/28-dxvk241-pixel/matriz.md)
- [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md)
