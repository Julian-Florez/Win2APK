# Decisión: CLI Linux y configuración declarativa v2

- **Fecha:** 2026-09-19
- **Estado:** aceptada; implementación inicial verificada en host Linux x86_64
- **Propósito:** convertir el proceso experimental de Cuphead en un empaquetador reproducible para carpetas Windows preparadas.

## Problema

El prototipo funcional dependía de módulos Gradle llamados `cuphead_files_*`,
una ruta de configuración fija, una división manual del payload y herramientas
del host no administradas por el proyecto. Ese estado permitía reproducir el
caso Cuphead en la estación de desarrollo, pero no constituía un CLI instalable
ni un procedimiento aplicable a otra carpeta sin editar el motor.

## Decisión

La primera versión de `win2apk` será un binario Rust para Linux x86_64. Recibirá
un único JSON con esquema v2 y realizará validación, inventario, división,
staging, iconos, firma, build e instalación.

Se fijaron estas decisiones:

1. La entrada es una carpeta preparada; instalar software Windows queda fuera de alcance.
2. `applicationId`, ejecutable y versiones son explícitos; no se detectan ni derivan.
3. El icono es obligatorio.
4. La firma automática usa una clave persistente por `applicationId`; también se admite un keystore externo.
5. Se generan AAB y APKS para Google Play y para bundletool local-testing.
6. Una instalación existente nunca se desinstala de manera implícita.
7. Los archivos mayores que un pack se segmentan y reconstruyen automáticamente.
8. El estado final conserva el modo de una sola copia verificado con Cuphead: los archivos PAD se mueven al prefijo Wine y luego se limpian.

## Distribución del toolchain

El repositorio conserva código fuente, esquema, configuración y un lockfile con
versiones y checksums. GitHub Releases se usará para publicar el binario propio
y la plantilla del motor. JDK, Android SDK/NDK/CMake y bundletool se obtienen de
sus distribuidores oficiales mediante `win2apk setup`; no se copian dentro del
historial Git.

El toolchain administrado vive bajo los directorios XDG del usuario. La
aceptación de licencias de Android se presenta de forma interactiva y no se
oculta.

## División y límites

El planificador usa un objetivo predeterminado de 1.350.000.000 bytes por pack,
dejando margen respecto al límite publicado de Play Asset Delivery. Los
archivos normales se asignan completos mediante un algoritmo determinista de
mayor a menor. Un archivo sobredimensionado se convierte en segmentos con
desplazamientos explícitos.

Si el payload supera 30 GB acumulados o 100 packs, el build local no se rechaza.
El reporte registra que el AAB no es publicable bajo los límites actuales de
Google Play.

## Instalación y actualización

- `win2apk install archivo.apks` instala sólo cuando el paquete no existe.
- `--fresh` permite explícitamente una desinstalación y reinstalación completas.
- `--code-update` actualiza los splits base con la misma firma y conserva los datos.
- Las actualizaciones distribuidas por Google Play siguen el flujo administrado por Play.

## Consecuencias

La carpeta original permanece intacta. Los módulos de asset packs son staging
regenerable y no forman parte del motor versionado. El proceso de instalación
en Android continúa teniendo una fase transitoria en la que Android conserva
los packs, pero el estado confirmado elimina las fuentes después de verificar
el árbol final.

Linux ARM64, aplicaciones x86 de Android y ejecución de instaladores Windows no
forman parte de esta versión.

## Trazabilidad

- [Especificación del CLI](../especificaciones/cli-empaquetado.md)
- [EXEC-047: build genérico y Cuphead](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md)
- [Limitación 35: output incremental de Gradle](../limitaciones/35-gradle-reutiliza-aab-entre-configuraciones.md)
- [Limitación 36: firma AGP multigigabyte](../limitaciones/36-agp-aab-multigigabyte-agotamiento-memoria.md)
- [Distribución de datos y una sola copia](../especificaciones/distribucion-datos-juego.md)
- [Automatización de iconos](./11-automatizacion-iconos-launcher.md)
- [Decisión de target API 28](./10-decision-target-api28-para-winlator-exec.md)
