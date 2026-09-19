---
name: win2apk-publicar-repos
description: "Revisar, separar, commitear y publicar cambios de los repositorios Win2APK y Winlator, incluyendo la actualización segura del superproyecto que fija el submódulo app. Usar cuando el usuario pida subir cambios a GitHub, sincronizar las dos partes del proyecto, crear commits separados o automatizar commit y push sin mezclar documentación, código, payloads locales ni artefactos de compilación."
---

# Publicar Win2APK y Winlator

Usar esta skill para mantener separados el repositorio de tesis y el repositorio de la aplicación. La publicación debe ser reproducible: primero revisar el estado, después seleccionar rutas explícitas, luego validar el índice, commitear en orden y finalmente hacer push a los remotos del usuario. No usar `git add -A` en `winlator/app`, porque allí pueden existir payloads locales de Cuphead y resultados de compilación que no pertenecen a Git.

## Mapa de repositorios

Leer [repo-map.md](references/repo-map.md) si las rutas, ramas o remotos no coinciden con este mapa.

| Rol | Ruta | Remoto de publicación por defecto | Contenido |
|---|---|---|---|
| Proyecto y tesis | `/home/julian/Tesis/Win2APK` | `origin` | Documentación, métricas, bitácoras y skills |
| Aplicación | `/home/julian/Tesis/Win2APK/winlator/app` | `julian` | Código, assets de runtime y configuración de Winlator |
| Superproyecto | `/home/julian/Tesis/Win2APK/winlator` | `julian` | Solo fija el commit del submódulo `app` |

El superproyecto no es un tercer conjunto de cambios funcionales: es la referencia necesaria para que `winlator/app` quede fijado en el commit publicado. Si no cambió el puntero `app`, no crear un commit vacío en el superproyecto.

## Flujo obligatorio

1. Confirmar que los tres directorios son repositorios Git independientes, que no están en detached HEAD y que tienen remoto de push. No cambiar de rama, no hacer `reset`, no hacer `clean` y no sobrescribir cambios existentes.
2. Mostrar rama, remoto, estado y rutas modificadas de cada repositorio. Identificar cambios fuera del alcance y detenerse si no se puede distinguir si pertenecen a la tarea.
3. Ejecutar el script en modo de inspección:

   ```bash
   python3 .codex/skills/win2apk-publicar-repos/scripts/publish_repositories.py
   ```

4. Para publicar, pasar un mensaje específico y confirmar la operación mediante `--execute --push`. Usar el remoto `julian` para los repositorios Winlator, nunca `origin` por defecto, porque `origin` apunta al upstream de Bruno Dev.

   ```bash
   python3 .codex/skills/win2apk-publicar-repos/scripts/publish_repositories.py \
     --message "Add device-aware direct-files packaging" \
     --execute --push
   ```

5. El script debe operar en este orden: `winlator/app`, superproyecto `winlator`, y proyecto `Win2APK`. Si un commit o push falla, detenerse y conservar los commits ya creados; informar el repositorio, rama, remoto y comando que falló. Nunca hacer force push.
6. Verificar después de publicar `git status --short --branch`, el commit remoto y el SHA del submódulo `app` desde el superproyecto. Informar los hashes y URLs de las ramas, sin afirmar que una compilación o prueba de dispositivo pasó si no se ejecutó.

## Selección de archivos

El script solo agrega por defecto las rutas del proyecto y las rutas funcionales conocidas de la aplicación. Debe dejar fuera, aunque estén presentes en el árbol de trabajo:

- `cuphead/`, `cuphead_data*`, `cuphead_files_*` y cualquier payload local del juego.
- `app/build/`, `outputs/`, APK, AAB, APKS, keystores, logs temporales y cachés.
- Contraseñas, tokens, claves privadas y archivos generados por herramientas locales.

Si una ruta nueva debe publicarse, añadirla de forma explícita con `--root-path` o `--app-path`, revisar el diff y explicar por qué pertenece al repositorio. No ampliar el alcance con comodines amplios solo para evitar una revisión.

## Mensajes y separación

- Usar un mensaje común breve y específico; el script lo adapta con el rol del repositorio.
- Crear un commit de la aplicación solo con el código y los assets funcionales seleccionados.
- Crear el commit del superproyecto únicamente para actualizar `app` al SHA recién creado.
- Crear el commit del proyecto de tesis con documentación, métricas y la propia skill seleccionadas.
- No mezclar archivos del proyecto de tesis dentro de `winlator/app`, ni código de la aplicación dentro de `Win2APK`.

## Recursos

- `scripts/publish_repositories.py`: inspecciona, selecciona, valida, commitea y opcionalmente hace push por repositorio.
- `references/repo-map.md`: remotos, ramas y reglas específicas de este checkout.
