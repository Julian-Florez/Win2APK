# Registro de observación — EXEC-011

## Observación inicial

- El instalador visible es `/home/julian/Tesis/Win2APK/cuphead/setup.exe`.
- Lutris utiliza el prefijo `/home/julian/Games/cuphead`.
- El runner observado es `GE-Proton11-5-x86_64` mediante UMU y pressure-vessel.
- El destino seleccionado es `C:\Program Files\Cuphead`, cuya ruta Linux es `/home/julian/Games/cuphead/drive_c/Program Files/Cuphead`.
- Se observó `setup.tmp` y posteriormente `CLS-srep_x64.exe` consumiendo CPU, por lo que la descompresión está activa.
- El destino llegó a aproximadamente 2,58 GB en una muestra y luego redujo su tamaño al eliminar temporales intermedios.
- Apareció `Cuphead_Data/StreamingAssets/AssetBundles` con archivos de contenido, pero todavía no se ha confirmado `Cuphead.exe`.
- La presencia de `srep-virtual-memory.tmp`, `freearc*.tmp` y paquetes `.fgpack` corresponde a trabajo temporal del instalador mientras la instalación continúa.

## Resultado final

- Después de pulsar `Finish`, no quedaron procesos `setup.exe`, `setup.tmp`, `CLS-srep_x64.exe` ni `unarc` activos.
- La carpeta final `/home/julian/Games/cuphead/drive_c/Program Files/Cuphead` ocupa aproximadamente `5,5G` según `du`.
- Se confirmó `Cuphead.exe` de `650752` bytes y el directorio `Cuphead_Data`.
- También se encontraron `UnityPlayer.dll`, `Galaxy64.dll`, `GalaxyPeer64.dll` y `GalaxyCSharpGlue.dll`.
- No quedaron archivos `*.tmp`, `*.fgpack` ni `*.fgpack.x2` en el destino final.
- `_Redist` contiene `dxwebsetup.exe`, `QuickSFV.EXE`, `fitgirl.md5` y `QuickSFV.ini`; no se observó un instalador de Visual C++ en esa carpeta.
- El registro Wine contiene la entrada de desinstalación `Cuphead_is1`, con `InstallLocation` en `C:\Program Files\Cuphead`.
- El instalador registró la capa de compatibilidad `RUNASADMIN` para `C:\Program Files\Cuphead\Cuphead.exe`.
- Hash SHA-256 observado de `Cuphead.exe`: `c5fffd221234ea520b9b5d545d9fff65eba497a0ce1b852334d293770d7ee02d`.
- Hash SHA-256 observado de `UnityPlayer.dll`: `598135e374441121d797689f6864f44b07d13c9deef0a8b1c40d7d2537399e11`.

## Primer inicio visible

- Lutris ejecutó `C:\Program Files\Cuphead\Cuphead.exe` con UMU y `GE-Proton11-5-x86_64`.
- El proceso permaneció activo durante la observación.
- `output_log.txt` registró Unity `2017.4.9f1`, Direct3D 11.0, GPU `NVIDIA GeForce RTX 2050` y versión de juego `1.3.4`.
- El log registra inicialización de input, XInput y Galaxy SDK. No se observó cierre fatal.
- El primer inicio creó cachés de DXVK/GLCache y el archivo `AppData/LocalLow/Studio MDHR/Cuphead/output_log.txt` fuera de la carpeta de publicación.

## Criterio para el asset

Para el primer asset se conservará el contenido de la publicación y se excluirán auxiliares de instalación que no son necesarios para ejecutar el juego en Winlator: `_Redist/`, `unins000.exe`, `unins000.dat` y los archivos `goggame-*`. La exclusión se hará al crear el archivo comprimido, sin borrar elementos del prefijo instalado.

## Interpretación

La ruta y el prefijo tienen permisos suficientes para escribir. La segunda ejecución superó la fase en la que quedó detenida la primera prueba y dejó una estructura de publicación Unity completa. La ejecución del juego todavía no se ha probado en este registro.

## Decisión provisional

No se modificó la carpeta después de finalizar el instalador. La carpeta es candidata para empaquetado y el primer inicio visible fue positivo en este equipo/runner; esto no demuestra compatibilidad universal con Android o Winlator.

## Evidencia adicional

Las muestras de proceso y tamaño se conservaron en la conversación de Codex; no se ha exportado todavía una captura ni un log de Lutris.
