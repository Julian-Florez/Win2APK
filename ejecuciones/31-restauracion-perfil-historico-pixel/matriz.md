# EXEC-031: Restauración del perfil histórico del Pixel 9a

## Identificación

- ID: `EXEC-031`
- Fecha: 2026-09-18
- Tipo: comparación de versiones y restauración controlada de perfil gráfico
- Dispositivo: Google Pixel 9a, serial `4A021JEBF06953`, Tensor G4 / Mali-G715, Android API 37
- Publicación probada: v44, `11.1-direct-files-auto-gpu-recovery-v14-pixel-sarek1130-leegao-etc2`
- Objetivo: comprobar si la regresión reciente proviene de los cambios de DXVK y capa BCn, restaurando los componentes con evidencia positiva de `EXEC-020` sin cambiar el perfil Adreno ni el almacenamiento directo.

## Comparación de configuraciones

| Componente | Perfil histórico v29 | v43 | v44 probada |
|---|---|---|---|
| GPU/driver | Mali-G715; Vortek 2.1 + Gladio 1.0 | Igual | Igual |
| Configuración Vortek | `maxDeviceMemory=1024,imageCacheSize=0` | Igual | Igual |
| DXVK | DXVK-Sarek 1.13.0 | DXVK 2.4.1 | DXVK-Sarek 1.13.0 |
| Capa BCn | Leegao `c4755eef`, SHA-256 `fcefa3fa...434f8d2` | Fcharan, SHA-256 `44115e67...c06b47` | Leegao `c4755eef`, SHA-256 `fcefa3fa...434f8d2` |
| Política BCn | ETC2, no ASTC | compute completo, ETC2 y flags de wrapper/caché | ETC2 explícito, ASTC desactivado, sin flags Fcharan |
| Ubicación de la capa BCn | Capa Android externa y shim durante la prueba histórica | Asset extraído al rootfs | A: rootfs; B: capa Android externa con el shim histórico |
| Resolución | 1280x720 | 1280x720 | 1280x720 |
| Box64/audio | 0.4.0, `INTERMEDIATE`, ALSA | Igual | Igual |
| CPU | 0–7 | 0–7 efectivo en el Pixel | Selección automática que resolvió 0–7 en v43 |
| Payload | Árbol directo usado por la publicación v29 | 815 archivos, 5847372363 bytes | Debe conservar el mismo marcador mediante actualización base-only |

## Artefactos recuperados

| Artefacto | Origen | SHA-256 |
|---|---|---|
| `bcn-leegao.tzst` | The412Banner/winlator-contents, `wrappers-v1` | `6ae12eacfe5d228e588569a51e28d9f65b54f7988d6aca835f7dc864636c41fb` |
| `libbcn_layer.so` dentro del asset | Leegao shader-v3, revisión `c4755eef` indicada por el paquete | `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2` |
| `dxvk-sarek-v1.13.0.wcp` | The412Banner/Nightlies | `7e792940c6ca9793ce9fb61aa8684b4fad7b72a207e84eb07b5f0edd95f41ba7` |
| `dxvk-1.13.0-sarek.tzst` normalizado | Generado desde los directorios `system32` y `syswow64` del WCP | `94ccf1062ccaccd1411db708f026072e37b33fe686c6e76731e81fc67902a968` |

La huella de `libbcn_layer.so` coincide exactamente con la restauración final registrada en `EXEC-020`. El shim Android histórico tenía SHA-256 `053b2815...d565`. La variante A no lo usó para separar el efecto de los binarios del efecto de la ubicación; la variante B restauró también ese shim.

## Criterios de aceptación

- Contenido del juego visible en una captura; fondo negro con cursor no aprueba.
- `Cuphead.exe` vivo y sin nuevo `LOW_MEMORY` durante al menos 90 s.
- Memoria del proceso Android y del proceso Windows registrada en un punto comparable.
- Marcador directo intacto y ausencia de una segunda copia del payload.
- Perfil Adreno sin cambios.

## Matriz de resultados

| Criterio | Resultado | Evidencia |
|---|---|---|
| Compilación v44 | Aprobada con JDK 17; JDK 21 reprodujo un fallo de R8 | [build.md](./logs/build.md) |
| Instalación base-only | Aprobada como actualización; `versionCode=44` | [build.md](./logs/build.md) |
| Variante A: BCn dentro del rootfs | Imagen visible, pero cierre por `LOW_MEMORY` a las 22:17:57.081, antes de 90 s | [rootfs-result.md](./logs/rootfs-result.md), [captura](./evidencias/pixel-v44-rootfs-30s.png) |
| Variante B: BCn como capa Android | Imagen visible en dos arranques y carga de `VK_LAYER_BCN_BCnLayer` confirmada por log | [android-layer-result.md](./logs/android-layer-result.md), [captura a 30 s](./evidencias/pixel-v44-android-layer-30s.png), [repetición](./evidencias/pixel-v44-android-layer-repeticion-45s.png) |
| Permanencia a 90 s | Aprobada en B: `com.cuphead` y `Cuphead.exe` vivos; sin nuevo `LOW_MEMORY` | [captura posterior](./evidencias/pixel-v44-android-layer-90s.png), [android-layer-result.md](./logs/android-layer-result.md) |
| Memoria | A falla con PSS combinado aproximado de 2742906 KiB a los 30–40 s; B estabiliza `ION_heap` alrededor de 1324 MiB y conserva aproximadamente 1,28–1,32 GiB disponibles durante doce muestras | [rootfs-result.md](./logs/rootfs-result.md), [android-layer-result.md](./logs/android-layer-result.md) |
| Datos directos | Un solo `Cuphead.exe`, árbol observado de 5847511447 bytes y staging `local_testing` ausente | [android-layer-result.md](./logs/android-layer-result.md) |

## Observación

La combinación DXVK-Sarek 1.13.0 + Leegao BCn ETC2 recuperó la imagen tanto dentro del rootfs como mediante la capa Android externa. Sin embargo, solo la segunda ruta cumplió la ventana de permanencia: la integración rootfs agotó la memoria y Android la cerró. En la ruta Android, el cargador registró explícitamente la capa histórica, `ION_heap` dejó de crecer y el título se mantuvo visible.

## Interpretación

El resultado confirma que la regresión no se explica solo por resolución o potencia del Pixel. La versión de DXVK y el binario BCn importan para recuperar el render, pero la ubicación y forma de carga de BCn también cambian de manera material el consumo de memoria. La coincidencia con el perfil histórico no se obtiene instalando los mismos binarios en cualquier ruta.

## Decisión

- Rechazar para Pixel la integración BCn dentro del rootfs, incluso con los binarios históricos.
- Conservar DXVK-Sarek 1.13.0, Leegao BCn ETC2 y la ruta de capa Android como referencia funcional del Pixel.
- No publicar todavía v44 como solución autónoma: la variante aprobada depende de ajustes ADB globales de depuración GPU.
- Mantener una sola publicación universal; el selector continúa eligiendo Vortek para Mali y Turnip para Adreno. Turnip no es intercambiable con la GPU del Pixel.

## Pendientes

- Integrar la capa Android sin comandos manuales ni permiso `WRITE_SECURE_SETTINGS`, o sustituirla por un mecanismo equivalente dentro del cargador gráfico.
- Repetir desde una instalación limpia para validar creación del contenedor y conservación del almacenamiento directo.
- Realizar una sesión de juego prolongada con control y registrar FPS/frame time; esta ejecución no valida controles por ADB ni gameplay completo.

## Relaciones

- Antecedente estable: [EXEC-020](../20-comparacion-graficos-pixel-tensor-mali/matriz.md)
- Regresión reciente: [EXEC-029](../29-pantalla-negra-dxvk241-pixel/matriz.md)
- Limitación de fidelidad aceptada: [limitación 14](../../limitaciones/14-fidelidad-texturas-pixel-tensor-mali.md)
- Pantalla negra: [limitación 26](../../limitaciones/26-pantalla-negra-dxvk241-pixel.md)
- Presión de memoria: [limitación 23](../../limitaciones/23-pixel-low-memory-metrica-20260918.md)
