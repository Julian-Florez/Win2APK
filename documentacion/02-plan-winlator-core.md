# 02. Plan de Winlator Core

- **Fecha:** 2026-08-18
- **Estado:** implementación funcional verificada, incluido paquete dinámico
- **Propósito:** definir la transformación de Winlator en un núcleo de ejecución dedicado para una aplicación Windows empaquetada.

## Decisión

La distribución será una APK Android normal, sin root y sin mostrar la interfaz general de Winlator. El usuario tocará el icono una vez; desde ese momento el núcleo mostrará únicamente una carga mínima, preparará el filesystem y el contenedor en segundo plano y abrirá automáticamente el shortcut de la aplicación Windows.

Cuando la aplicación Windows termine, el núcleo cerrará su actividad y devolverá al usuario al launcher de Android.

## Flujo previsto

```text
Instalar APK
    ↓
Usuario toca el icono una vez
    ↓
Pantalla de carga mínima
    ↓
Preparar rootfs y Container-1 sin mostrar opciones
    ↓
Copiar la carpeta Windows configurada
    ↓
Crear el shortcut configurado
    ↓
Abrir automáticamente la aplicación Windows
    ↓
Cerrar el núcleo cuando la aplicación termine
```

## Configuración previa a la compilación

El archivo [`config/win2apk.json`](../config/win2apk.json) es la fuente única de configuración previa a la compilación. Controla, como mínimo:

- carpeta de entrada y ejecutable Windows;
- nombre del shortcut y ruta de destino;
- etiqueta, nombre y `applicationId` derivado de la carpeta;
- nombre e identificador del contenedor;
- resolución, variables de entorno y afinidad de CPU;
- driver gráfico, configuración gráfica, DX wrapper y configuración;
- driver de audio y configuración;
- componentes Windows;
- unidades `D:` y `E:`;
- HUD, modo de inicio, preset Box64, tema y versión de Wine;
- carga mínima, ocultamiento de interfaz, autoejecución y comportamiento al salir;
- política de error técnico.

La APK no expondrá estas opciones al usuario final.

## Empaquetado dinámico

Gradle genera el `applicationId` durante la compilación a partir del nombre normalizado de la carpeta, sin truncarlo, rellenarlo ni imponer un límite de ocho caracteres. La normalización solo conserva la sintaxis válida para un `applicationId` Android: segmentos en minúsculas, con caracteres alfanuméricos, y un prefijo `app` si el nombre empieza por un número.

La tarea `prepareCoreAssets` crea una copia generada de los assets y reemplaza la raíz original `/data/data/com.winlator` por un alias de igual longitud basado en `/proc/self/fd/3`. Así no se modifican offsets de ejecutables ni bibliotecas. El launcher nativo abre la carpeta de datos del paquete como descriptor 3, elimina `FD_CLOEXEC` y ejecuta Box64 directamente; los procesos Wine heredan el descriptor y resuelven el rootfs aunque el paquete tenga otra longitud. La compilación también pasa las rutas dinámicas a CMake para las librerías nativas de Winlator.

El identificador Android se define al compilar, no durante la ejecución. Si cambia el nombre de carpeta y, por tanto, el `applicationId`, Android lo tratará como otra aplicación y no como una actualización de la anterior.

## Resultado de la primera implementación

1. Contrato JSON y sincronización automática dentro de `assets`.
2. Etiqueta y parámetros de compilación desde el contrato.
3. Arranque de preparación separado del flujo de interfaz general.
4. Preparación oculta de rootfs, contenedor, carpeta y shortcut.
5. Lanzamiento automático de `XServerDisplayActivity`.
6. Cierre de la tarea Core al terminar el proceso Windows.
7. Mensaje técnico ante fallos de configuración o preparación.
8. Verificación mediante `adb install` y una instalación limpia.
9. Paquete dinámico sin límite de longitud, con transformación reproducible de assets, alias de rootfs y launcher nativo.

## Decisiones pendientes

- Si el mensaje técnico debe incluir un botón para copiar el diagnóstico.
- Aplicación Windows definitiva que reemplazará a `TestApp` y actualización de `pathRewriteAssets` si incorpora nuevos assets sensibles.

## Trazabilidad

- [Especificación de Winlator Core](../especificaciones/winlator-core.md)
- [Limitación del primer toque sin root](../limitaciones/05-inicio-winlator-core-sin-root.md)
- [Ejecución del shortcut corregido](../ejecuciones/06-debug-shortcut-win2apktest-lenovo/matriz.md)
- [Ejecución dinámica en instalación limpia](../ejecuciones/08-winlator-core-paquete-dinamico-lenovo/matriz.md)
- [Ejecución con paquete variable y descriptor de rootfs](../ejecuciones/09-winlator-core-paquete-variable-fd-lenovo/matriz.md)
