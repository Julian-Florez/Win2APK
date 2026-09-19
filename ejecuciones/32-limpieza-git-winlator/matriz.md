# Limpieza local de Git y artefactos de compilación del fork Winlator

- **ID:** `EXEC-032`
- **Fecha:** `2026-09-18`
- **Tipo:** automatizada
- **Resultado general:** aprobado
- **Método:** inspección de Git y del sistema de archivos, previsualización con `git clean -ndX`, limpieza de rutas ignoradas, poda de objetos Git inalcanzables y verificación posterior.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Fork `winlator` y submódulo `winlator/app` | Rutas locales del proyecto |
| Versión | `agent/winlator-core-dynamic-package` en `winlator`; `codex/no-duplicate-game-data` en `winlator/app` | `git rev-parse --abbrev-ref HEAD` |
| Ejecutable | N/A | Limpieza de almacenamiento |
| Publicación/hash | `b78c4b3` en `winlator`; `3e894ed` en `winlator/app` | Estado local observado |
| Método | Automatizado | Comandos Git y `du`/`df` |
| Entorno | Linux local | `/home/julian/Tesis/Win2APK` |
| Versión de Winlator | N/R | No aplica a la limpieza |
| Contenedor/configuración | N/A | No se ejecutó la aplicación |
| Dispositivo/variante | N/A | No se ejecutó la aplicación |
| Android/API | N/A | No se ejecutó la aplicación |
| ABI | N/A | No se ejecutó la aplicación |
| Resolución | N/A | No se ejecutó la aplicación |
| Fecha y hora de inicio | N/R | No se registró la hora exacta |

## Observaciones cuantificadas

| Criterio | Antes | Después | Evidencia |
|---|---:|---:|---|
| Tamaño de `winlator/` | `68G` | `6.4G` | [log de limpieza](./logs/limpieza.md) |
| `winlator/app/build/` | `45G` | Ausente | [log de limpieza](./logs/limpieza.md) |
| `winlator/app/app/build/` | `18G` | Ausente | [log de limpieza](./logs/limpieza.md) |
| `winlator/app/app/.cxx/` | `56M` | Ausente | [log de limpieza](./logs/limpieza.md) |
| `.git/` raíz | `3.9G` | `203M` | [log de limpieza](./logs/limpieza.md) |
| Espacio disponible | `171G` | `236G` | [log de limpieza](./logs/limpieza.md) |
| Objetos inalcanzables en repositorios comprobados | N/R | `0` | [log de limpieza](./logs/limpieza.md) |

## Fallos y decisiones

- **Limitación relacionada:** [28-consumo-local-de-builds-y-objetos-git-winlator.md](../../limitaciones/28-consumo-local-de-builds-y-objetos-git-winlator.md)
- **Mensaje exacto:** `git: 'lfs' is not a git command.`
- **Decisión:** retirar únicamente salidas ignoradas de compilación y podar objetos Git que no fueran alcanzables desde ramas, etiquetas o reflogs. Se conservaron los cambios de código, los assets locales no ignorados y `cuphead_data_01`, `cuphead_data_02` y `cuphead_data_03`.

## Evidencias

- [Registro de inspección y verificación](./logs/limpieza.md)
- Capturas: N/A
- APK/AAB: N/A

## Repetibilidad y pendientes

- [x] Verificar que las tres rutas de compilación estén ausentes.
- [x] Confirmar que Git no reporte objetos inalcanzables en `.`, `winlator` ni `winlator/app`.
- [x] Confirmar que el estado de trabajo del fork conserve sus cambios previos.
- [ ] Confirmar, con acceso al panel del proveedor, si existe una cuota remota de Git LFS independiente de este checkout.
