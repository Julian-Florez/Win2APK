# 17 - Ruta de log relativa fuera del repositorio

## Descripción

Un intento de redirigir el log de generación de la matriz utilizó una ruta relativa al repositorio mientras el comando se ejecutaba con directorio de trabajo temporal.

## Contexto técnico

| Campo | Valor |
|---|---|
| Fecha | 2026-08-30 |
| Herramienta | Bash y Node.js del entorno de trabajo |
| Publicación | N/A |
| Dispositivo / Android / ABI | N/A |
| Ejecución asociada | [EXEC-022](../ejecuciones/22-revision-bibliografia-local-20260830/matriz.md) |

## Reproducción o evidencia

Comando intentado desde el directorio temporal /tmp/win2apk-sheet:

    /home/julian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node /home/julian/Tesis/Win2APK/ejecuciones/22-revision-bibliografia-local-20260830/scripts/crear_matriz_ampliada.mjs > ejecuciones/22-revision-bibliografia-local-20260830/logs/crear_matriz_ampliada.log 2>&1

Mensaje exacto:

    /nix/store/bwry105b7v5jspr41bx9x3fcfqsmfkq2-bash-interactive-5.3p15/bin/bash: line 1: ejecuciones/22-revision-bibliografia-local-20260830/logs/crear_matriz_ampliada.log: No such file or directory

## Impacto

El proceso no se inició por la falla de redirección y no se modificó la matriz. La salida ya había sido generada correctamente en el intento anterior.

## Análisis técnico

La ruta del log se resolvió desde el directorio temporal, no desde la raíz del repositorio. Es una limitación de invocación del comando, no de la matriz ni del script Node.

## Solución aplicada

Se utilizará una ruta absoluta para el log o se ejecutará la redirección desde la raíz del repositorio.

## Resultado

La matriz ampliada existente conserva las hojas y conteos generados. La corrección solo afecta el registro de la nueva ejecución del generador.

## Limitaciones pendientes

Ninguna sobre el archivo de salida. La lectura completa y la validación de los candidatos continúan pendientes.

## Referencias

- [Script de generación de matriz](../ejecuciones/22-revision-bibliografia-local-20260830/scripts/crear_matriz_ampliada.mjs)

## Ejecuciones asociadas

- [EXEC-022 - Revisión de bibliografía local](../ejecuciones/22-revision-bibliografia-local-20260830/matriz.md)
