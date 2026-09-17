# Probe reducido de `STORAGE_FILES` en Redmi

- **Versión de plantilla:** 1.0
- **ID:** `EXEC-019`
- **Fecha:** `2026-08-24`
- **Tipo:** automatizada
- **Resultado general:** aprobado
- **Método:** AAB debug local con un pack on-demand sintético (`probe_assets`). La app solicitó el pack mediante Play Asset Delivery, obtuvo `AssetPackLocation`, y ejecutó dos ciclos ida/vuelta: `Files.move` seguido de `Os.rename`, y `Os.rename` seguido de `Files.move`. El archivo fue restaurado al origen al finalizar.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | StorageFiles Probe (`com.win2apk.storageprobe`) | App aislada creada para esta ejecución |
| Versión | `1.0-probe`, versionCode `1` | `dumpsys package` |
| Ejecutable | N/A | No se ejecutó software Windows |
| Publicación/hash | Debug local; AAB SHA-256 `f19d0ee762fdd463f8c3eb3174f5345644dd91a53ce012f1c289ac095df2a58d` | [artefactos](./logs/artefactos.md) |
| Método | `bundletool 1.18.3 install-apks --local-testing` | Instalación local con `--device-id=16f88243` |
| Entorno | Android Gradle Plugin 7.2.2, Gradle 7.3.3, JDK 17 | Build reproducible en `/tmp/win2apk-storagefiles-probe` |
| Versión de Winlator | N/A | Probe independiente |
| Contenedor/configuración | N/A | No se creó contenedor |
| Dispositivo/variante | Redmi Note 8, `Xiaomi/infinity_ginkgo/ginkgo` | Serial exclusivo `16f88243` |
| Android/API | Android 16 / API 36 | `getprop ro.build.version.sdk` |
| ABI | `arm64-v8a,armeabi-v7a,armeabi` | `getprop ro.product.cpu.abilist` |
| Resolución | 1080x2340 | `wm size` |
| Fecha y hora de inicio | `2026-08-24 23:21:48` hora local del logcat | [logcat](./logs/logcat-storagefilesprobe.txt) |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación | Aprobado | Probe instalado con base/config; pack on-demand solicitado después | Sin Cuphead ni sus packs | [ejecución](./logs/ejecucion-adb-y-app.txt) | El paquete fue desinstalado al terminar |
| M-02 | Primer inicio | Aprobado | `MainActivity` visible y `fetch_complete success=true` | Redmi `16f88243` | [log](./logs/storagefiles-probe.log) | El pack pasó de `NOT_INSTALLED` a `COMPLETED` |
| M-03 | Aperturas posteriores | N/A | N/A | No era objetivo | N/A | |
| M-04 | Operación básica | Aprobado | Dos ciclos de movimiento y restauración | Archivo sintético de 698 bytes | [log](./logs/storagefiles-probe.log) | `Files.move` y `Os.rename` completaron sin error |
| M-05 | Aislamiento de archivos | Aprobado | `storage_method=0`, `assets_path` no nulo | `AssetPackLocation` entregó ruta de almacenamiento | [log](./logs/storagefiles-probe.log) | Interpretado como `STORAGE_FILES`; no fue `APK_ASSETS` |
| M-06 | Persistencia de archivos | Aprobado | Origen restaurado; destino ausente | `source_exists=true moved_exists=false` | [log](./logs/storagefiles-probe.log) | Se verificó tras ambos ciclos |
| M-07 | Tamaño del APK | N/A | AAB 2,342,774 bytes; APKS 3,082,620 bytes | El criterio pide APK individual | [artefactos](./logs/artefactos.md) | No se reporta APK individual como tamaño del AAB |
| M-08 | Tiempo de instalación | N/R | N/R | No se midió con cronómetro | [baseline](./logs/baseline-adb.txt) | |
| M-09 | Tiempo de primer inicio | N/R | N/R | Se esperó 20 s; no se midió intervalo exacto | [ejecución](./logs/ejecucion-adb-y-app.txt) | Pack completado dentro de la ventana observada |
| M-10 | Tiempo de aperturas posteriores | N/A | N/A | No era objetivo | N/A | |
| M-11 | Tasa de éxito | Aprobado | 2/2 ciclos de movimiento; 2/2 restauraciones | Un único dispositivo, un payload | [log](./logs/storagefiles-probe.log) | No implica compatibilidad universal |
| M-12 | Pasos manuales | Aprobado | 0 pasos en el dispositivo después de `install-apks` | Arranque automatizado por ADB | [ejecución](./logs/ejecucion-adb-y-app.txt) | |

## Métricas por dispositivo

| Dispositivo | Instalación | Primer inicio | Segundo inicio | Operación | Persistencia | Tamaño APK | Tiempos | Tasa de éxito | Pasos manuales |
|---|---|---|---|---|---|---|---|---|---|
| Redmi Note 8 `16f88243` | Aprobada | Aprobado | N/A | Aprobada | Aprobada | N/A | N/R | 2/2 ciclos | 0 |

## Mediciones del almacenamiento y seguridad

| Medición | Antes | Después de la prueba | Fuente |
|---|---:|---:|---|
| `/data` usado | 48,872,624 KiB | 48,878,860 KiB antes de limpiar el probe; 48,874,996 KiB tras desinstalarlo | [baseline](./logs/baseline-adb.txt), [final](./logs/final-adb.txt) |
| `/data` disponible | 2,448,188 KiB | 2,441,952 KiB antes de limpiar; 2,447,616 KiB tras limpiar | Mismos logs |
| Payload | N/A | 698 bytes | [artefactos](./logs/artefactos.md) |
| `st_dev` origen/destino | `66359` / `66359` | `66359` / `66359` | [log](./logs/storagefiles-probe.log) |
| `st_ino` origen/destino | `114867` / `114867` | `114867` / `114867` | [log](./logs/storagefiles-probe.log) |
| Tamaño tras mover/restaurar | 698 bytes | 698 bytes | [log](./logs/storagefiles-probe.log) |
| SHA-256 tras mover/restaurar | `cabc6f6e...06ed30` | `cabc6f6e...06ed30` | [log](./logs/storagefiles-probe.log) |
| SELinux | `Enforcing`; `u:object_r:app_data_file:s0:c132,c257,c512,c768` en origen y `filesDir` | Igual durante la prueba | [log](./logs/storagefiles-probe.log), [ADB](./logs/final-adb.txt) |
| errno | N/A | No se produjo excepción; no hubo errno que registrar | [log](./logs/storagefiles-probe.log) |

## Fallos y decisiones

- **Limitación relacionada:** N/A.
- **Mensaje exacto:** N/A para las operaciones de movimiento; no hubo `ErrnoException` ni denegación SELinux de la app.
- **Decisión:** El mecanismo de mover un archivo desde una ubicación `STORAGE_FILES` a `filesDir` es técnicamente viable en este Redmi y, en esta ejecución, se comportó como rename en el mismo filesystem: inode y bytes permanecieron iguales. Esto no demuestra por sí solo que todos los árboles de un asset pack puedan moverse con las mismas garantías.

## Evidencias

- [Payload sintético](./evidencias/payload-sintetico.txt)
- [Log de la app](./logs/storagefiles-probe.log)
- [Logcat filtrado](./logs/logcat-storagefilesprobe.txt)
- [Mediciones ADB finales](./logs/final-adb.txt)
- [Ejecución ADB y estados PAD](./logs/ejecucion-adb-y-app.txt)
- [Artefactos y hashes](./logs/artefactos.md)

## Repetibilidad y pendientes

- [x] Verificar `STORAGE_FILES` con `assetsPath` no nulo.
- [x] Verificar `Files.move` y `Os.rename` en ambos sentidos.
- [x] Confirmar inode, bytes, SHA-256, `st_dev`, SELinux y `df`.
- [x] Restaurar el archivo y limpiar el probe.
- [ ] Repetir con un árbol de archivos sintético si se requiere validar directorios completos.
- [ ] Validar la estrategia con una implementación de Winlator antes de extrapolarla a Cuphead.
