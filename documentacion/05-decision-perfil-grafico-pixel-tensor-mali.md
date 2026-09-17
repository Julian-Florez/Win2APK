# Decisión de perfil gráfico para Pixel Tensor/Mali

- **Fecha:** 2026-08-25
- **Estado:** decisión provisional para el prototipo
- **Propósito:** elegir el perfil predeterminado del Pixel 9a después de comparar estabilidad y fidelidad visual.

## Problema

El Pixel 9a usa una GPU Mali-G715 y no puede reutilizar sin cambios el perfil Turnip destinado a Adreno. Las rutas alternativas para texturas BCn presentaron un intercambio entre fidelidad, memoria y estabilidad.

## Decisión

Para el Pixel 9a probado, Win2APK debe preferir provisionalmente:

- Vortek 2.1 + Gladio 1.0;
- DXVK-Sarek 1.13.0;
- transcodificación BCn a ETC2;
- 1280x720;
- límite de memoria reportada por DXVK de 1024 MiB;
- Box64 `INTERMEDIATE` y audio ALSA.

La selección automática futura debe basarse en capacidades y perfil de GPU, conservar una anulación manual visible y evitar activar en este dispositivo las variantes ASTC, Fcharan o preservación BC3-RGBA que fueron rechazadas en la ejecución.

## Justificación

Este fue el único perfil de los comparados que mantuvo simultáneamente inicio, texturas presentes, audio, control y gameplay aceptable durante la sesión manual. Las alternativas no corrigieron el borde borroso y añadieron cierres, stuttering, texturas ausentes o presión de memoria.

La decisión prioriza estabilidad sobre una mejora visual no demostrada. El defecto de bordes transparentes se acepta por ahora como limitación del Pixel 9a y no se extrapola a otros dispositivos.

## Evidencia

- [EXEC-020: comparación de perfiles](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md)
- [Limitación 14: fidelidad de texturas](../limitaciones/14-fidelidad-texturas-pixel-tensor-mali.md)

## Alcance

Esta decisión define el perfil del prototipo y el estado que quedó instalado en el Pixel. No demuestra todavía que el AAB seleccione el perfil de manera autónoma ni que la configuración sea estable en todos los Pixel, Tensor o Mali.

## Decisiones pendientes

- Integrar la detección de GPU, driver, ABI y versión Android en el selector de perfiles.
- Definir el fallback cuando el perfil preferido no pueda inicializar Direct3D 11.
- Repetir una prueba de duración fija con el perfil integrado, sin ajustes ADB externos.
- Mantener Turnip como perfil separado para Adreno y validar la Lenovo antes de ampliar la matriz.
