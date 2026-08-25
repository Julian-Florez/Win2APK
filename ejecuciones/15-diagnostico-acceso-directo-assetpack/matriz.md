# Ejecución 15: diagnóstico de acceso directo a asset packs

- **ID:** `EXEC-015`
- **Fecha:** 2026-08-24
- **Tipo:** diagnóstico AAB/PAD y regresión de ejecución
- **Resultado general:** No-go para acceso directo por ruta en bundletool; fallback de extracción aprobado
- **Rama:** `codex/direct-assetpack-cuphead`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | `config/win2apk.json` |
| Cambio bajo prueba | `AssetPackDiagnostics` + Play Asset Delivery `2.3.0` | Rama de trabajo |
| AAB | `winlator/app/app/build/outputs/bundle/debug/app-debug.aab` | `bundleDebug` exitoso |
| APK set | `winlator/app/build/cuphead-direct-diagnostic.apks` | `5.051.038.271` bytes |
| Bundletool | `1.18.3` | `--local-testing --connected-device` |
| Dispositivo | Lenovo TB-J606F, `HA1QXMW2` | API 36, ABI `arm64-v8a` |
| Instalación | Limpia | Se desinstaló `com.cuphead` antes de `install-apks` |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Evidencia | Observaciones |
|---|---|---|---|---|---|
| M-01 | Compilación con Play Asset Delivery | Aprobado | `BUILD SUCCESSFUL`, 43 tareas | [build](./logs/build.md) | Se añadió la biblioteca de diagnóstico |
| M-02 | Generación del APK set | Aprobado | 1 `.apks` | [bundletool](./logs/bundletool.md) | Los tres packs se firmaron y empaquetaron |
| M-03 | Instalación limpia con bundletool | Aprobado | `com.cuphead` | [bundletool](./logs/bundletool.md) | Se instalaron los splits base y PAD |
| M-04 | Ruta directa `assetsPath` | No-go | `null` en los 3 packs | [diagnóstico](./logs/diagnostico.md) | `storageMethod=1`, sin carpeta POSIX |
| M-05 | Fallback de extracción | Aprobado | 804 archivos, `Cuphead.exe` 650.752 bytes | [regresión](./logs/regresion.md) | El cambio no rompió la variante funcional |
| M-06 | Arranque del juego | Aprobado experimentalmente | Proceso `Cuphead.exe` activo | [regresión](./logs/regresion.md) | Unity/Direct3D 11/Turnip/input táctil inicializados |

## Observación e interpretación

Los tres packs devolvieron `storageMethod=1`, `path=null` y `assetsPath=null`. En esta instalación local, los datos están montados como APK assets y solo están disponibles mediante `AssetManager`; no existe una carpeta que Winlator pueda enlazar directamente a `C:\Cuphead`.

La variante existente siguió extrayendo el stream segmentado y arrancó Cuphead. Por tanto, el diagnóstico valida el límite técnico sin convertirlo en un fallo del juego ni del dispositivo.

## Decisión

No implementar enlaces directos basados únicamente en `AssetPackLocation.assetsPath()`. El siguiente intento requeriría una capa virtual de archivos para APK assets o un mecanismo de almacenamiento PAD que entregue `STORAGE_FILES`; ambas alternativas quedan separadas del fallback funcional.
