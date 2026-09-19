# 28. Consumo local de artefactos y objetos Git en el fork Winlator

## Descripción

El checkout del fork de Winlator consumió almacenamiento hasta dificultar nuevos builds. El síntoma se atribuyó inicialmente a Git LFS, pero la inspección local no encontró Git LFS activo en las referencias del fork.

## Contexto técnico

- Proyecto: `/home/julian/Tesis/Win2APK`.
- Fork principal: `winlator`, remoto `julian` en `https://github.com/Julian-Florez/winlator.git`.
- Submódulo de aplicación: `winlator/app`, remoto `julian` en `https://github.com/Julian-Florez/winlator-app.git`.
- Ramas observadas: `agent/winlator-core-dynamic-package` y `codex/no-duplicate-game-data`.
- Ejecución asociada: [EXEC-032](../ejecuciones/32-limpieza-git-winlator/matriz.md).

## Reproducción o evidencia

Antes de la limpieza se observaron:

- `winlator/`: `68G`.
- `winlator/app/build/`: `45G`.
- `winlator/app/app/build/`: `18G`.
- `winlator/app/app/.cxx/`: `56M`.
- `.git/`: `3.9G`.
- Espacio libre: `171G`.

El mensaje exacto de la herramienta ausente fue:

```text
git: 'lfs' is not a git command.

The most similar command is
	refs
```

No se encontró `.gitattributes` en el checkout ni un puntero con `version https://git-lfs.github.com/spec/v1`. La configuración global sí contiene filtros `filter.lfs.*`, pero eso no prueba que este fork use LFS.

## Impacto

Las salidas de compilación duplicaron archivos grandes entre APKs, AABs e intermediarios. El historial Git raíz también retenía blobs inalcanzables de aproximadamente `2.90 GB` y `0.93 GB`. El fork conservaba aproximadamente `1.3G` de historial Git alcanzable, sin objetos inalcanzables equivalentes.

## Análisis técnico

La observación separa dos fuentes:

1. Las carpetas `build/` y `.cxx/` eran artefactos regenerables e ignorados por Git. No eran objetos LFS.
2. El `.git` raíz contenía objetos Git normales que ya no eran alcanzables desde ramas, etiquetas ni reflogs. La causa más probable es historial local abandonado por intentos anteriores. Se mantiene como hipótesis local porque no se inspeccionó el panel remoto del proveedor.

## Solución aplicada

Se verificó la lista con `git clean -ndX` y se retiraron únicamente estas rutas del submódulo `winlator/app`:

- `build/`.
- `app/build/`.
- `app/.cxx/`.

Después se ejecutó `git gc --prune=now` en el repositorio raíz y la limpieza equivalente en `winlator/app`. No se modificaron ramas, etiquetas, remotos ni archivos de código. Se conservaron los tres directorios locales `cuphead_data_*`.

## Resultado

Después de la limpieza:

- `winlator/`: `6.4G`.
- `.git/`: `203M`.
- Espacio libre: `236G`.
- Las tres rutas de build: ausentes.
- Objetos inalcanzables en `.`, `winlator` y `winlator/app`: `0`.

El estado de trabajo previo del fork permanece presente. La reducción observada es local; no implica que se haya cambiado el historial publicado en GitHub.

## Limitaciones pendientes

- No se verificó una cuota o almacenamiento remoto de Git LFS en GitHub porque el checkout no contiene referencias LFS y no se dispone de una medición del panel del proveedor.
- El ejecutable `git-lfs` sigue sin estar instalado. Si otro repositorio del usuario usa LFS, sus filtros globales pueden producir el mismo mensaje hasta instalar la herramienta.
- Los siguientes builds volverán a generar archivos grandes si no se limpian después de cada intento.

## Referencias

- [EXEC-032](../ejecuciones/32-limpieza-git-winlator/matriz.md)
- [Registro de limpieza](../ejecuciones/32-limpieza-git-winlator/logs/limpieza.md)
- [Configuración del submódulo `winlator/app`](../winlator/app/.gitignore)

## Ejecuciones asociadas

- [EXEC-032](../ejecuciones/32-limpieza-git-winlator/matriz.md)
