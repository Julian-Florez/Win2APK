# EXEC-029: Diagnóstico de pantalla negra y sustitución de DXVK en Pixel 9a

## Identificación

- ID: `EXEC-029`
- Fecha: 2026-09-18
- Tipo: diagnóstico visual y prueba de compatibilidad DXVK
- Dispositivo inicial: Google Pixel 9a, serial `4A021JEBF06953`, Tensor G4 / Mali-G715, Android API 37.
- Publicación de partida: v41, `11.1-direct-files-auto-gpu-recovery-v11-fcharan-dxvk241`.
- Objetivo: recuperar una imagen visible sin reintroducir la duplicación del payload ni modificar el perfil Adreno.

## Condiciones conservadas

| Parámetro | Valor |
|---|---|
| Driver | Vortek 2.1 + Gladio 1.0 |
| Capa BCn | Fcharan `5c168f4`, compute automático, ETC2 y caché |
| Resolución | `1280x720` |
| Límite anunciado | `maxDeviceMemory=1024` |
| Payload directo | `815` archivos, `5847372363` bytes |
| Staging `local_testing` | Ausente en Pixel después de EXEC-028 |
| `android:largeHeap` | Ausente |

## Observación inicial de v41

- La captura ADB es un cuadro completamente negro.
- `XServerDisplayActivity` era la actividad reanudada y su SurfaceView estaba registrado en SurfaceFlinger.
- `com.cuphead` y `Cuphead.exe` estaban vivos con PID `10432` y `10654` en el corte inicial.
- `dumpsys meminfo` registró PSS `553042 KiB`, RSS `677452 KiB` y Graphics `475092 KiB`.
- Unity reconoció `Direct3D 11.0` y `Renderer: Vortek (Mali-G715)` sin registrar un error fatal en `output_log.txt`.

La observación diferencia inicialización de D3D11 de presentación funcional: tener procesos vivos y memoria estable no basta para aprobar el juego.

## Intento A: creación diferida de superficie

Se añadió de manera temporal y reversible `DXVK_CONFIG=dxgi.deferSurfaceCreation=True` al contenedor del Pixel. La opción está documentada por DXVK 2.4.1 para aplicaciones cuya ventana puede permanecer negra si la superficie Vulkan se crea antes del primer `Present`.

Resultado: no aprobado. Después de 35 s, la captura siguió negra y sólo mostró el cursor. `com.cuphead` y `Cuphead.exe` permanecieron vivos con PID `15171` y `15316`. La modificación se retiró antes de preparar la publicación siguiente.

## Variante v42

| Parámetro | v41 | v42 |
|---|---|---|
| DXVK del perfil Mali | `2.4.1` | `1.7.2` |
| Origen de la variante | Winlator base | WinlatorMali Bionic, commit `fbf42d26411444249a301086da0dcb652b861b17` |
| Perfil Adreno | sin cambios | sin cambios |
| Resto del perfil Pixel | referencia | sin cambios |
| versionCode | `41` | `42` |

DXVK 1.7.2 es el valor predeterminado declarado por el fork WinlatorMali Bionic consultado. Su uso aquí es una hipótesis de compatibilidad específica, no una afirmación general sobre GPU Mali.

## Criterios de aceptación

- Captura ADB con contenido visible del juego; un cursor sobre fondo negro no aprueba.
- `Cuphead.exe` vivo después del umbral aproximado de 72 s que falló en variantes Sarek.
- Ausencia de un nuevo `LOW_MEMORY`, crash de Unity o error de inicialización gráfica durante la ventana registrada.
- Marcador directo válido y ausencia de una segunda copia en `local_testing`.
- El perfil Adreno no cambia en el código ni en la configuración generada.

## Resultado v42

| Campo | Resultado |
|---|---|
| Build | Correcto, `3m39s` |
| APK base-only | `276959256` bytes; SHA-256 `778ddccca640d5c130a52618664b58bb9dc7f5aabfa42408c56ba11b63410442` |
| Instalación | `adb install -r`, correcta en `10.317 s` |
| Marcador tras actualizar | `815` archivos, `5847372363` bytes |
| Validación visual | Aprobada a los 40 s: se observó el grano de película renderizado por Cuphead, no un cuadro negro plano |
| Memoria a los 40 s | PSS `2816620 KiB`, RSS `2864164 KiB`, Graphics `2750532 KiB` en `com.cuphead` |
| Cierre | `reason=3 (LOW_MEMORY)` a las `21:48:31.774`, aproximadamente 82 s después del lanzamiento |

v42 demuestra que DXVK 1.7.2 corrige la presentación, pero no es una solución estable: reintroduce un crecimiento de memoria gráfica muy superior al de v41.

## Variante v43

La comparación de [EXEC-030](../30-comparacion-memoria-gpu-cuatro-dispositivos/matriz.md) mostró que el Pixel con v42 consumía entre 46 % y 49 % más PSS combinado y entre 2,16 y 2,23 veces la memoria gráfica de los dispositivos Adreno. Para aislar la selección BCn, v43 vuelve a DXVK 2.4.1 y cambia sólo el modo BCn de automático a decodificación compute completa según los valores observados en WinlatorMali:

| Parámetro | v41 | v43 |
|---|---|---|
| DXVK | `2.4.1` | `2.4.1` |
| `BCN_COMPUTE_AUTO` | `1` | `0` |
| `WRAPPER_EMULATE_BCN` | `3` | `2` |
| ETC2 / caché | activados | activados |
| Perfil Adreno | referencia | sin cambios |

## Resultado v43

| Campo | Resultado |
|---|---|
| Build | Correcto, `3m42s` |
| APK base-only | `276959256` bytes; SHA-256 `0edc27f908f8f2b339642956f2f3be8759c9da5e68216df25be007eaecf53314` |
| Instalación | `adb install -r`, correcta en `10.588 s` |
| Marcador tras actualizar | `815` archivos, `5847372363` bytes |
| Validación visual | No aprobada: cuadro negro excepto por el cursor a los 30 s |
| Memoria combinada a los 30 s | PSS `959616 KiB`, RSS `1102888 KiB`; Graphics del proceso Android `488676 KiB` |
| Interpretación | Forzar BCn compute completo redujo la memoria frente a v42, pero no recuperó la presentación con DXVK 2.4.1 |

## Evidencia

- [Captura negra de v41](./evidencias/pixel-v41-pantalla-negra.png)
- [Configuración del contenedor v41](./logs/pixel-v41-container.json)
- [Memoria de v41](./logs/pixel-v41-meminfo.txt)
- [Log de Unity v41](./logs/pixel-v41-cuphead-output_log.txt)
- [Logcat filtrado de v41](./logs/pixel-v41-logcat-filtrado.txt)
- [Render visible de v42 a los 40 s](./evidencias/pixel-v42-render-40s.png)
- [Pantalla de inicio después del cierre v42](./evidencias/pixel-v42-cierre-75s.png)
- [Memoria v42 a los 40 s](./logs/pixel-v42-meminfo-40s.txt)
- [Exit info v42](./logs/pixel-v42-exit-info.txt)
- [Pantalla negra de v43](./evidencias/pixel-v43-bcnfull-30s.png)
- [Memoria v43 a los 30 s](./logs/pixel-v43-memoria-30s.txt)

## Relación

- Antecedente: [EXEC-028](../28-dxvk241-pixel/matriz.md)
- Fallo asociado: [limitación 26](../../limitaciones/26-pantalla-negra-dxvk241-pixel.md)
