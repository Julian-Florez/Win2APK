# EXEC-048 — Intento de instalación `--fresh` de Cuphead en Mi A3

- **ID:** `EXEC-048`
- **Fecha:** 2026-09-19
- **Tipo:** repetición / instalación automatizada
- **Resultado general:** fallido; intento no ejecutado por una dependencia del entorno
- **Método:** se intentó ejecutar `win2apk install --fresh` sobre el dispositivo USB `51c803a01206`.

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead empaquetado por Win2APK | Archivo `.apks` indicado en el log |
| Versión | `11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core` | Nombre del artefacto |
| Ejecutable | `Cuphead.exe` | Objetivo de ejecución |
| Publicación/hash | N/R | No se registró hash en este intento |
| Método | CLI `win2apk install --fresh` | Comando registrado |
| Entorno | Linux, binario `target/release/win2apk` | Comando registrado |
| Versión de Winlator | N/R | No aplica al fallo previo a la instalación |
| Dispositivo/variante | Xiaomi Mi A3, serial `51c803a01206` | ADB |
| Android/API | N/R | No se necesitó consultar el dispositivo para este intento |
| ABI | N/R | No se necesitó consultar el dispositivo para este intento |
| Resolución | N/R | No se necesitó consultar el dispositivo para este intento |
| Fecha y hora de inicio | `2026-09-19T20:48:02-05:00` | Log |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación | Fallido | Código `127` | El wrapper no inició la instalación | [log de instalación](./logs/01-cli-install-fresh.log) | No se puede atribuir el resultado al APK ni al dispositivo |
| M-02 | Primer inicio | N/A | N/A | La instalación no comenzó | N/A |  |
| M-03 | Aperturas posteriores | N/A | N/A | La instalación no comenzó | N/A |  |
| M-04 | Operación básica | N/A | N/A | La instalación no comenzó | N/A |  |
| M-05 | Aislamiento de archivos | N/A | N/A | La instalación no comenzó | N/A |  |
| M-06 | Persistencia de archivos | N/A | N/A | La instalación no comenzó | N/A |  |
| M-07 | Tamaño del APK | N/A | N/A | No se midió | N/A |  |
| M-08 | Tiempo de instalación | N/A | N/R | El comando terminó antes de instalar | [log de instalación](./logs/01-cli-install-fresh.log) |  |
| M-09 | Tiempo de primer inicio | N/A | N/A | La instalación no comenzó | N/A |  |
| M-10 | Tiempo de aperturas posteriores | N/A | N/A | La instalación no comenzó | N/A |  |
| M-11 | Tasa de éxito | N/A | N/A | No es una muestra válida de instalación | N/A |  |
| M-12 | Pasos manuales | Parcial | N/R | Se identificó el requisito de `bundletool` y del ejecutable auxiliar del entorno | [log de instalación](./logs/01-cli-install-fresh.log) |  |

## Fallos y decisiones

- **Limitación relacionada:** N/A; el fallo corresponde al entorno de ejecución del comando.
- **Mensaje exacto:** `/nix/store/bwry105g7v5jspr41bx9x3fcfqsmfkq2-bash-interactive-5.3p15/bin/bash: line 1: /usr/bin/time: No such file or directory`
- **Decisión:** conservar este intento como registro fallido y repetir la prueba con el binario CLI directo, sin el wrapper que requiere `/usr/bin/time`.

## Evidencias

- [Estado previo del paquete](./logs/00-before-install.log)
- [Intento CLI](./logs/01-cli-install-fresh.log)

## Repetibilidad y pendientes

- [x] Registrar el error exacto.
- [x] Separar este intento del intento válido posterior.
- [ ] Repetir con el CLI ejecutable y `WIN2APK_BUNDLETOOL` configurado.
