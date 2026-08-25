# Limitación 07: el instalador de Cuphead no avanza en Wine

- **Proyecto:** Win2APK
- **Estado:** detectada
- **Fecha de registro:** 2026-08-24

## Descripción

La instalación controlada de Cuphead mediante `setup.exe` no completó la descompresión de los archivos del juego dentro de un prefijo Wine temporal. El instalador creó la carpeta de destino y algunos archivos auxiliares, pero quedó procesando indefinidamente el primer volumen auxiliar sin producir la publicación final.

## Contexto técnico

- Instalador: `cuphead/setup.exe`, Inno Setup 5.5.0.1.
- Datos disponibles: `fg-01.bin`, `fg-02.bin`, `fg-03.bin` y `fg-04.bin`.
- Wine utilizado: `wine-11.0` de `nixpkgs#wineWow64Packages.stable`.
- Arquitectura del prefijo: `win64`.
- Prefijo: `/tmp/win2apk-cuphead-exec010-20260824`.
- Pantalla: `DISPLAY=:0`.
- Dispositivo Android, Winlator y APK: N/A en este intento.

## Reproducción o evidencia

Se ejecutó el instalador desde la carpeta `cuphead` con:

```text
wine setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LANG=english /DIR=C:\Cuphead
```

Después de más de once minutos se observó:

- el proceso `setup.tmp` permanecía en estado de ejecución con aproximadamente 102 % de CPU;
- el descriptor del archivo `fg-04.bin` permanecía en el desplazamiento `31`;
- `C:\Cuphead\01.fgpack.x2` permanecía en `0` bytes;
- la carpeta instalada solo contenía `unins000.exe`, `unins000.dat`, `_Redist` y el archivo temporal `01.fgpack.x2`;
- el prefijo ocupaba aproximadamente `1016M`;
- no se mostró un mensaje de error del instalador.

El intento se interrumpió de forma controlada con código de la sesión `58` y se detuvieron los procesos restantes únicamente dentro del prefijo temporal mediante `wineserver -k`.

## Impacto

No se obtuvo todavía una carpeta instalada válida, por lo que no es posible confirmar el ejecutable principal, medir la publicación final, empaquetar `cuphead.tzst` ni generar el APK de Cuphead.

## Análisis técnico

La evidencia demuestra que el proceso no estaba esperando una interacción visible: consumía CPU y no avanzaba en la lectura del volumen ni en la escritura del archivo temporal. La causa exacta no está confirmada. La hipótesis actual es una incompatibilidad entre Wine 11.0 en modo WoW64 y la rutina de descompresión personalizada incluida por el repack; debe verificarse con otra versión o con una instalación nativa de Windows.

## Solución aplicada

No se aplicó una solución. Se conservó el prefijo temporal para inspección y se evitó modificar el Wine del usuario.

## Resultado

La instalación controlada no fue reproducible en este entorno. La estructura parcial confirma que el instalador acepta el destino `C:\Cuphead`, pero no demuestra que el juego haya sido instalado.

## Evidencia posterior

La ejecución independiente [EXEC-011](../ejecuciones/11-instalacion-cuphead-lutris/matriz.md) completó el mismo instalador en el prefijo `/home/julian/Games/cuphead` usando UMU con `GE-Proton11-5-x86_64`, y el primer inicio visible de `Cuphead.exe` fue positivo. Esto cambia el alcance de la limitación: el fallo de este informe permanece válido para el entorno Wine 11.0 temporal y no se generaliza a todos los runners.

## Limitaciones pendientes

- Probar la instalación con el Wine que el usuario tiene instalado fuera de este entorno, si está disponible en una ruta accesible.
- Probar una versión de Wine con soporte WoW64 diferente o un prefijo de 32 bits si el ejecutable del juego lo requiere.
- Como alternativa, instalar la copia legal en Windows y entregar a Win2APK la carpeta ya instalada.
- No continuar con el empaquetado hasta confirmar el ejecutable y una ejecución básica del juego.

## Referencias

- [Guía de trabajo del repositorio](../AGENTS.md)
- [Guía de ejecuciones](../ejecuciones/AGENTS.md)
- [Configuración actual de Win2APK](../config/win2apk.json)

## Ejecuciones asociadas

- [EXEC-010: instalación controlada de Cuphead mediante Wine](../ejecuciones/10-instalacion-cuphead-wine/matriz.md)
- [EXEC-011: instalación visible de Cuphead mediante Lutris](../ejecuciones/11-instalacion-cuphead-lutris/matriz.md)
