# Ejecución 16: retiro de splits de Cuphead después de la extracción

- **ID:** `EXEC-016`
- **Fecha:** 2026-08-24
- **Tipo:** prueba controlada de almacenamiento y relanzamiento
- **Resultado general:** parcial; se liberaron los splits, pero la implementación instalada volvió a exigirlos
- **Método:** retiro individual mediante Package Manager, sin borrar directamente `/data/app`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | Paquete `com.cuphead` |
| Versión | `11.1-core` | `dumpsys package` |
| Ejecutable | `Cuphead.exe` | Copia extraída de `EXEC-015` |
| Publicación/hash | APK set diagnóstico de `EXEC-015`; hash N/R | Instalación existente |
| Método | `pm uninstall --user 0 com.cuphead <split>` | Un split por operación |
| Entorno | Winlator Core + PAD `install-time` | Tres packs segmentados |
| Dispositivo/variante | Lenovo TB-J606F, serial `HA1QXMW2` | Dispositivo físico |
| Android/API | API 36 | `getprop ro.build.version.sdk` |
| ABI | `arm64-v8a, armeabi-v7a, armeabi` | `getprop ro.product.cpu.abilist` |
| Resolución | `1200x2000` física | `wm size` |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Retirar un asset-pack split sin desinstalar la base | Aprobado | `Success` | Package Manager | [registro](./logs/retiro-splits.md) | No se usó `rm` sobre `/data/app` |
| M-02 | Retirar los tres splits | Aprobado | 3/3 | Operaciones consecutivas | [registro](./logs/retiro-splits.md) | Permanecieron base y splits de configuración |
| M-03 | Reducir el código instalado | Aprobado | `5.056.035.328` a `268.724.736` bytes | Medición de almacenamiento del paquete | [registro](./logs/retiro-splits.md) | Diferencia: `4.787.310.592` bytes |
| M-04 | Conservar la extracción | Aprobado | rootfs `6.732.318` KiB; Cuphead `5.715.382` KiB | `run-as com.cuphead` | [registro](./logs/retiro-splits.md) | Se observaron 804 archivos de Cuphead |
| M-05 | Relanzar sin packs | Fallido | 0/1 | Tres splits ya retirados | [registro](./logs/retiro-splits.md) | La versión instalada intentó extraer otra vez |
| M-06 | Mantener instalado el paquete base | Aprobado | 1 paquete | Después del retiro | [registro](./logs/retiro-splits.md) | `com.cuphead` permaneció instalado |

## Observación, interpretación y decisión

Android permitió retirar los tres splits y conservó los datos privados extraídos. El relanzamiento mostró `Unable to create the configured container or shortcut.` y el diagnóstico informó `location=null` para los tres packs.

La observación demuestra que la segunda copia se puede liberar, pero no que una aplicación ordinaria pueda retirar por sí misma packs `install-time`. También demuestra que Winlator necesita un marcador transaccional para reconocer una extracción terminada. Se decidió probar PAD `on-demand`, su API `removePack()` y el marcador en [EXEC-017](../17-pad-ondemand-limpieza-cuphead-mi-a3/matriz.md).

## Fallos y decisiones

- **Limitación relacionada:** [Limitación 12](../../limitaciones/12-retiro-splits-install-time-no-autonomo.md)
- **Mensaje exacto:** `Unable to create the configured container or shortcut.`
- **Decisión:** no adoptar el comando `pm` como flujo final; conservarlo como evidencia y recuperación asistida.

