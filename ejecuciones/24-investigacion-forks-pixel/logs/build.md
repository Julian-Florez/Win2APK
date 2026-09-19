# Build de la variante F-03

```text
nix shell nixpkgs#jdk17 -c bash ./gradlew :app:bundleDebug
BUILD SUCCESSFUL in 3m 44s
45 actionable tasks: 20 executed, 25 up-to-date
```

Artefactos observados:

| Artefacto | Tamaño | SHA-256 |
|---|---:|---|
| `app-debug.aab` | 5,469,774,837 bytes | `0314c62a927a571a3264a355f12aece5833afa0307016138e57e6f619153c82f` |
| `cuphead-v35-base-pixel.apks` | N/R | `995870972e962a0fc5f515afd4cd3b83836d188387fab5b4873a6028b79e5149` |
| `universal.apk` extraído del módulo base | 267,988,746 bytes | N/R |

El APK universal se generó con bundletool en modo `universal` y `--modules=base`; no contiene una reinstalación del payload de Cuphead.
