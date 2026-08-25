# Ejecución 14: AAB segmentado de Cuphead instalado con bundletool

- **ID:** `EXEC-014`
- **Fecha:** 2026-08-24
- **Tipo:** prueba de distribución AAB/PAD y ejecución en dispositivo
- **Resultado general:** Aprobado experimentalmente: AAB convertido, instalado y ejecutado
- **Método:** `bundletool build-apks --local-testing` seguido de `bundletool install-apks`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | `config/win2apk.json` |
| AAB | `winlator/app/app/build/outputs/bundle/debug/app-debug.aab` | `bundleDebug` terminado |
| Tamaño del AAB | `5.043.469.401` bytes | Medición local |
| Asset packs | `cuphead_data_01`, `cuphead_data_02`, `cuphead_data_03` | `install-time` |
| Partes | 1.800.000.000 + 1.800.000.000 + 1.182.573.186 bytes | Concatenación validada |
| SHA-256 reconstruido | `33aad774c30e07be8088160d35bacdd191eae7d06ed0fd507f396c726d7eff93` | Igual al asset original |
| APK set local | `winlator/app/build/cuphead-lenovo-segmented.apks` | `5.050.689.275` bytes |
| Bundletool | `1.18.3` | JAR local; SHA-256 `a099cfa1543f55593bc2ed16a70a7c67fe54b1747bb7301f37fdfd6d91028e29` |
| Dispositivo | Lenovo TB-J606F, `HA1QXMW2` | API 36; almacenamiento suficiente durante la prueba |
| Paquete instalado | `com.cuphead` | `versionCode=28`, `versionName=11.1-core` |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | AAB con los tres asset packs | Aprobado | 3 módulos | `bundleDebug` | [build](./logs/build.md) | Cada pack queda por debajo de 2 GB |
| M-02 | Generación de APK set local | Aprobado | 1 `.apks` | bundletool 1.18.3, `--local-testing`, Lenovo | [bundletool](./logs/bundletool.md) | Superó el fallo del pack único |
| M-03 | Instalación con bundletool | Aprobado | `com.cuphead` | `install-apks --device-id=HA1QXMW2` | [bundletool](./logs/bundletool.md) | Se instalaron base, configuración y los tres splits PAD |
| M-04 | Extracción del payload | Aprobado | 804 archivos; `Cuphead.exe` de 650.752 bytes | Primera ejecución Core | [runtime](./logs/runtime.md) | `du` reportó aproximadamente 5,4 GiB en la carpeta Cuphead |
| M-05 | Arranque de Cuphead.exe | Aprobado experimentalmente | Proceso activo y Unity inicializado | `XServerDisplayActivity` | [runtime](./logs/runtime.md) | Se confirmó Direct3D 11, Turnip Adreno 610 e input táctil |
| M-06 | Imagen de juego | Parcial | Pantalla inicial marrón sin menú legible | Captura durante ejecución | [captura](./evidencias/cuphead-game-menu.png) | No declarar una sesión de juego completa |
| M-07 | Detención controlada | Aprobado | Procesos Wine/Cuphead ausentes tras `force-stop` | Fin de prueba | [runtime](./logs/runtime.md) | El paquete permaneció instalado |

## Observación, interpretación y decisión

La distribución segmentada resolvió el fallo de `build-apks` del asset pack único. Los tres splits `cuphead_data_*` aparecen en `pm path com.cuphead`, y la primera ejecución reconstruyó el stream Zstandard a través del `AssetManager` antes de extraerlo al prefijo.

El ejecutable se inició mediante Box64/Wine y Unity registró la carga de Cuphead, pero la captura solo muestra el fondo de la escena inicial. Se considera validado el empaquetado, instalación, extracción y arranque del proceso; la jugabilidad y la interacción prolongada quedan pendientes.

## Evidencias

- [Log de compilación](./logs/build.md)
- [Log de bundletool e instalación](./logs/bundletool.md)
- [Log de ejecución Android/Unity](./logs/runtime.md)
- [Captura durante la ejecución](./evidencias/cuphead-game-menu.png)
