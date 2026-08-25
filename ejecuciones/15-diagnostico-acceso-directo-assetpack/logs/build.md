# Log de build — EXEC-015

Comando ejecutado con JDK 17:

```text
nix shell nixpkgs#jdk17 --command env JAVA_HOME=... ANDROID_HOME=/home/julian/Android/Sdk ANDROID_SDK_ROOT=/home/julian/Android/Sdk bash gradlew bundleDebug --console=plain
```

Resultado:

```text
BUILD SUCCESSFUL in 2m 40s
43 actionable tasks: 21 executed, 22 up-to-date
```

Advertencias existentes del proyecto: Android Gradle Plugin 7.2.2 con compile SDK 34 y sustituciones no posicionales en algunos recursos. No impidieron el build.
