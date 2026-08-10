# Limitación 01: inicialización de CoreCLR en Winlator

- **Proyecto:** Win2APK
- **Aplicación:** Win2APK Test 0.1
- **Entorno:** Winlator sobre Android
- **Estado:** resuelta experimentalmente
- **Fecha de registro:** 2026-08-07

## Descripción

La primera publicación de `Win2APKTest.exe` no iniciaba en Winlator. El proceso terminaba sin mostrar la ventana y reportaba el siguiente error:

```text
GC heap initialization failed with error 0x8007000E
Failed to create CoreCLR, HRESULT: 0x8007000E
```

El código `0x8007000E` corresponde a `E_OUTOFMEMORY`. En este caso el error ocurría durante la inicialización del runtime .NET, antes de ejecutar el código de la ventana principal.

## Contexto técnico

La aplicación estaba publicada con estas características:

- .NET 8 para Windows.
- Windows Forms.
- Arquitectura `win-x64`.
- Publicación self-contained.
- Ejecutable single-file con extracción de librerías nativas.
- Subsistema gráfico `WinExe` en la primera versión.

La combinación de CoreCLR x64, Wine/Box64 y la publicación single-file podía requerir más memoria o espacio de direcciones del disponible para inicializar el heap del recolector de basura. Por ocurrir antes de `Main`, los manejadores de errores de la aplicación no podían registrar información adicional.

La lógica funcional de la aplicación no fue la causa del fallo: el error se producía antes de crear el formulario y antes de ejecutar el botón.

## Solución aplicada

Se generó una nueva publicación de la aplicación con los siguientes ajustes:

1. Se cambió el subsistema de `WinExe` a `Exe` para conservar una consola visible durante el diagnóstico.
2. Se añadieron mensajes de inicio con runtime, arquitectura, sistema operativo, directorio base y PID.
3. Se añadieron manejadores para excepciones fatales, excepciones del hilo de interfaz y tareas no observadas.
4. Se configuró CoreCLR para utilizar:

   - GC de estación de trabajo.
   - GC no concurrente.
   - Límite de heap de 128 MiB.

La configuración se incorporó al proyecto mediante las propiedades `System.GC.Server`, `System.GC.Concurrent` y `System.GC.HeapHardLimit`.

También se generó una variante self-contained por carpeta, sin single-file, para evitar la extracción inicial de librerías nativas:

```text
TestApp/publish/win-x64-folder/
```

## Resultado

La aplicación comenzó a ejecutarse correctamente en Winlator después de reemplazar la publicación anterior por la versión actualizada. No fue necesario modificar las variables de entorno del contenedor de Winlator.

La solución confirmada corresponde a la nueva publicación de la aplicación, no a un cambio de configuración del entorno Android.

## Limitaciones pendientes

- La solución fue validada en el entorno Winlator utilizado para esta prueba; no garantiza el mismo resultado en todas sus versiones.
- La aplicación continúa requiriendo un contenedor compatible con Windows x64 y Box64.
- El límite de heap de 128 MiB está orientado a esta aplicación mínima y no debe generalizarse automáticamente a aplicaciones Windows más grandes.
- La variante single-file todavía puede ser más sensible a la memoria disponible; para diagnóstico y pruebas iniciales se recomienda `win-x64-folder`.
- Deben conservarse la versión del ejecutable, el dispositivo, la versión de Winlator y el resultado de la prueba para comparar futuras ejecuciones.

## Referencias

- [Configuración del recolector de basura de .NET](https://learn.microsoft.com/en-us/dotnet/core/runtime-config/garbage-collector)
- [Valores HRESULT comunes: `E_OUTOFMEMORY`](https://learn.microsoft.com/en-us/windows/win32/seccrypto/common-hresult-values)
