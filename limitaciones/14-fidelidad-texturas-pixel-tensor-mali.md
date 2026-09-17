# Fidelidad de texturas transparentes en Pixel Tensor/Mali

- **Proyecto:** Win2APK
- **Aplicación:** Cuphead mediante entorno de compatibilidad
- **Estado:** aceptada provisionalmente por dispositivo
- **Fecha de registro:** 2026-08-25

## Descripción

En el Pixel 9a con GPU Mali-G715, el perfil que permitió ejecutar Cuphead con audio, control y framerate aceptables muestra bordes borrosos o pixelados en algunas texturas con transparencia. La misma anomalía no fue observada por el usuario en el Xiaomi Mi A3 usado como referencia.

La limitación se atribuye al conjunto Pixel 9a + Android 17 beta + Vortek/Gladio + DXVK-Sarek + transcodificación BCn a ETC2 probado aquí. No se afirma que afecte a todos los dispositivos Mali, Tensor, Pixel o versiones de Android.

## Contexto técnico

| Campo | Valor |
|---|---|
| Dispositivo | Google Pixel 9a (`tegu`) |
| Android/API | Android 17 beta / API 37, `CP41.260731.005.B1` |
| ABI | `arm64-v8a` |
| GPU | ARM Mali-G715 |
| Driver informado | OpenGL ES 3.2 `v1.r54p3-00eac0.44603346b7f0666d385a72285181f505` |
| Wrapper final | DXVK-Sarek 1.13.0 |
| Driver final | Vortek 2.1 + Gladio 1.0 |
| Resolución final | 1280x720 |
| Capa de texturas | BCn layer, transcodificación ETC2 |

## Reproducción o evidencia

1. Iniciar el paquete `com.cuphead` con el contenedor descrito en [EXEC-020](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md).
2. Conectar un control físico y entrar al juego.
3. Observar los contornos de elementos con transparencia.
4. Comparar con la captura de referencia del Mi A3 bajo sus propias condiciones de ejecución.

Evidencias visuales:

- [Pixel, ETC2 jugable](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/evidencias/01-etc2-gameplay.png)
- [Pixel, defecto en bordes](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/evidencias/02-etc2-bordes-transparentes.png)
- [Mi A3, referencia](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/evidencias/03-mi-a3-referencia.png)

La clasificación de “borroso/pixelado” es una observación visual del usuario; no se obtuvo una imagen de referencia renderizada por el mismo Pixel sin transcodificación para calcular una diferencia cuantitativa.

## Impacto

- El juego puede ser utilizable en este Pixel, pero la fidelidad visual no coincide con la referencia observada en el Mi A3.
- La instalación sin duplicación de datos no se ve afectada; la limitación pertenece a la etapa de ejecución gráfica.
- Un perfil automático no debe elegir una variante de mayor calidad teórica si esa variante reduce estabilidad, elimina texturas o provoca cierres.

## Análisis técnico

La traza diagnóstica en la pantalla de título registró imágenes BC1a, BC3 y BC7. La prueba que mantuvo 130 imágenes BC3 en RGBA no eliminó el defecto, por lo que **BC3 no explica por sí solo** la anomalía. El inventario offline identificó además texturas BC7 de gran tamaño; conservar todas en RGBA aumentaría materialmente la memoria. Esta última relación es una estimación técnica, no una prueba de que una textura BC7 concreta sea la causa visual.

Las variantes produjeron resultados distintos:

- cambiar de 1280x720 a 1920x1080 y desactivar el efecto cromático no corrigió el borde;
- ASTC mantuvo el defecto y el proceso terminó posteriormente por uso excesivo de CPU;
- la variante Fcharan con ASTC de alta calidad y omisión de texturas pequeñas produjo texturas ausentes, stuttering, menor velocidad y `LOW_MEMORY`;
- preservar BC3 como RGBA mantuvo el defecto y añadió presión de memoria.

No se demostró de forma causal si el borde proviene de la transcodificación ETC2, del muestreo alfa, del driver Mali, de Vortek o de una interacción entre ellos. Se conserva como hipótesis abierta.

## Solución aplicada

Se restauró el perfil más estable observado:

- Vortek 2.1 + Gladio 1.0;
- DXVK-Sarek 1.13.0;
- transcodificación BCn a ETC2;
- 1280x720;
- `libbcn_layer.so` SHA-256 `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`;
- shim SHA-256 `053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565`.

El perfil conserva el defecto visual, pero evitó en la sesión validada los problemas más graves de las alternativas. La aplicación no debe activar automáticamente en este Pixel las variantes ASTC, Fcharan o BC3-RGBA probadas.

## Resultado

El perfil ETC2 fue restaurado y el paquete volvió a mostrar la pantalla de título. La evidencia previa con control físico registró gameplay, audio y framerate aceptables según el usuario. La fidelidad de algunos bordes transparentes queda aceptada como limitación específica de este dispositivo/perfil.

“Más estable” es una comparación entre las variantes de esta ejecución, no una garantía de estabilidad indefinida. La validación de larga duración del binario integrado permanece pendiente.

## Limitaciones pendientes

- La selección automática por GPU/capacidades todavía debe integrarse en el paquete; la prueba utilizó configuración diagnóstica por ADB.
- No se midió una sesión repetida de duración fija ni una tasa de éxito.
- Android 17 estaba en beta; el resultado puede cambiar con otra compilación del sistema o driver.
- No se aisló una textura BC7 específica como causa del defecto.
- El control por toques no formó parte de esta corrección; el gameplay se validó con control físico.

## Referencias

- [Guía de wrappers gráficos de Bannerlator](https://github.com/The412Banner/Bannerlator/blob/main/docs/graphics-wrappers-guide.md)
- [Capa BCn upstream](https://github.com/leegao/bcn_layer)
- [WinlatorMali](https://github.com/GunaCharanTeja/WinlatorMali)

## Ejecuciones asociadas

- [EXEC-020](../ejecuciones/20-comparacion-graficos-pixel-tensor-mali/matriz.md)
