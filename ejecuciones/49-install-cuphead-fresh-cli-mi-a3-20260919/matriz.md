# EXEC-049 — Instalación `--fresh` de Cuphead mediante el CLI en Mi A3

- **ID:** `EXEC-049`
- **Fecha:** 2026-09-19
- **Tipo:** instalación automatizada / repetición válida
- **Resultado general:** aprobado experimentalmente para instalación, transferencia directa y arranque del ejecutable
- **Método:** instalación desde cero con `win2apk install --fresh`, `bundletool` 1.18.3 y lanzamiento posterior mediante ADB.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead empaquetado por Win2APK | Archivo `.apks` usado por el CLI |
| Versión | `11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core` | `dumpsys package` |
| Ejecutable | `Cuphead.exe` | Log de `WinlatorProcess` y proceso ADB |
| Publicación/hash | N/R | No se registró hash en esta prueba |
| Método | `win2apk install ... --fresh` | Comando reproducible en log |
| Entorno | Linux; `WIN2APK_BUNDLETOOL=/tmp/bundletool-all-1.18.3.jar` | Comando ejecutado |
| Versión de Winlator | N/R | El perfil se identificó desde los logs de la aplicación |
| Contenedor/configuración | `Adreno / Turnip + Gladio / DXVK`; `graphicsDriver=turnip,gladio`; `dxwrapper=dxvk` | `Win2APKGraphicsProfile` |
| Dispositivo/variante | Xiaomi Mi A3, serial `51c803a01206` | ADB |
| Android/API | Android 16 / API 36 | `getprop` |
| ABI | `arm64-v8a` principal | `getprop` y splits instalados |
| Resolución | 720x1560, densidad 320 | `wm size`, `wm density` |
| Fecha y hora de inicio | N/R | El inicio exacto del segundo comando no se capturó |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación | Aprobado | Código de salida `0` | Se solicitó `--fresh`; el CLI informó desinstalación y reinstalación | [log CLI](./logs/01-cli-install-fresh-valid.log) |  |
| M-02 | Primer inicio | Aprobado | `MainActivity` en 0.569 s desde el lanzamiento observado | Lanzamiento con `adb shell monkey` | [log de arranque](./logs/02-launch-and-runtime.log) | El tiempo se refiere a la actividad Android, no al primer frame del juego |
| M-03 | Aperturas posteriores | N/R | N/R | No se realizó un segundo lanzamiento independiente | N/A |  |
| M-04 | Operación básica | Aprobado experimentalmente | `XServerDisplayActivity` visible; `Cuphead.exe` activo | Usuario confirmó que la aplicación funcionó; el proceso permaneció vivo en el corte | [log de arranque](./logs/02-launch-and-runtime.log) | No se midió FPS ni se documentó interacción de menú |
| M-05 | Aislamiento de archivos | Aprobado | 5 paquetes fuente eliminados; `local_testing` eliminado | Después del movimiento transaccional | [log de arranque](./logs/02-launch-and-runtime.log) | La copia final queda en el árbol privado de la aplicación |
| M-06 | Persistencia de archivos | Aprobado en el corte | 815 archivos, 5.847.372.363 bytes transferidos | El proceso del juego siguió activo después de la limpieza | [log de arranque](./logs/02-launch-and-runtime.log) | No se hizo relanzamiento posterior |
| M-07 | Tamaño del APK | N/R | N/R | No se midió el artefacto local | N/A |  |
| M-08 | Tiempo de instalación | N/R | N/R | El inicio exacto del comando no quedó registrado | N/A | No inferirlo desde `firstInstallTime` |
| M-09 | Tiempo de primer inicio | Parcial | `+569 ms` hasta `MainActivity`; `+292 ms` hasta `XServerDisplayActivity` tras la preparación | Tiempos reportados por `ActivityTaskManager` | [log de arranque](./logs/02-launch-and-runtime.log) | No equivale al tiempo total hasta el primer frame jugable |
| M-10 | Tiempo de aperturas posteriores | N/A | N/A | No se realizó una apertura posterior | N/A |  |
| M-11 | Tasa de éxito | N/A | N/A | Una sola repetición válida; no calcular tasa | N/A |  |
| M-12 | Pasos manuales | Aprobado | Conectar ADB y ejecutar un comando CLI | No se requirió copiar la carpeta ni intervenir en asset packs | [log CLI](./logs/01-cli-install-fresh-valid.log) |  |

## Transferencia y almacenamiento

La instalación inicializó cinco paquetes on-demand. La aplicación registró la descarga completa de cada uno, movió el contenido a su ubicación final y confirmó la eliminación de los paquetes fuente:

- `win2apk_payload_001`: 1.346.611.571 bytes
- `win2apk_payload_002`: 1.346.682.735 bytes
- `win2apk_payload_003`: 1.346.703.032 bytes
- `win2apk_payload_004`: 1.347.153.355 bytes
- `win2apk_payload_005`: 460.491.613 bytes
- Total registrado por la transacción: 5.847.372.363 bytes en 815 archivos.

## Fallos, advertencias y decisiones

- **Advertencia exacta:** `run-as: package not debuggable: com.cuphead` al intentar limpiar `splitcompat`.
- **Interpretación:** la limpieza específica de `splitcompat` no pudo usar `run-as` porque el APK es release/no-debuggable; el propio instalador continuó y reportó instalación correcta. No impidió la transferencia directa ni la eliminación de los cinco paquetes fuente en esta prueba.
- **Mensajes SELinux:** hubo denegaciones `ioctl` sobre directorios privados durante la ejecución; también se observaron concesiones `execute`. No produjeron la terminación de `Cuphead.exe` en el corte y no se convierten en una afirmación de compatibilidad universal.
- **Decisión:** aceptar esta ruta como la candidata actual para distribución en el Mi A3 y conservar la advertencia como condición conocida para futuras pruebas release.

## Evidencias

- [Instalación válida](./logs/01-cli-install-fresh-valid.log)
- [Arranque, transferencia, limpieza y procesos](./logs/02-launch-and-runtime.log)
- Captura: N/A

## Repetibilidad y pendientes

- [x] Ejecutar la instalación con `--fresh` sobre un paquete previamente instalado.
- [x] Confirmar la transferencia y limpieza de los paquetes fuente.
- [x] Confirmar que `Cuphead.exe` queda activo.
- [ ] Medir el tiempo completo desde el envío del `.apks` hasta el primer frame.
- [ ] Repetir en Redmi, Xiaomi/Lenovo y Pixel con el mismo artefacto.
- [ ] Medir el tamaño ocupado antes y después con un método que pueda acceder al almacenamiento privado.
