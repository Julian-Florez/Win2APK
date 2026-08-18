# Ejecución 05: aplicación de pruebas y shortcut preinstalados en el contenedor

- **ID:** `EXEC-005`
- **Fecha del intento:** 2026-08-18
- **Fecha de registro:** 2026-08-18
- **Tipo:** compilación, instalación limpia y verificación de archivos en dispositivo
- **Resultado general:** aprobado para el empaquetado y la copia automática de la aplicación de pruebas
- **Método:** generación de APK mediante Gradle, instalación mediante ADB y lectura del almacenamiento privado de la aplicación

## Objetivo

Comprobar que una instalación limpia de la APK incluye la publicación completa de `Win2APKTest`, la copia en `C:\Win2APKTest` y un shortcut visible para esa aplicación al crear el contenedor predeterminado.

## Condiciones de prueba

| Campo | Valor observado | Fuente o estado |
|---|---|---|
| APK | `app-debug.apk` | Salida de `assembleDebug` |
| Tamaño APK | 205 MB | `ls -lh` |
| SHA-256 APK | `9e495554281f6343237a7b7e745702cd32bed117580f71a60489faa2a0438876` | `sha256sum` |
| Asset incluido | `assets/test_app.tzst` | Lista del APK; archivo generado desde `TestApp/publish/win-x64-folder` |
| Publicación de origen | `TestApp/publish/win-x64-folder` | 161 MB; 463 archivos |
| Dispositivo | Redmi Note 8 | ADB, serial `16f88243` |
| Android/API | Android 16 / API 36 | Propiedades del dispositivo |
| Instalación | Aprobada | `adb install` devolvió `Success` |
| RootFS | Versión 19 | `files/rootfs/.winlator/.rfs_version` |

## Matriz de criterios

| ID | Criterio | Resultado | Evidencia | Observaciones |
|---|---|---|---|---|
| M-01 | Compilar la APK con el asset de pruebas | Aprobado | `BUILD SUCCESSFUL` | El APK aumentó a 205 MB al incluir la publicación autocontenida |
| M-02 | Instalar desde cero | Aprobado | Desinstalación seguida de `adb install` | Se eliminó previamente solo el paquete `com.winlator` del dispositivo de prueba |
| M-03 | Crear el contenedor predeterminado | Aprobado | `files/rootfs/home/xuser-1` | Se creó durante el primer inicio |
| M-04 | Crear `C:\Win2APKTest` automáticamente | Aprobado | `files/rootfs/home/xuser-1/.wine/drive_c/Win2APKTest` | La ruta corresponde a la unidad `C:` del contenedor |
| M-05 | Copiar la publicación completa | Aprobado | Conteo de archivos en origen, asset y dispositivo | Se observaron 463 archivos en cada punto |
| M-06 | Copiar `Win2APKTest.exe` | Aprobado | `test -f .../Win2APKTest.exe` devolvió código 0 | Tamaño observado: 152064 bytes |
| M-07 | Crear el shortcut en el Desktop del contenedor | Aprobado | `users/xuser/Desktop/Win2APKTest.desktop` | Contiene `Exec=wine C:\\Win2APKTest\\Win2APKTest.exe` |
| M-08 | Ejecutar la aplicación Windows desde el shortcut | N/R | N/A | Esta ejecución verificó la creación del shortcut; no ejecutó el binario mediante Wine |

## Implementación verificada

- La publicación se empaquetó en [`test_app.tzst`](../../winlator/app/app/src/main/assets/test_app.tzst).
- La instalación se realiza desde [`ContainerManager.java`](../../winlator/app/app/src/main/java/com/winlator/container/ContainerManager.java), después de extraer el patrón del contenedor predeterminado.
- El shortcut se guarda como `Win2APKTest.desktop` en el `Desktop` del usuario y utiliza el formato que consume `ShortcutsFragment`.
- Si la extracción falla, el contenedor recién creado se elimina y la creación se reporta como fallida.

## Pendientes

- [ ] Ejecutar `Win2APKTest.exe` dentro de `Container-1`.
- [ ] Confirmar visualmente la ventana y la interacción del botón.
