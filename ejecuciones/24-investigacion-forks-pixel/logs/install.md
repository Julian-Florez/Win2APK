# Actualización del módulo base en Pixel

Condición: paquete `com.cuphead` ya instalado; se conservó el prefijo y no se desinstaló la aplicación.

```text
adb -s 4A021JEBF06953 install -r universal.apk
Performing Streamed Install
Success
install_status=0 elapsed_ms=10034
```

El tiempo corresponde a la actualización del APK base por USB y no al tiempo de instalación inicial ni a la transferencia de los datos del juego.
