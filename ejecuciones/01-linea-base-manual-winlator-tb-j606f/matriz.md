# Ejecución 01: línea base manual en Winlator sobre Lenovo Tab P11

- **ID:** `EXEC-001`
- **Fecha del intento:** 2026-08-07, fecha visible en la evidencia
- **Fecha de registro:** 2026-08-10
- **Tipo:** manual, línea base de compatibilidad
- **Resultado general:** parcial: operación básica comprobada; empaquetado APK no evaluado
- **Método:** ejecución manual de `Win2APKTest.exe` dentro de Winlator

## Objetivo

Comprobar la ejecución y la operación básica de la aplicación Windows de referencia en un entorno Winlator antes de evaluar el empaquetado automatizado mediante Win2APK.

Esta ejecución sirve como línea base manual. No demuestra que exista un APK generado por Win2APK ni que el usuario final pueda omitir la configuración manual.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| Aplicación | Win2APK Test | Documento de limitación y evidencia |
| Versión | 0.1 | Documento `limitaciones/01-error-coreclr-gc-winlator.md` |
| Ejecutable | `Win2APKTest.exe` | Consola visible en la captura |
| Publicación | `win-x64-folder/`, por carpeta, no single-file | Ruta y contenido visibles en la captura |
| Runtime | .NET 8.0.29 | Consola visible en la captura |
| Arquitectura del proceso | x64 | Consola visible en la captura |
| Sistema Windows mostrado | Microsoft Windows 10.0.19045 | Consola visible en la captura |
| Entorno | Winlator sobre Android | Usuario y evidencia |
| Versión de Winlator | N/R | No aparece en la evidencia |
| Contenedor y configuración | N/R | No aparecen en la evidencia |
| Dispositivo | Lenovo TB-J606F, Lenovo Tab P11 | Datos confirmados del dispositivo |
| Android/API | Android 16 / API 36 | Datos confirmados del dispositivo |
| ABI reportadas | `arm64-v8a`, `armeabi-v7a`, `armeabi` | Datos confirmados del dispositivo |
| Resolución reportada | 1200×2000 | Datos confirmados del dispositivo |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Preparar y abrir la publicación manual | Parcial | N/R | Se abrió la carpeta `win-x64-folder` dentro de Winlator | [captura](./evidencias/01-win2apktest-winlator-tb-j606f.png) | No se registró el número exacto de pasos manuales |
| M-02 | Primer inicio | Aprobado | Ventana visible | Se ejecutó `Win2APKTest.exe` manualmente | [captura](./evidencias/01-win2apktest-winlator-tb-j606f.png) | Se observa la ventana con “Hola mundo” |
| M-03 | Operación básica: cambiar texto | Aprobado | Cambio visible | Se activó el botón | [captura](./evidencias/01-win2apktest-winlator-tb-j606f.png) | La consola muestra `Texto cambiado` |
| M-04 | Operación básica: restaurar texto | Aprobado | Restauración visible | Se activó nuevamente el botón | [captura](./evidencias/01-win2apktest-winlator-tb-j606f.png) | La consola muestra `Hola mundo` |
| M-05 | Repetición de la interacción | Aprobado | Varias alternancias visibles | Misma sesión manual | [captura](./evidencias/01-win2apktest-winlator-tb-j606f.png) | La captura muestra alternancias sucesivas; no se fija una cantidad exacta |
| M-06 | Apertura posterior después de cerrar | N/R | N/R | No hay evidencia de cierre y segundo inicio | N/A | Repetir en una ejecución posterior |
| M-07 | Aislamiento de archivos | N/A | N/A | La versión 0.1 no lee ni escribe archivos | [especificación](../../especificaciones/app-minima.md) | No aplica a esta aplicación mínima |
| M-08 | Persistencia de archivos | N/A | N/A | La versión 0.1 no tiene persistencia | [especificación](../../especificaciones/app-minima.md) | Requiere una variante de prueba con archivos |
| M-09 | Instalación de APK | N/A | N/A | Esta fue una ejecución manual dentro de Winlator | [bitácora](../../bitacora/index.md) | No se probó un APK generado |
| M-10 | Tamaño del APK | N/A | N/A | No existió APK en este intento | N/A | Medir en una ejecución del builder |
| M-11 | Tiempos | N/R | N/R | No se usó medición temporal documentada | N/A | Registrar instalación, primer inicio y aperturas posteriores |
| M-12 | Tasa de éxito | N/R | N/R | No se definió numerador/denominador para este único registro visual | N/A | No calcular una tasa con esta evidencia |
| M-13 | Pasos manuales eliminados | N/A | N/A | La prueba es precisamente la línea base manual | [guía](../AGENTS.md) | Comparar después con el flujo automatizado |

## Fallo y decisión asociada

La publicación inicial de la aplicación presentó el fallo de inicialización de CoreCLR/GC descrito en [Limitación 01](../../limitaciones/01-error-coreclr-gc-winlator.md). El mensaje registrado fue:

```text
GC heap initialization failed with error 0x8007000E
Failed to create CoreCLR, HRESULT: 0x8007000E
```

La solución documentada cambió el subsistema a `Exe`, añadió diagnósticos y configuró el recolector de basura; además, se generó la publicación por carpeta `win-x64-folder/` sin single-file. `EXEC-001` corresponde a la ejecución observada de esa publicación actualizada y el error no aparece en la captura.

Decisión para las siguientes pruebas: conservar la publicación por carpeta como referencia diagnóstica hasta comparar formalmente con la variante single-file. Esta decisión no generaliza el resultado a todas las versiones de Winlator ni a aplicaciones Windows de mayor tamaño.

## Evidencia

- [Captura de la ejecución manual](./evidencias/01-win2apktest-winlator-tb-j606f.png)
- [Informe detallado de la limitación](../../limitaciones/01-error-coreclr-gc-winlator.md)

La captura muestra la carpeta `win-x64-folder`, la ventana de `Win2APK Test`, la consola, el runtime, la arquitectura, el sistema Windows y varias alternancias del texto. No contiene la versión de Winlator ni la configuración del contenedor.

## Repetibilidad y pendientes

- [ ] Registrar la versión exacta de Winlator.
- [ ] Registrar la configuración y versión del contenedor.
- [ ] Guardar el hash de la publicación utilizada.
- [ ] Medir el tiempo del primer inicio y de aperturas posteriores.
- [ ] Repetir el caso desde un inicio en frío.
- [ ] Registrar una ejecución del APK generado por Win2APK.
- [ ] Comparar formalmente `win-x64-folder` con single-file.
- [ ] Mantener la evidencia por dispositivo sin extrapolar a los otros tres equipos.