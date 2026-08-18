# Limitación 02: entorno incompleto para compilar Winlator

- **Proyecto:** Win2APK
- **Aplicación:** Winlator 11.1 modificada
- **Entorno:** repositorio local con Gradle 7.3.3, Android Gradle Plugin 7.2.2 y Android SDK local
- **Estado:** resuelta experimentalmente
- **Fecha de registro:** 2026-08-18

## Descripción

La modificación para crear automáticamente un contenedor predeterminado pudo compilarse en Java, pero no fue posible completar la compilación del APK porque el entorno no contiene CMake 3.22.1 ni Ninja, herramientas requeridas por el bloque `externalNativeBuild` de Winlator.

## Contexto técnico

El proyecto usa Gradle 7.3.3 y Android Gradle Plugin 7.2.2. La primera ejecución utilizó OpenJDK 21.0.12 y falló por incompatibilidad del Gradle incluido. La segunda ejecución utilizó OpenJDK 17.0.20 y encontró el Android SDK en `/home/julian/Android/Sdk`, pero la configuración nativa no pudo localizar CMake 3.22.1 ni Ninja.

## Reproducción o evidencia

Con OpenJDK 21.0.12:

```text
Unsupported class file major version 65
```

Con OpenJDK 17.0.20 y el SDK configurado:

```text
[CXX1300] CMake '3.22.1' was not found in SDK, PATH, or by cmake.dir property.
[CXX1416] Could not find Ninja on PATH or in SDK CMake bin folders.
```

Al desactivar temporalmente el bloque nativo únicamente para aislar la compilación Java, la tarea `:app:compileDebugJavaWithJavac` terminó con `BUILD SUCCESSFUL`. La configuración nativa original fue restaurada inmediatamente después.

## Impacto

No se puede confirmar todavía que el APK completo de Winlator compile ni instalarlo en un dispositivo Android. La limitación impide verificar en dispositivo la creación automática de `Container-1`.

## Análisis técnico

La limitación corresponde al entorno de construcción y no constituye evidencia de un error en la lógica Java añadida. La compilación Java pasó cuando se aisló el componente nativo; la cadena CMake/NDK no pudo iniciar por falta de CMake 3.22.1 y Ninja.

## Solución aplicada

- Se usó JDK 17, compatible con el Gradle incluido.
- Se configuró temporalmente el Android SDK existente mediante variables del entorno de compilación.
- Se aisló la compilación Java sin alterar de forma permanente el `build.gradle`.

## Resultado

La compilación parcial de Java fue satisfactoria. En una ejecución posterior, después de instalar CMake 3.22.1 y disponer del NDK requerido, la build avanzó hasta detectar una duplicación independiente de bibliotecas nativas; esa segunda limitación se documenta en [Limitación 03](./03-duplicacion-bibliotecas-nativas.md).

La limitación de herramientas ausentes quedó resuelta experimentalmente en [EXEC-003](../ejecuciones/03-build-apk-winlator/matriz.md).

## Limitaciones pendientes

- CMake 3.22.1 no está instalado.
- Ninja no está disponible en el PATH ni en los directorios de CMake del SDK.
- No existe todavía un APK generado a partir de esta modificación.
- No se ha probado el contenedor predeterminado en un dispositivo Android.

## Referencias

- [Configuración de compilación de Winlator](../winlator/app/app/build.gradle)
- [Ejecución asociada](../ejecuciones/02-compilacion-winlator/matriz.md)

## Ejecuciones asociadas

- [EXEC-002: verificación de compilación de Winlator](../ejecuciones/02-compilacion-winlator/matriz.md)
