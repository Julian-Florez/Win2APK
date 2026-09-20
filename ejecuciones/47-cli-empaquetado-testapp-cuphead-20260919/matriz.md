# EXEC-047 — CLI declarativo con carpeta genérica y Cuphead

- **ID:** `EXEC-047`
- **Fecha:** `2026-09-19`
- **Tipo:** automatizada; comparación y repetición de build
- **Resultado general:** aprobado con correcciones durante la ejecución
- **Método:** `win2apk validate`, `win2apk plan` y `win2apk build` usando el
  esquema v2; primero se comprobó una carpeta genérica y después la carpeta
  completa de Cuphead. Se validaron los artefactos con `bundletool` y con una
  inspección ZIP resumida.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación genérica | Win2APKTest | `config/example.testapp.json` |
| Aplicación de reempaquetado | Cuphead | `config/win2apk.json` |
| Versión genérica | `0.1.0`, `versionCode=1` | Configuración v2 |
| Versión Cuphead | `11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core`, `versionCode=48` | Configuración v2 |
| Ejecutables | `Win2APKTest.exe`; `Cuphead.exe` | JSON y validación de entrada |
| Método | CLI Rust local con Gradle, firma externa y bundletool | Host de desarrollo |
| Host | Linux x86_64 | Restricción de alcance v0.1 |
| Motor Android | `winlator/app` | Repositorio local |
| Toolchain | SDK disponible en el host; bundletool `1.18.3` | Fallback de desarrollo; `WIN2APK_BUNDLETOOL` |
| Dispositivo/Android/ABI | N/A | No se realizó instalación en dispositivo en esta ejecución |
| Fecha y hora de inicio | N/R | No se registró un cronómetro de inicio único |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Validación de configuración | Aprobado | 463 archivos genéricos; 815 archivos Cuphead | `validate` y `plan` | [resumen](./logs/resumen.md) | La carpeta fuente permaneció fuera del staging |
| M-02 | División determinista | Aprobado | 1 pack genérico; 5 packs Cuphead | `targetPackBytes=1.350.000.000` | [reporte Cuphead](./evidencias/build-report-cuphead.json) | Cuphead total: 5.847.372.363 bytes |
| M-03 | Generación de icono | Aprobado | Recursos adaptive, monochrome y legacy | Icono obligatorio del JSON | [resumen](./logs/resumen.md) | Sin ImageMagick, Inkscape ni Python |
| M-04 | AAB genérico | Aprobado | 490.787.881 bytes | Build limpio | [reporte TestApp](./evidencias/build-report-testapp.json) | El AAB contiene solo `win2apk_payload_001` |
| M-05 | APKS genérico | Aprobado | 744.602.045 bytes | `bundletool build-apks` | [checksums](./evidencias/checksums-testapp.sha256) | 86 entradas ZIP |
| M-06 | AAB Cuphead | Aprobado | 5.494.326.036 bytes | Build limpio, firma externa | [reporte Cuphead](./evidencias/build-report-cuphead.json) | `bundletool validate` aprobado |
| M-07 | APKS Cuphead | Aprobado | 6.424.836.814 bytes | `bundletool build-apks` | [checksums](./evidencias/checksums-cuphead.sha256) | 90 entradas ZIP |
| M-08 | Firma persistente | Aprobado | Firma automática reutilizable por `applicationId` | Clave fuera del repositorio | [resumen](./logs/resumen.md) | No se registra ninguna contraseña |
| M-09 | Instalación Android | N/A | N/A | Esta ejecución solo construyó artefactos | N/A | Requiere una ejecución de dispositivo separada |
| M-10 | Reconstrucción/movimiento del payload | N/A | N/A | No se instaló en Android | N/A | Pendiente para `EXEC-048` o posterior |

## Intentos y fallos observados

1. La firma de AGP agotó la memoria con un AAB de varios gigabytes; se cambió a
   firma externa con el módulo `jdk.jartool`.
2. La primera prueba genérica reutilizó el AAB anterior de Cuphead porque el
   output de Gradle era compartido entre builds; el artefacto no se publicó.
3. La reconstrucción limpia dejó el AAB intermedio pero las tareas de listado de
   AGP esperaban el AAB firmado; se desactivaron esas tareas cuando firma el CLI.
4. La firma mediante `jarsigner @archivo` no era válida como invocación directa;
   se corrigió ejecutando `java @archivo` y seleccionando el módulo JDK.
5. La prueba genérica final y el build completo de Cuphead terminaron con AAB,
   APKS, reportes y checksums.

## Decisión

La arquitectura CLI v2 queda aprobada para continuar. El build debe limpiar el
output de Gradle en cada ejecución y firmar el AAB intermedio externamente. La
instalación en Android y la verificación de una sola copia siguen pendientes.

## Evidencias

- [Log resumido](./logs/resumen.md)
- [Reporte TestApp](./evidencias/build-report-testapp.json)
- [Reporte Cuphead](./evidencias/build-report-cuphead.json)
- [Checksums TestApp](./evidencias/checksums-testapp.sha256)
- [Checksums Cuphead](./evidencias/checksums-cuphead.sha256)

## Repetibilidad y pendientes

- [x] Validar una carpeta genérica sin heredar los packs de Cuphead.
- [x] Reempaquetar Cuphead completo desde el JSON v2.
- [x] Validar AAB y APKS con bundletool.
- [ ] Ejecutar `win2apk install --fresh` en un dispositivo.
- [ ] Verificar el movimiento y la limpieza de las fuentes PAD en Android.
- [ ] Empaquetar un binario Linux x86_64 instalable sin Rust.
