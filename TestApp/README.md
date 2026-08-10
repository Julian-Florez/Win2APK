# Win2APK Test

Aplicación Windows mínima definida en `../especificaciones/app-minima.md`.

## Comportamiento

- Al iniciar muestra `Hola mundo`.
- El botón `Cambiar texto` alterna entre `Hola mundo` y `Texto cambiado`.
- El ciclo puede repetirse sin reiniciar la aplicación.
- Se cierra usando el control normal de cierre de la ventana.
- Es una aplicación de consola con ventana gráfica para que los fallos de inicio sean visibles en Winlator.

No usa red, archivos, base de datos, audio, video, servicios ni permisos de administrador.

## Requisitos de desarrollo

- .NET SDK 8.0 o posterior.
- Windows para compilar y ejecutar la aplicación.

El proyecto está orientado a `net8.0-windows`, Windows x64 y usa Windows Forms, que forma parte del SDK/runtime de .NET. No requiere paquetes NuGet adicionales.

## Compilación rápida

Desde esta carpeta, en Windows:

```powershell
dotnet build Win2APKTest.csproj -c Release -p:Platform=x64
```

En Windows, el ejecutable se genera en:

```text
bin/x64/Release/net8.0-windows/Win2APKTest.exe
```

## Publicación portable para Win2APK

Para generar una carpeta autocontenida que no requiere instalar .NET en el equipo destino:

```powershell
dotnet publish Win2APKTest.csproj `
  -c Release `
  -r win-x64 `
  --self-contained true `
  -p:Platform=x64 `
  -p:PublishSingleFile=true `
  -p:IncludeNativeLibrariesForSelfExtract=true `
  -o publish/win-x64
```

La carpeta `publish/win-x64` contiene `Win2APKTest.exe`, que es el ejecutable que debe entregarse a Win2APK. El resto de archivos generados son metadatos opcionales de publicación y pueden excluirse de la carpeta de entrada si el flujo de Win2APK solo requiere el ejecutable.

Para diagnosticar problemas de inicio en Winlator, es preferible publicar sin single-file:

```powershell
dotnet publish Win2APKTest.csproj `
  -c Release `
  -r win-x64 `
  --self-contained true `
  -p:Platform=x64 `
  -p:PublishSingleFile=false `
  -p:IncludeNativeLibrariesForSelfExtract=false `
  -o publish/win-x64-folder
```

En ese caso debe copiarse toda la carpeta `publish/win-x64-folder` al contenedor y ejecutarse su `Win2APKTest.exe`.

## Verificación manual

1. Ejecutar `Win2APKTest.exe`.
2. Confirmar que aparece `Hola mundo`.
3. Pulsar `Cambiar texto` diez veces consecutivas.
4. Confirmar que el texto alterna en cada pulsación y termina en `Hola mundo`.
5. Cerrar la ventana con el botón de cierre.

La aplicación no necesita instalación ni conexión a Internet.

## Ajuste de memoria para Winlator

La publicación incluye una configuración conservadora de CoreCLR: GC de estación de trabajo, GC no concurrente y un límite de heap de 128 MiB. Esto evita que CoreCLR intente reservar más memoria de la disponible en el contenedor.

Si se desea probar el ajuste directamente desde la configuración del contenedor, añade estas variables de entorno en Winlator y vuelve a ejecutar la aplicación:

```text
DOTNET_GCServer=0
DOTNET_GCConcurrent=0
DOTNET_GCHeapHardLimit=8000000
```

El valor de `DOTNET_GCHeapHardLimit` se expresa en hexadecimal; `8000000` equivale a 128 MiB. Estas opciones se leen durante el inicio del runtime, antes de que exista la ventana. [Documentación oficial de configuración del GC de .NET](https://learn.microsoft.com/en-us/dotnet/core/runtime-config/garbage-collector)

## Diagnóstico en Winlator

Ejecuta la aplicación desde una consola de Windows/Wine para conservar la salida:

```bat
cd C:\Win2APKTest
Win2APKTest.exe
```

La aplicación imprime el runtime, arquitectura, sistema operativo, directorio base y PID. También informa excepciones fatales, excepciones del hilo de interfaz, excepciones de tareas y cada pulsación del botón.

Si se cierra sin imprimir siquiera la línea `Iniciando aplicación`, el fallo ocurre antes de que .NET pueda ejecutar `Main`, normalmente en el cargador x64, Wine/Box64 o la extracción del ejecutable single-file.
