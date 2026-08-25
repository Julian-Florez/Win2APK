# Bundletool no firma el asset pack único de Cuphead por el tamaño ZIP

## Descripción

La compilación `bundleDebug` genera un AAB con un asset pack `install-time`, pero `bundletool 1.18.3` no logra producir el conjunto `.apks` para instalación local cuando el pack contiene el `cuphead.tzst` completo de `4.782.573.186` bytes.

## Observación

Durante `build-apks --local-testing --connected-device`, bundletool falla en la firma con:

`ZIP Central Directory overlaps with End of Central Directory. CD end: 8589934590, EoCD start: 4782574132`

El AAB se generó antes de este paso. No se instaló la aplicación en la Lenovo TB-J606F.

## Evidencia

La reproducción completa está en [EXEC-013](../ejecuciones/13-bundletool-cuphead-aab/matriz.md) y el mensaje exacto en su [log](../ejecuciones/13-bundletool-cuphead-aab/logs/bundletool.md).

## Interpretación

La evidencia acota el problema a la transformación/firma ZIP del asset pack grande en la ruta local de bundletool. No permite atribuir el fallo al ejecutable de Cuphead, al prefijo Wine ni a la capacidad de almacenamiento del dispositivo. El límite interno exacto de bundletool/apksig no se determina solo con esta ejecución.

## Decisión

No se usará un único asset pack de más de 4 GiB para la prueba local. El siguiente intento dividirá el stream Zstandard en tres packs install-time de menos de 2 GiB cada uno y lo concatenará en memoria de lectura antes de la extracción.

## Estado

Resuelta experimentalmente para la prueba local mediante tres asset packs: [EXEC-014](../ejecuciones/14-aab-segmentado-cuphead-lenovo/matriz.md) generó el APK set, lo instaló con bundletool y arrancó `Cuphead.exe`. El asset pack único de más de 4 GiB sigue sin ser una variante utilizable en esta ruta.
