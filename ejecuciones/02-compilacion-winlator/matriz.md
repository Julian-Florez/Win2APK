# Ejecución 02: verificación de compilación de Winlator con contenedor por defecto

- **ID:** `EXEC-002`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** compilación y verificación estática
- **Resultado general:** parcial: compilación Java aprobada; APK completo no generado
- **Método:** Gradle sobre el submódulo `winlator/app`

## Objetivo

Comprobar que los cambios para crear automáticamente el primer contenedor después de instalar el sistema de archivos de Winlator compilan correctamente.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| Proyecto | Winlator | Repositorio local `winlator` |
| Versión declarada | 11.1 / versionCode 28 | `app/build.gradle` |
| Revisión del repositorio | `fb66541` | `git -C winlator log` |
| Revisión del submódulo Android | `c2f4ad4` | `git -C winlator submodule status` |
| Gradle | 7.3.3 | `gradle-wrapper.properties` |
| Android Gradle Plugin | 7.2.2 | `build.gradle` |
| JDK inicial | OpenJDK 21.0.12 | `java -version` |
| JDK usado para la compilación Java | OpenJDK 17.0.20 | Ruta local del JDK |
| Android SDK | `/home/julian/Android/Sdk` | Ruta existente en el entorno |
| CMake requerido | 3.22.1 | Declarado en `app/build.gradle` |
| CMake disponible | N/R; no encontrado | Salida de Gradle |
| Ninja disponible | N/R; no encontrado | Salida de Gradle |
| Dispositivo Android | N/A | No se generó APK |

## Matriz de criterios

| ID | Criterio | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | El código Java modificado debe compilar | Aprobado | Salida de `:app:compileDebugJavaWithJavac` | Se aisló temporalmente el bloque de compilación nativa para verificar Java |
| M-02 | La configuración original de CMake/NDK debe conservarse | Aprobado | `git diff --check` y revisión de `app/build.gradle` | La configuración fue restaurada después de la prueba aislada |
| M-03 | Generar el APK completo | No evaluado | N/A | La configuración nativa requiere CMake 3.22.1 y Ninja |
| M-04 | Instalar y ejecutar en Android | N/A | N/A | No existió APK generado |
| M-05 | Verificar creación automática del contenedor en dispositivo | N/A | N/A | Pendiente de instalar el APK en un dispositivo |

## Cambios incluidos en el intento

- `MainActivity` solicita la creación del contenedor predeterminado cuando el `rootfs` está listo.
- `ContainerManager` construye la configuración predeterminada y extrae el patrón de contenedor existente.
- `RootFSInstaller` expone un callback para continuar después de la instalación asíncrona del `rootfs`.

## Errores y decisiones

Con Java 21, Gradle informó exactamente:

```text
Unsupported class file major version 65
```

Al repetir con JDK 17 y el SDK configurado, Gradle informó:

```text
[CXX1300] CMake '3.22.1' was not found in SDK, PATH, or by cmake.dir property.
[CXX1416] Could not find Ninja on PATH or in SDK CMake bin folders.
```

Decisión: conservar el código de Winlator sin actualizar su versión de Gradle o del Android Gradle Plugin. La compilación completa se repetirá cuando el entorno tenga CMake 3.22.1 y Ninja.

## Pendientes

- [ ] Instalar CMake 3.22.1 y Ninja.
- [ ] Ejecutar la compilación completa del APK.
- [ ] Instalar el APK en un dispositivo Android limpio.
- [ ] Confirmar que aparece `Container-1` sin usar el formulario de creación.
- [ ] Confirmar que una segunda apertura no crea un contenedor adicional.

