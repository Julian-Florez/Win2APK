# Registro de limpieza local

## Observación

El checkout no contiene un archivo `.gitattributes` ni punteros LFS detectables. `git lfs version` devuelve exactamente:

```text
git: 'lfs' is not a git command.

The most similar command is
	refs
```

La configuración global contiene filtros `filter.lfs.*`, pero el fork no los utiliza en sus referencias actuales.

Antes de la limpieza:

```text
68G  winlator/
45G  winlator/app/build/
18G  winlator/app/app/build/
56M  winlator/app/app/.cxx/
3.9G .git/
171G available
```

El análisis de objetos encontró dos blobs Git inalcanzables de aproximadamente `2897000939` y `930106630` bytes en el repositorio raíz. `winlator` no tenía objetos inalcanzables relevantes; `winlator/app` tenía un objeto inalcanzable aislado.

## Acción

Primero se ejecutó una previsualización:

```text
git -C winlator/app clean -ndX -- build app/build app/.cxx
Would remove app/.cxx/
Would remove app/build/
Would remove build/
```

Después se ejecutó la limpieza limitada a esas rutas ignoradas y la poda local:

```text
git -C winlator/app clean -fdX -- build app/build app/.cxx
git gc --prune=now --quiet
git -C winlator/app gc --prune=now --quiet
```

No se eliminó ningún archivo de código, asset no ignorado, rama, etiqueta ni remoto.

## Verificación

```text
6.4G  winlator/
203M  .git/
236G  available
ABSENT winlator/app/build
ABSENT winlator/app/app/build
ABSENT winlator/app/app/.cxx
```

El conteo Git del corte posterior reportó `unreachable_objects=0` para `.`, `winlator` y `winlator/app`. La previsualización posterior de `git clean -ndX` no produjo rutas pendientes.

## Interpretación

El consumo observado era principalmente de salidas de compilación ignoradas y de objetos Git históricos ya abandonados en el repositorio raíz. No se demostró consumo por Git LFS en el fork local. Una cuota remota de Git LFS, si existiera en el proveedor, queda fuera de esta verificación.
