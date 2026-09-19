# EXEC-045: Verificación posterior de procesos Cuphead con v48 en cuatro dispositivos

- **Fecha:** 2026-09-19
- **Tipo:** verificación ADB puntual posterior a las instalaciones frías
- **Artefacto:** v48, mismo APKS usado en EXEC-041 a EXEC-044
- **Método:** consulta no destructiva de `pidof Cuphead.exe`; sin root
- **Resultado general:** proceso del juego observado en los cuatro dispositivos

## Condiciones y alcance

Esta comprobación no reemplaza las matrices de instalación fría ni extiende
retrospectivamente su ventana de 300 segundos. Solo responde si el ejecutable
del juego estaba vivo después de que terminaron esas mediciones.

## Resultado

| Dispositivo | Serial | PID observado | Estado |
|---|---|---:|---|
| Pixel 9a | `pixel-9a` | 20707 | `Cuphead.exe` vivo |
| Lenovo TB-J606F | `lenovo-tb-j606f` | 18381 | `Cuphead.exe` vivo |
| Redmi Note 8 | `redmi-note-8` | 30137 | `Cuphead.exe` vivo |
| Xiaomi Mi A3 | `mi-a3` | 28511 | `Cuphead.exe` vivo |

## Interpretación

La consulta confirma que los cuatro dispositivos terminaron ejecutando el
juego. En particular, el Redmi no debe clasificarse como cierre: su ejecución
ocurrió después de la ventana automatizada de 300 segundos de `EXEC-043`, por
lo que su tiempo exacto hasta el primer frame queda `N/R` en esa ejecución.

## Evidencia

- [Salida exacta de ADB](./evidencias/pidof-cuphead-20260919T161203-0500.txt)
- [EXEC-041: Pixel](../41-metricas-legacy-exec-api28-pagesizecompat-v48-pixel-cold-install-20260919/matriz.md)
- [EXEC-042: Lenovo](../42-metricas-legacy-exec-api28-pagesizecompat-v48-lenovo-cold-install-20260919/matriz.md)
- [EXEC-043: Redmi](../43-metricas-legacy-exec-api28-pagesizecompat-v48-redmi-cold-install-20260919/matriz.md)
- [EXEC-044: Mi A3](../44-metricas-legacy-exec-api28-pagesizecompat-v48-mi-a3-cold-install-20260919/matriz.md)
