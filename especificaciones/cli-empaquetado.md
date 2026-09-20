# Especificación del CLI de empaquetado Win2APK

- **Identificador:** `WIN2APK-CLI-001`
- **Versión:** 0.1
- **Fecha:** 2026-09-19
- **Estado:** implementación inicial
- **Decisión relacionada:** [CLI Linux y configuración v2](../documentacion/13-decision-cli-linux-configuracion-v2.md)

## Alcance

El CLI recibe una carpeta Windows ya preparada y un JSON explícito. No ejecuta
instaladores de Windows ni infiere el ejecutable principal. El resultado sigue
siendo una aplicación ejecutada mediante un entorno de compatibilidad, no una
aplicación Android nativa.

La primera versión del host admite únicamente Linux x86_64. El APK generado
contiene bibliotecas `arm64-v8a` y requiere Android API 26 o posterior.

## Requisitos funcionales

| ID | Requisito verificable |
|---|---|
| CLI-RF-01 | `win2apk validate CONFIG` deberá rechazar un JSON distinto del esquema v2, rutas inexistentes, un `applicationId` inválido o un `entrypoint` que no exista dentro de `sourceFolder`. |
| CLI-RF-02 | El usuario deberá indicar explícitamente nombre, carpeta fuente, ejecutable, directorio de instalación, `applicationId`, `versionCode`, `versionName` e icono. |
| CLI-RF-03 | Las rutas relativas del JSON se resolverán respecto al directorio que contiene el JSON. |
| CLI-RF-04 | `win2apk plan CONFIG` deberá recorrer la carpeta sin modificarla y producir siempre el mismo plan para el mismo contenido y configuración. |
| CLI-RF-05 | Los archivos de tamaño menor o igual a `targetPackBytes` se asignarán completos a un asset pack. |
| CLI-RF-06 | Un archivo mayor que `targetPackBytes` se dividirá automáticamente en segmentos ordenados, sin rechazar el proyecto por ese motivo. |
| CLI-RF-07 | El manifiesto deberá registrar ruta, tamaño y SHA-256 de cada archivo, además del pack, ruta, desplazamiento y tamaño de cada segmento. |
| CLI-RF-08 | El CLI generará automáticamente los módulos PAD `on-demand` sin exigir subcarpetas preparadas por el usuario. |
| CLI-RF-09 | El CLI generará recursos de launcher adaptativos, monocromáticos y heredados a partir del icono obligatorio. |
| CLI-RF-10 | `win2apk build CONFIG` generará AAB, APKS o ambos según `distribution`, además de manifiesto, configuración resuelta, checksums y reporte. |
| CLI-RF-11 | `signing.profile=auto` generará una clave persistente distinta por `applicationId`; un build posterior deberá reutilizarla. |
| CLI-RF-12 | `signing.profile=custom` leerá las contraseñas sólo desde variables de entorno y nunca desde el JSON. |
| CLI-RF-13 | `win2apk install` no desinstalará una aplicación existente sin `--fresh`. |
| CLI-RF-14 | `win2apk install --code-update` actualizará únicamente los splits del módulo base y conservará el payload instalado. |
| CLI-RF-15 | El motor reconstruirá archivos segmentados, moverá archivos ordinarios y eliminará las fuentes PAD sólo después de validar el destino. |
| CLI-RF-16 | Una instalación interrumpida deberá conservar el contenedor y poder continuar en un arranque posterior. |
| CLI-RF-17 | `win2apk setup` instalará un toolchain aislado con JDK 17, Android SDK 36, NDK 30.0.15729638, CMake 3.22.1, platform-tools y bundletool 1.18.3. |
| CLI-RF-18 | `win2apk doctor` deberá comprobar host, Java, SDK, ADB, bundletool y plantilla Android antes de construir. |

## Requisitos no funcionales

| ID | Requisito verificable |
|---|---|
| CLI-RNF-01 | La carpeta fuente no será modificada durante validación, planificación, staging o build. |
| CLI-RNF-02 | Los binarios de terceros no se almacenarán en el historial Git; se descargarán desde su fuente oficial y se verificarán mediante checksum. |
| CLI-RNF-03 | Las claves y contraseñas no se almacenarán en el repositorio ni se imprimirán en el reporte de build. |
| CLI-RNF-04 | Los archivos temporales vivirán bajo el caché XDG y `clean` sólo podrá eliminar staging regenerable. |
| CLI-RNF-05 | El APK conservará una sola copia completa del payload después de una preparación exitosa y de la limpieza PAD. |
| CLI-RNF-06 | Un payload mayor de 30 GB o con más de 100 packs no se rechazará para instalación local; el reporte lo marcará como no compatible con los límites de Google Play. |
| CLI-RNF-07 | El binario publicado se compilará para Linux x86_64 y no requerirá tener Rust instalado. |

## Contrato de salida

Una construcción completa produce:

```text
dist/
├── <nombre>-<version>.aab
├── <nombre>-<version>.apks
├── build-report.json
├── checksums.sha256
├── payload-manifest.json
└── resolved-config.json
```

`build-report.json` es el registro de procedencia del build. No constituye por
sí solo evidencia de ejecución en un dispositivo; esa evidencia se conserva en
`ejecuciones/`.

## Criterios de aceptación

| ID | Criterio | Evidencia |
|---|---|---|
| CLI-CA-01 | Compilación, pruebas unitarias y validación de la configuración Cuphead v2 | Aprobado; `cargo test`, `cargo clippy`, `validate` y [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md) |
| CLI-CA-02 | AAB y APKS generados desde una carpeta de prueba sin módulos manuales | Aprobado; [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md) |
| CLI-CA-03 | Instalación fría, reconstrucción de segmentos y segundo arranque | N/R; requiere prueba en Android |
| CLI-CA-04 | Reempaquetado completo de Cuphead mediante una sola orden | Aprobado en host; [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md) |
