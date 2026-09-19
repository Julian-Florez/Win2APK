# Fuentes de componentes y variantes revisadas

| Componente | Fuente | Variante consultada | Resultado para F-03 |
|---|---|---|---|
| BCn compute layer | [leegao/bcn_layer](https://github.com/leegao/bcn_layer) | release `shader-v3`, SHA del `.so` `31b3b8ece28a7a7beeb53c882defb56c5b22bebb916f0909b4b45ccb1b9c20e9` | Se cargó, pero F-03 terminó por `LOW_MEMORY` |
| DXVK-Sarek | [Winlator-CMOD](https://github.com/Stredohori/Winlator-CMOD) | asset `1.11.1-sarek`, SHA `ce37f7d779e1f9ec51bc01997a7bedc31ad5e5c16f96c26840f9389f034fe3f2` | El ejecutable llegó a iniciar |
| WinlatorMali | [GunaCharanTeja/WinlatorMali](https://github.com/GunaCharanTeja/WinlatorMali) | `leegao_bcn.tzst`, variante modificada por Fcharan/WinMali-Dev con ETC2/ASTC | Reservada para F-04 |
| Vortek patcher | [leegao/vortek-patcher](https://github.com/leegao/vortek-patcher/releases) | hotfix con soporte anunciado para Adreno 6xx y posiblemente Mali | No se inyectó el APK fork completo en `com.cuphead` |

La lista documenta investigación y no implica que cada fork sea intercambiable con el rootfs de Win2APK.
