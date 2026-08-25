# Referencia obsoleta durante la transición a asset packs segmentados

## Descripción

El primer reintento de compilación después de cambiar de un asset pack a tres módulos falló al evaluar Gradle porque `app/build.gradle` todavía referenciaba `coreAssetPackName` en una condición, aunque la variable había sido reemplazada por `coreAssetPackNames`.

## Mensaje exacto

`Could not get unknown property 'coreAssetPackName' for project ':app' of type org.gradle.api.Project.`

## Corrección y evidencia

Se actualizó la condición para usar `coreAssetPackNames`. El build posterior generó el AAB de [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md), que además fue instalado y ejecutado en el dispositivo.

## Estado

Resuelta experimentalmente; no queda como limitación del diseño segmentado.
