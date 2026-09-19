# Build v41

```text
nix shell nixpkgs#jdk17 -c bash ./gradlew :app:bundleDebug
BUILD SUCCESSFUL in 3m 43s
45 actionable tasks: 20 executed, 25 up-to-date
```

| Artefacto | Tamaño | SHA-256 |
|---|---:|---|
| `app-debug.aab` | N/R | N/R |
| `cuphead-v41-base.apks` | `273711346` bytes | `682f12f49f37ca14ff03aebb1280d8301e44e3767ba55ab303f5d5742627e82d` |
| `universal.apk` base-only | `273711050` bytes | `01b2c6663cc5b364acf331f7fac9937bafb35242bd1d5232bb2b08019cc01a1a` |

bundletool generó el APKS universal con el keystore debug del entorno. Se extrajo e instaló solo `universal.apk`; los módulos del payload no se instalaron.

