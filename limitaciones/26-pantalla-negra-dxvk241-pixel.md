# 26. Pantalla negra con DXVK 2.4.1 en Pixel Tensor/Mali

## Descripción

La publicación v41 mantuvo vivos el proceso Android y `Cuphead.exe` en el Pixel 9a, pero la superficie visible permaneció completamente negra. El resultado invalida la clasificación inicial basada sólo en procesos y memoria.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Tensor G4 / Mali-G715, Android API 37.
- Publicación: versionCode `41`, `11.1-direct-files-auto-gpu-recovery-v11-fcharan-dxvk241`.
- Perfil: Vortek 2.1 + Gladio 1.0 + DXVK 2.4.1 + capa BCn Fcharan automática/ETC2.
- Resolución: `1280x720`.
- Payload directo: `815` archivos, `5847372363` bytes.
- Staging de bundletool: ausente después de la limpieza documentada en EXEC-028.

## Observación

La captura obtenida con `screencap` es negra. En el mismo corte:

- `XServerDisplayActivity` era la actividad superior reanudada.
- SurfaceFlinger enumeró el SurfaceView de la actividad.
- `com.cuphead` y `Cuphead.exe` estaban vivos.
- La memoria era PSS `553042 KiB`, RSS `677452 KiB` y Graphics `475092 KiB`.
- Unity registró `Direct3D 11.0` y `Renderer: Vortek (Mali-G715)`.

No apareció un mensaje fatal de Unity ni un cierre `LOW_MEMORY` en ese corte.

## Interpretación

La evidencia descarta como explicación primaria la ausencia del ejecutable, la pérdida del payload y el cierre Android por memoria. Es consistente con un fallo de renderizado o presentación en la combinación DXVK 2.4.1, Vortek y el driver Mali del Pixel. La evidencia disponible no permite atribuirlo a un componente más específico.

## Intento de mitigación

Se probó temporalmente `dxgi.deferSurfaceCreation=True`, opción documentada por DXVK 2.4.1 para ciertos casos de ventana negra. La captura siguió negra, con el cursor visible, por lo que el intento fue retirado.

## Impacto

v41 no es una publicación funcional para el Pixel, aunque reduzca de forma importante la memoria respecto de las variantes DXVK-Sarek. A partir de este fallo, toda validación gráfica requiere evidencia visual además de procesos vivos.

## Acciones correctivas en prueba

La v42 sustituyó únicamente el DXVK del perfil Mali por la versión 1.7.2 incluida en WinlatorMali Bionic. Recuperó el render visible, pero la memoria del proceso Android creció hasta PSS `2816620 KiB` y Graphics `2750532 KiB` a los 40 s; Android terminó la aplicación con `reason=3 (LOW_MEMORY)` aproximadamente a los 82 s.

La v43 volvió a DXVK 2.4.1 y cambió BCn automático por decodificación compute completa (`BCN_COMPUTE_AUTO=0`, `WRAPPER_EMULATE_BCN=2`). La memoria combinada bajó a PSS `959616 KiB` en el corte de 30 s, pero la captura siguió negra excepto por el cursor. Esto descarta el modo automático/completo de Fcharan como explicación única.

La v44 en `EXEC-031` restauró DXVK-Sarek 1.13.0 y el binario Leegao ETC2 cuya huella coincide con el perfil histórico jugable. Tanto la integración dentro del rootfs como la capa Android recuperaron imagen. La primera volvió a terminar por memoria; la segunda conservó el título visible más allá de 90 s y lo reprodujo en un segundo arranque a 45 s. El log confirmó que Android cargó `VK_LAYER_BCN_BCnLayer` desde `/data/user/0/com.cuphead/libVkLayer_BCN_BCnLayer.so`.

## Estado

Reproducida con v41 y v43; v42 recupera imagen pero falla por memoria. Resuelta experimentalmente en el Pixel probado con v44, DXVK-Sarek 1.13.0 y Leegao BCn ETC2 cargada como capa Android. La solución aún no es autónoma porque requiere configuración ADB de depuración GPU.

## Evidencia y ejecución asociada

- [EXEC-029](../ejecuciones/29-pantalla-negra-dxvk241-pixel/matriz.md)
- [Captura negra](../ejecuciones/29-pantalla-negra-dxvk241-pixel/evidencias/pixel-v41-pantalla-negra.png)
- [Log de Unity](../ejecuciones/29-pantalla-negra-dxvk241-pixel/logs/pixel-v41-cuphead-output_log.txt)
- [Memoria](../ejecuciones/29-pantalla-negra-dxvk241-pixel/logs/pixel-v41-meminfo.txt)
- [Captura v43](../ejecuciones/29-pantalla-negra-dxvk241-pixel/evidencias/pixel-v43-bcnfull-30s.png)
- [EXEC-031](../ejecuciones/31-restauracion-perfil-historico-pixel/matriz.md)
- [Captura v44 a más de 90 s](../ejecuciones/31-restauracion-perfil-historico-pixel/evidencias/pixel-v44-android-layer-90s.png)
- [Log de la capa Android](../ejecuciones/31-restauracion-perfil-historico-pixel/logs/android-layer-result.md)
