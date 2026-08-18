# Ejecución 03: generación del APK de Winlator con contenedor por defecto

- **ID:** `EXEC-003`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** compilación completa del APK
- **Resultado general:** aprobado: APK debug generado y firmado
- **Método:** Gradle sobre el submódulo `winlator/app`

## Objetivo

Generar el APK completo de Winlator después de incorporar la creación automática del contenedor predeterminado y corregir el conflicto de bibliotecas nativas.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| Proyecto | Winlator | Repositorio local `winlator` |
| Versión | 11.1 / versionCode 28 | `app/build.gradle` y `aapt dump badging` |
| Revisión del repositorio | `fb66541` | `git -C winlator log` |
| Revisión del submódulo Android | `c2f4ad4` | `git -C winlator submodule status` |
| Gradle | 7.3.3 | `gradle-wrapper.properties` |
| Android Gradle Plugin | 7.2.2 | `build.gradle` |
| JDK | OpenJDK 17.0.20 | Runtime usado por Gradle |
| Android SDK | `/home/julian/Android/Sdk` | Ruta usada por Gradle |
| CMake | 3.22.1 | Instalado en el SDK |
| NDK | 24.0.8215888 | `app/build.gradle` |
| ABI | `arm64-v8a` | `app/build.gradle` |
| Tarea | `assembleDebug` | Comando ejecutado |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | Compilar el código Java modificado | Aprobado | Tarea `compileDebugJavaWithJavac` | Sin errores de compilación |
| M-02 | Compilar las bibliotecas nativas | Aprobado | `configureCMakeDebug`, `buildCMakeDebug`, `externalNativeBuildDebug` | ABI `arm64-v8a` |
| M-03 | Generar el APK | Aprobado | `BUILD SUCCESSFUL` | `app-debug.apk`, 150 MB |
| M-04 | Verificar la firma debug | Aprobado | APK Signature Scheme v2: `true` | Un firmante; no es firma de publicación |
| M-05 | Instalar y ejecutar en Android | N/R | N/A | Pendiente de prueba en dispositivo |
| M-06 | Verificar creación automática de `Container-1` | N/R | N/A | Pendiente de prueba en dispositivo limpio |

## Artefacto generado

```text
winlator/app/app/build/outputs/apk/debug/app-debug.apk
```

- **Tamaño:** 150 MB
- **SHA-256:** `b50459e48d7cd5d93c259408db4683cfc7750d018fb464dcd44fbf339be03b25`
- **Paquete:** `com.winlator`
- **Versión:** 11.1
- **Firma:** APK Signature Scheme v2 verificada

El APK contiene las bibliotecas nativas `arm64-v8a`, `rootfs.tzst` y `container_pattern.tzst`.

## Corrección aplicada durante la ejecución

La primera repetición de la build falló porque `libFLAC.so` y otras bibliotecas de MIDI aparecían tanto en `jniLibs` como en targets IMPORTED de CMake. Se añadieron reglas `packagingOptions.pickFirst` para las copias idénticas. La limitación está documentada en [Limitación 03](../../limitaciones/03-duplicacion-bibliotecas-nativas.md).

## Pendientes

- [ ] Instalar el APK en un dispositivo Android ARM64.
- [ ] Confirmar que el primer inicio crea `Container-1` sin abrir el formulario.
- [ ] Confirmar que una segunda apertura no crea un contenedor adicional.
- [ ] Ejecutar `Win2APKTest.exe` dentro del contenedor generado.

