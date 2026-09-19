# Decisión sobre la capa BCn Android para Pixel Tensor/Mali

- **Fecha:** 2026-09-18
- **Estado:** adoptada como referencia experimental; integración autónoma pendiente
- **Propósito:** fijar la combinación gráfica que recuperó imagen y evitó el cierre por memoria en el Pixel 9a, conservando una sola publicación con perfiles automáticos por GPU.

## Problema

Las variantes recientes del perfil Mali separaron dos fallos: DXVK 2.4.1 mantuvo un consumo menor pero mostró pantalla negra, mientras DXVK 1.7.2 y distintas versiones Sarek recuperaron imagen y terminaron por presión de memoria. El Pixel es el dispositivo más potente de la matriz, pero su GPU Mali requiere una ruta distinta de los tres dispositivos Adreno; la potencia general no sustituye la compatibilidad del driver y del formato de texturas.

## Evidencia

[EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md) restauró los componentes exactos del perfil histórico:

- Vortek 2.1 + Gladio 1.0;
- DXVK-Sarek 1.13.0;
- Leegao BCn ETC2, SHA-256 `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`;
- shim `VK_LAYER_BCN_BCnLayer`, SHA-256 `053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565`;
- resolución `1280x720`, `maxDeviceMemory=1024` e `imageCacheSize=0`.

La misma combinación produjo resultados distintos según la integración. Dentro del rootfs mostró imagen, pero agotó la memoria y Android la terminó antes de 90 s. Como capa Vulkan cargada por Android mostró el título en dos arranques, mantuvo los procesos más allá de 90 s y estabilizó `ION_heap` alrededor de 1.324 GiB durante la ventana medida.

## Decisión

El perfil de referencia para Tensor/Mali queda definido por DXVK-Sarek 1.13.0 + Leegao BCn ETC2 cargada como capa Android. No se volverá a tratar la capa dentro del rootfs como equivalente, porque la ejecución controlada demostró un comportamiento de memoria diferente.

La distribución conserva un único artefacto y selecciona el perfil según el renderer, vendor y hardware:

| Familia detectada | Perfil previsto |
|---|---|
| Adreno / Qualcomm | Turnip + Gladio + DXVK ya validado en los dispositivos Adreno de la matriz |
| Mali / Tensor | Vortek + Gladio + DXVK-Sarek 1.13.0 + Leegao BCn ETC2 por ruta Android |
| GPU desconocida | Perfil conservador; resultado no validado y registro diagnóstico obligatorio |

Esta tabla es una política del prototipo, no una declaración de compatibilidad universal.

## Alcance de la decisión

La ruta gráfica queda demostrada en el Pixel 9a probado, pero la publicación v44 no es todavía una solución final. Su resultado positivo dependió de ajustes globales enviados por ADB, y la aplicación normal no ha demostrado que pueda habilitarlos por sí sola. La limitación se registra en [limitación 27](../limitaciones/27-capa-bcn-android-requiere-configuracion-adb.md).

El almacenamiento directo se mantuvo: solo se encontró un `Cuphead.exe`, el staging `local_testing` estaba ausente y no se generó una segunda instalación del juego dentro de los datos privados observados. El valor de `du` no se iguala retrospectivamente con el marcador lógico histórico porque emplean métodos de medición distintos.

## Decisiones descartadas

- DXVK 2.4.1 + Fcharan BCn para Pixel: procesos vivos, pero pantalla negra.
- DXVK 1.7.2 + BCn dentro del rootfs: imagen visible, pero cierre por memoria.
- DXVK-Sarek 1.13.0 + Leegao BCn dentro del rootfs: imagen visible, pero cierre por memoria.
- Turnip en Pixel: no corresponde a la GPU Mali y no se considera una sustitución válida.

## Pendientes

- Empaquetar y activar la capa BCn sin `settings put global` ni preparación ADB.
- Probar la solución desde una instalación limpia y repetir la creación del contenedor.
- Ejecutar una sesión prolongada con control, audio y captura de FPS/frame time.
- Verificar que la ruta Adreno permanezca sin regresiones en los otros tres dispositivos con el mismo artefacto.

## Relaciones

- [EXEC-020: perfil histórico](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md)
- [EXEC-029: pantalla negra y memoria](../ejecuciones/29-pantalla-negra-dxvk241-pixel/matriz.md)
- [EXEC-031: restauración controlada](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md)
- [Limitación 23: presión de memoria](../limitaciones/23-pixel-low-memory-metrica-20260918.md)
- [Limitación 26: pantalla negra](../limitaciones/26-pantalla-negra-dxvk241-pixel.md)
- [Limitación 27: dependencia de ADB](../limitaciones/27-capa-bcn-android-requiere-configuracion-adb.md)
