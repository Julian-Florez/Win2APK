# Mapa de publicación

Este checkout contiene dos repositorios de contenido y un superproyecto Git que fija el submódulo de la aplicación.

| Repositorio | Ruta | Rama observada | Remoto que publica el fork |
|---|---|---|---|
| Win2APK | `/home/julian/Tesis/Win2APK` | `codex/no-duplicate-game-data` | `origin` -> `Julian-Florez/Win2APK` |
| Winlator app | `/home/julian/Tesis/Win2APK/winlator/app` | `codex/no-duplicate-game-data` | `julian` -> `Julian-Florez/winlator-app` |
| Winlator manifest | `/home/julian/Tesis/Win2APK/winlator` | `agent/winlator-core-dynamic-package` | `julian` -> `Julian-Florez/winlator` |

`winlator/app` tiene también un remoto `origin` que apunta a `brunodev85/winlator-app`; ese remoto es upstream de lectura y no debe recibir pushes automáticos. El superproyecto tiene la misma precaución con `origin` (`brunodev85/winlator`).

El repositorio raíz ignora `/winlator/`, por lo que los commits de código no se publican desde el repositorio de tesis. El superproyecto sí debe actualizarse cuando cambia el SHA del submódulo `app`; ese commit solo contiene el puntero Git.

Antes de cada publicación, comprobar que estas URL siguen siendo las configuradas localmente. Si cambiaron, detenerse y pedir confirmación en lugar de publicar en un destino nuevo.
