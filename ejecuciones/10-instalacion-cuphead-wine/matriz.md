# Ejecución 10: instalación controlada de Cuphead mediante Wine

- **ID:** `EXEC-010`
- **Fecha:** 2026-08-24
- **Tipo:** instalación controlada y preparación de publicación Windows
- **Resultado general:** No aprobado: el instalador quedó sin progreso durante la descompresión
- **Aplicación:** Cuphead
- **Versión:** N/R
- **Ejecutable:** N/R; la instalación no terminó
- **Método:** instalación automatizada de `setup.exe` en un prefijo Wine temporal
- **Instalador:** `cuphead/setup.exe` con `fg-01.bin` a `fg-04.bin`
- **Copia legal:** declarada por el usuario

## Objetivo

Obtener una carpeta instalada de Cuphead, identificar el ejecutable principal y registrar las dependencias necesarias para empaquetar posteriormente la publicación como asset de Win2APK.

## Condiciones

| Elemento | Valor |
|---|---|
| Sistema de compilación | Linux; versión exacta N/R |
| Wine | `wine-11.0` aislado mediante Nix; pendiente de confirmar el resultado de la instalación |
| Prefijo | Temporal fuera del repositorio; ruta N/R hasta finalizar el intento |
| Pantalla | `DISPLAY=:0` |
| Dispositivo Android | N/A en esta ejecución |
| Winlator | N/A en esta ejecución |
| ABI | N/A en esta ejecución |

## Matriz de observaciones

| Métrica | Resultado | Evidencia | Interpretación |
|---|---|---|---|
| Inicialización del prefijo Wine | Aprobada | `/tmp/win2apk-cuphead-exec010-20260824` | Se creó un prefijo `win64` con Wine 11.0 |
| Ejecución del instalador | Parcial | [log](./logs/instalacion.md) | El instalador inició y creó el destino |
| Instalación completa | No aprobada | [Limitación 07](../../limitaciones/07-instalador-cuphead-no-avanza-en-wine.md) | No terminó la descompresión |
| Carpeta instalada | Parcial | [log](./logs/instalacion.md) | Solo contiene auxiliares, `_Redist` y `01.fgpack.x2` vacío |
| Ejecutable principal | N/R | N/A | No se obtuvo una publicación válida |
| Tamaño de la carpeta instalada | N/R | N/A | El prefijo completo ocupó aproximadamente `1016M`; no representa el tamaño del juego |
| Dependencias adicionales | N/R | N/A | No se debe inferir desde la instalación incompleta |
| Ejecución posterior del juego | N/R | N/R | Se verificará por separado si la instalación termina |
| Asset `.tzst` generado | N/A | N/A | Esta ejecución se limita a preparar y revisar la carpeta |
| APK generado | N/A | N/A | Esta ejecución no compila todavía la APK |

## Decisión

No usar esta instalación parcial para generar el asset. Repetir con otra versión o entorno de Wine, o partir de una carpeta instalada en Windows.

## Pendientes

- Confirmar la carpeta final y el ejecutable en una instalación que termine.
- Revisar si el instalador agregó redistribuibles, accesos directos o archivos que no deban entrar en el asset.
- Empaquetar la carpeta instalada y configurar `config/win2apk.json` en una ejecución posterior.
- Investigar la incompatibilidad del descompresor con este Wine; véase [Limitación 07](../../limitaciones/07-instalador-cuphead-no-avanza-en-wine.md).
