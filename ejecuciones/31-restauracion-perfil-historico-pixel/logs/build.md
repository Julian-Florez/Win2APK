# Compilación e instalación de v44

## Compilación

- Fecha: 2026-09-18.
- Variante: `versionCode=44`, `versionName=11.1-direct-files-auto-gpu-recovery-v14-pixel-sarek1130-leegao-etc2`.
- Primer intento: JDK 21; falló durante R8 con `java.lang.NullPointerException` al procesar `ControlsProfile.class`.
- Repetición limpia con JDK 21: reprodujo el mismo fallo.
- Comando que completó la compilación: `nix shell nixpkgs#jdk17 -c bash ./gradlew :app:bundleDebug`.
- Resultado: `BUILD SUCCESSFUL in 3m 43s`, 45 tareas.

El fallo con JDK 21 se registra como una diferencia de herramienta de compilación. No se atribuye al perfil gráfico porque el mismo árbol fuente compiló con JDK 17.

## Artefactos

| Artefacto | Tamaño | SHA-256 |
|---|---:|---|
| Conjunto `.apks` base-only de bundletool | N/R | `25acc85517ff2b0245dbec1b5ba47d5e46fc2f016781b53e72b94c32f26738d5` |
| `universal.apk` extraído | 287105232 bytes | `e76556dc5b2fdd928b43610525196ab8fbdb4e4cb1f671a70fc5656bea62d2c0` |

## Instalación

- Método: `adb install -r` del APK universal extraído del conjunto base-only.
- Dispositivo: Pixel 9a, serial `4A021JEBF06953`.
- Resultado: `Success`.
- Duración observada del comando: 10562 ms.
- Versión confirmada por `dumpsys package`: `versionCode=44`, `versionName=11.1-direct-files-auto-gpu-recovery-v14-pixel-sarek1130-leegao-etc2`.
- Staging `local_testing`: ausente.

La instalación fue una actualización sobre los datos existentes. Esta ejecución no demuestra por sí sola un primer inicio desde cero.
