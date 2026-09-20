# 36. El firmador de AGP agota la memoria con AAB multigigabyte

## Descripción

El primer build completo de Cuphead generó el bundle intermedio, pero la tarea
de firma de Android Gradle Plugin no pudo cerrar un AAB de aproximadamente
5,5 GB. El fallo ocurrió en el host durante el empaquetado, antes de instalar
el resultado en Android.

## Contexto técnico

- Aplicación: Cuphead.
- `applicationId`: `com.cuphead`.
- Payload: 815 archivos, 5.847.372.363 bytes, 5 asset packs.
- Entorno: Linux x86_64, Gradle 8.7, Android Gradle Plugin 8.5.1.
- Ejecución relacionada: [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md).

## Reproducción o evidencia

La tarea devolvió un agotamiento de memoria al cerrar el AAB:

```text
Caused by: java.lang.OutOfMemoryError
    at com.android.builder.internal.packaging.AabFlinger.close
Caused by: java.lang.OutOfMemoryError: Java heap space
    at com.android.zipflinger.StreamSource
```

La configuración de Gradle disponía de un heap de aproximadamente 2 GB,
insuficiente para la tabla ZIP que AGP mantiene durante esa operación.

## Impacto

El modo de firma de AGP no es viable para payloads multigigabyte en el entorno
probado. Aumentar el heap puede trasladar el problema al límite de memoria del
host y no elimina la necesidad de mantener una representación completa del ZIP.

## Análisis técnico

La tarea `packageReleaseBundle` sí produjo un AAB intermedio. El agotamiento se
concentró en `signReleaseBundle`, no en la planificación ni en la generación
de los asset packs. Esta separación se comprobó al desactivar la firma de AGP y
obtener después un AAB funcional mediante el firmador del JDK.

## Solución aplicada

El motor desactiva la firma de AGP y sus tareas de listado dependientes cuando
`WIN2APK_SIGN_WITH_GRADLE` es falso. El CLI toma el archivo
`intermediary-bundle.aab`, ejecuta el módulo `jdk.jartool` desde Java usando un
archivo de argumentos temporal con permisos `0600`, elimina el archivo temporal
y continúa con `bundletool build-apks`.

## Resultado

Resuelta experimentalmente para el build de Cuphead de `EXEC-047`:

- AAB firmado: 5.494.326.036 bytes.
- APKS generado: 6.424.836.814 bytes.
- `bundletool validate`: aprobado.

El cálculo de SHA-256 se cambió a streaming después de observar que el informe
anterior podía reservar varios gigabytes de RAM leyendo cada artefacto completo.

## Limitaciones pendientes

- La firma externa genera un certificado autofirmado persistente; la clave debe
  respaldarse fuera del repositorio.
- `jarsigner` trabaja sobre el ZIP completo y puede tardar varios minutos.
- No se ha comparado este flujo con una publicación en Google Play.

## Referencias

- [jarsigner — documentación del JDK](https://docs.oracle.com/en/java/javase/17/docs/specs/man/jarsigner.html)
- [Android App Bundle](https://developer.android.com/guide/app-bundle)

## Ejecuciones asociadas

- [EXEC-047](../ejecuciones/47-cli-empaquetado-testapp-cuphead-20260919/matriz.md)
