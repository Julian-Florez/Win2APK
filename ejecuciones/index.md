# Ejecuciones de Win2APK

Cada registro corresponde a un intento experimental independiente. Las matrices conservan las condiciones y las observaciones disponibles en ese momento.

| ID | Ejecución | Tipo | Dispositivo | Resultado general | Matriz | Evidencia |
|---|---|---|---|---|---|---|
| EXEC-001 | Línea base manual en Winlator | Manual | Lenovo TB-J606F | Parcial: operación básica comprobada | [matriz.md](./01-linea-base-manual-winlator-tb-j606f/matriz.md) | [captura](./01-linea-base-manual-winlator-tb-j606f/evidencias/01-win2apktest-winlator-tb-j606f.png) |
| EXEC-002 | Verificación de compilación de Winlator | Compilación | N/A | Parcial: Java aprobado, APK no generado | [matriz.md](./02-compilacion-winlator/matriz.md) | N/A |
| EXEC-003 | Generación del APK de Winlator con contenedor por defecto | Compilación | N/A | Aprobado: APK debug generado | [matriz.md](./03-build-apk-winlator/matriz.md) | APK local no versionado |
| EXEC-004 | Verificación del contenedor predeterminado en Xiaomi Mi A3 | Dispositivo | Xiaomi Mi A3 | Aprobado: instalación, creación e idempotencia | [matriz.md](./04-prueba-dispositivo-mi-a3/matriz.md) | N/A |
| EXEC-005 | Aplicación de pruebas y shortcut preinstalados en el contenedor | Dispositivo | Redmi Note 8 | Aprobado: copia de 463 archivos y shortcut automático | [matriz.md](./05-prueba-aplicacion-preinstalada-redmi-note-8/matriz.md) | N/A |
| EXEC-006 | Depuración del shortcut de Win2APKTest | Dispositivo | Lenovo TB-J606F | Aprobado: crash reproducido y corregido | [matriz.md](./06-debug-shortcut-win2apktest-lenovo/matriz.md) | N/A |
| EXEC-007 | Winlator Core desde instalación limpia | Dispositivo | Lenovo TB-J606F | Aprobado: arranque oculto y aplicación automática con `com.winlator` | [matriz.md](./07-winlator-core-limpio-lenovo/matriz.md) | N/A |
| EXEC-008 | Winlator Core con `applicationId` dinámico | Dispositivo | Lenovo TB-J606F | Aprobado: `com.testappx`, rootfs transformado y aplicación automática | [matriz.md](./08-winlator-core-paquete-dinamico-lenovo/matriz.md) | N/A |
| EXEC-009 | Winlator Core con paquete variable y descriptor de rootfs | Dispositivo | Lenovo TB-J606F | Aprobado: `com.testapp`, alias heredado y aplicación automática | [matriz.md](./09-winlator-core-paquete-variable-fd-lenovo/matriz.md) | N/A |

## Plantilla

Usar [plantilla-metricas.md](./plantilla-metricas.md) para crear la matriz del siguiente intento. No completar campos con datos que no estén respaldados por la ejecución.
