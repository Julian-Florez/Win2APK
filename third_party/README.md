# Componentes gráficos de terceros

Esta carpeta registra el origen de los binarios gráficos añadidos para la
prueba `EXEC-024`. No contiene el instalador ni archivos de datos de Cuphead.

## `bcn-layer-leegao-shader-v3.tzst`

- Proyecto: [leegao/bcn_layer](https://github.com/leegao/bcn_layer)
- Referencia: rama `shader-v3`, release `shader-v3`
- Archivo de origen: `libbcn_layer.so.zip`
- Uso: capa Vulkan que decodifica texturas BCn mediante compute shader; la
  configuración de esta rama solicita transcodificación ETC2 sólo para la
  ruta Vortek/Mali.
- SHA-256 de `libbcn_layer.so`: `31b3b8ece28a7a7beeb53c882defb56c5b22bebb916f0909b4b45ccb1b9c20e9`
- SHA-256 del archivo empaquetado en assets:
  `2faf9a91ca99b9277a921b55dbab2781c4fded10f8046477988c0f9b1855d5c8`
- Licencia declarada por el proyecto: MIT; se conserva el aviso de licencia
  en esta documentación y en el enlace de origen.

## `dxvk-1.11.1-sarek.tzst`

- Proyecto de origen del asset: [Stredohori/Winlator-CMOD](https://github.com/Stredohori/Winlator-CMOD)
- Referencia local consultada: commit `26f65e9f82cc314a4c1f2656f2c76786c59bf68f`
- Asset de origen: `app/src/main/assets/dxwrapper/dxvk-1.11.1-sarek.tzst`
- SHA-256 del archivo empaquetado en assets:
  `ce37f7d779e1f9ec51bc01997a7bedc31ad5e5c16f96c26840f9389f034fe3f2`
- El repositorio consultado declara licencia MIT. La variante se usa como
  componente experimental para D3D11 en la GPU Mali; no reemplaza DXVK del
  perfil Turnip de Adreno.

## Alcance de la prueba

Los dos archivos se incorporan como componentes built-in del prototipo y se
extraen dentro del rootfs del contenedor. Su presencia no copia ni duplica el
árbol de 815 archivos del juego. El resultado de compatibilidad debe
considerarse específico de la combinación Pixel 9a, Android/API y driver
observada en `EXEC-024` hasta que existan mediciones equivalentes en los cuatro
dispositivos.

## Variante F-04: `bcn-layer-winmali-fcharan-5c168f4.tzst`

- Proyecto de origen: [GunaCharanTeja/WinlatorMali](https://github.com/GunaCharanTeja/WinlatorMali)
- Rama consultada: `bionic-mali-1.0`
- Asset: `app/src/main/assets/graphics_driver/leegao_bcn.tzst`
- SHA-256 del asset: `4c30fbaacd7f7e46e906f38c9564bdfbc50b95cca9c3ff6dab2d92130552cd0c`
- SHA-256 de `usr/lib/libbcn_layer.so`: `44115e67673eb0a7f2a2aac9d1a399edab3a1f43721d0b6f80f8db7fa0c06b47`
- `version.txt` lo describe como una variante modificada de Leegao por
  Fcharan/WinMali-Dev, con correcciones y detección para Mali, incluyendo ETC2.
- La variante conserva la licencia MIT declarada por el repositorio de origen.

## DXVK-Sarek 1.12.1

- Proyecto de origen: [GunaCharanTeja/WinlatorMali](https://github.com/GunaCharanTeja/WinlatorMali), rama `bionic-mali-1.0`.
- Asset: `app/src/main/assets/dxwrapper/dxvk-1.12.1-sarek.tzst`.
- SHA-256 del asset: `715a37bc6e4d9a8f7270af50ac042fa04084f709e04625a2efd01d1234eba8a1`.

## DXVK 1.7.2 para el perfil Mali

- Proyecto de origen del asset: [GunaCharanTeja/WinlatorMali](https://github.com/GunaCharanTeja/WinlatorMali), rama `bionic-mali-1.0`.
- Commit consultado: `fbf42d26411444249a301086da0dcb652b861b17`.
- Asset: `app/src/main/assets/dxwrapper/dxvk-1.7.2.tzst`.
- SHA-256 del asset: `d2c23ad3b0e622368bf2ef2de4904e98cb03f241431f1789b6868e01daf28c8a`.
- Motivo de incorporación: es la versión DXVK predeterminada declarada por ese fork orientado a Mali. En Win2APK se prueba de forma aislada después de que DXVK 2.4.1 redujera la memoria del Pixel pero produjera una pantalla negra.
- Alcance: componente experimental para la ruta Vortek/Mali; el selector Adreno no cambia.

## Perfil histórico del Pixel: Leegao `c4755eef` y DXVK-Sarek 1.13.0

- Catálogo de la capa BCn: [The412Banner/winlator-contents](https://github.com/The412Banner/winlator-contents), entrada `bannerlator-bcn-leegao`.
- Asset de origen BCn: `bcn-leegao.tzst` de `wrappers-v1`.
- SHA-256 del asset BCn: `6ae12eacfe5d228e588569a51e28d9f65b54f7988d6aca835f7dc864636c41fb`.
- SHA-256 de `usr/lib/libbcn_layer.so`: `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`.
- La huella del binario coincide con la registrada en `EXEC-020` para el perfil ETC2 jugable del Pixel.
- Asset de origen DXVK: `dxvk-sarek-v1.13.0.wcp`, publicado por The412Banner/Nightlies.
- SHA-256 del WCP: `7e792940c6ca9793ce9fb61aa8684b4fad7b72a207e84eb07b5f0edd95f41ba7`.
- SHA-256 del asset DXVK normalizado para Winlator: `94ccf1062ccaccd1411db708f026072e37b33fe686c6e76731e81fc67902a968`.
- El WCP identifica la versión como DXVK-Sarek 1.13.0 `Pacemaker`, orientada a Vulkan 1.1/1.2 y GPU de recursos limitados.
- Uso en Win2APK: restauración controlada del perfil Pixel; el selector Adreno y sus assets no cambian.

## Capa Android empaquetada para v45

- `app/src/main/jniLibs/arm64-v8a/libVkLayer_BCN_BCnLayer.so` es el shim Android probado en `EXEC-031`, SHA-256 `053b2815e832961d1f3ad4c4be18eb6cd1a99c1a430a08e8784ed4920457d565`.
- `app/src/main/jniLibs/arm64-v8a/libbcn_layer.so` es el binario Leegao `c4755eef`, SHA-256 `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`.
- Las bibliotecas se empaquetan en el directorio nativo de la aplicación. Vortek consulta `vkEnumerateInstanceLayerProperties` y solicita `VK_LAYER_BCN_BCnLayer` durante `vkCreateInstance` cuando está disponible.
- Esta ruta reemplaza, para Vortek, la extracción de BCn dentro del rootfs. La publicación debe verificarse con los ajustes globales de depuración GPU desactivados.
