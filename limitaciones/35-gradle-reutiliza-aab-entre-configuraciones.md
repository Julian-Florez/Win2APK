# 35. Gradle reutiliza el AAB de una configuración anterior

## Descripción

Durante la primera repetición de la prueba genérica, Gradle dejó como salida el
`app-release.aab` producido por Cuphead. El CLI estaba construyendo
`Win2APKTest`, pero el AAB conservaba los cinco asset packs de Cuphead. El
artefacto no se publicó ni se usó para instalarlo.

## Contexto técnico

- Motor: `winlator/app`.
- Configuración anterior: Cuphead, cinco módulos dinámicos llamados
  `win2apk_payload_001` a `win2apk_payload_005`.
- Configuración solicitada: TestApp, un módulo `win2apk_payload_001`.
- Gradle conserva el output en `app/build/outputs/bundle/release/` y el nombre
  de los módulos dinámicos se reutiliza entre builds.
- Ejecución relacionada: [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md).

## Reproducción o evidencia

La primera tentativa genérica terminó con un proceso de firma sobre el output
existente. La inspección del ZIP mostró:

```text
app-release.aab: 5494326036 bytes
manifest modules: win2apk_payload_001, win2apk_payload_002,
                  win2apk_payload_003, win2apk_payload_004,
                  win2apk_payload_005
```

El timestamp del AAB correspondía al build anterior de Cuphead y no al build
genérico. La prueba se interrumpió antes de entregar el archivo.

## Impacto

Sin invalidar el output, una segunda aplicación podría recibir archivos de la
primera. Eso compromete la reproducibilidad y podría distribuir datos de otra
aplicación bajo un `applicationId` distinto.

## Análisis técnico

La observación confirma una interacción entre el output compartido de Gradle,
los nombres repetidos de módulos y la detección incremental de symlinks/staging.
No se interpretó como un problema del planificador de archivos: el plan
genérico sí contenía 463 archivos y 167.479.464 bytes.

## Solución aplicada

El CLI ejecuta `:app:clean :app:bundleRelease` en cada build. Después inspecciona
el AAB intermedio de la ejecución actual, lo firma y lo copia a un directorio de
salida separado. La prueba final produjo un AAB genérico de 490.787.881 bytes
con solo `win2apk_payload_001` y sin entradas `Cuphead`.

## Resultado

Resuelta experimentalmente en el host Linux x86_64 y en el motor utilizado por
`EXEC-047`. Debe repetirse si se cambia el motor Gradle o el sistema de staging.

## Limitaciones pendientes

- La limpieza completa aumenta el tiempo de cada build.
- No se ha validado todavía un proceso concurrente de dos builds.
- La evidencia cubre una carpeta genérica y Cuphead, no todas las
  configuraciones posibles.

## Referencias

- [Gradle incremental build](https://docs.gradle.org/current/userguide/incremental_build.html)
- [Especificación del CLI](../especificaciones/cli-empaquetado.md)

## Ejecuciones asociadas

- [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md)
