# Registro de retiro de splits

## Comando aceptado por Package Manager

```text
pm uninstall --user 0 com.cuphead cuphead_data_01
Success
```

La misma forma devolvió `Success` para `cuphead_data_02` y `cuphead_data_03`.

## Estado final del paquete

```text
splits=[base, config.arm64_v8a, config.es, config.hdpi]
code: 268724736 bytes (256,28 Mb)
data: 7161323520 bytes (6,67 Gb)
apk: 268439230 bytes (256,00 Mb)
```

Antes del retiro se registraron `5.056.035.328` bytes de código instalado.

## Extracción conservada

```text
rootfs: 6732318 KiB
Cuphead: 5715382 KiB
rootfs_file_count: 5677
cuphead_file_count: 804
```

## Relanzamiento

```text
pack=cuphead_data_01 location=null
pack=cuphead_data_02 location=null
pack=cuphead_data_03 location=null
Unable to create the configured container or shortcut.
```

