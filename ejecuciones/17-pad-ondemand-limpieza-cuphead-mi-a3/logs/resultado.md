# Build y resultado del Mi A3

## Build

```text
JAVA_HOME=<JDK 17> ANDROID_HOME=<Android SDK> bash gradlew :app:compileDebugJavaWithJavac --no-daemon
BUILD SUCCESSFUL

bash gradlew :app:bundleDebug --no-daemon
BUILD SUCCESSFUL
```

## Descarga y lectura

```text
pack=cuphead_data_01 status=4 downloaded=1800008100 total=1800008100 error=0
pack=cuphead_data_02 status=4 downloaded=1800008100 total=1800008100 error=0
pack=cuphead_data_03 status=4 downloaded=1182581156 total=1182581156 error=0
opening on-demand asset path=.../cuphead_data_01.part exists=true size=1800000000
opening on-demand asset path=.../cuphead_data_02.part exists=true size=1800000000
opening on-demand asset path=.../cuphead_data_03.part exists=true size=1182573186
```

## Limpieza y relanzamiento

```text
removed source asset pack=cuphead_data_01
removed source asset pack=cuphead_data_02
removed source asset pack=cuphead_data_03
local-testing source cleanup path=/storage/emulated/0/Android/data/com.cuphead/files/local_testing removed=true existsAfter=false
application installation already complete; skipping asset extraction
Starting: ... box64 wine ... /dir C:\\Cuphead "Cuphead.exe"
```

Mediciones finales:

```text
files/rootfs: 6732416 KiB
files/assetpacks: 28 KiB
/sdcard/Android/data/com.cuphead: 7 KiB
```

