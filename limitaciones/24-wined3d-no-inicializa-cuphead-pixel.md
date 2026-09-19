# WineD3D no inicializa los gráficos de Cuphead en Pixel Tensor/Mali

- **Proyecto:** Win2APK
- **Aplicación:** Cuphead mediante entorno de compatibilidad
- **Estado:** reproducida; variante descartada
- **Fecha de registro:** 2026-09-18

## Descripción

Al reemplazar DXVK por WineD3D en el Pixel 9a, el proceso del juego llegó a
mostrar el diálogo de error de Unity y no inició la escena. La prueba se hizo
como alternativa de recuperación después de observar cierres por memoria con
DXVK; no se interpreta como un fallo de toda versión de WineD3D o de todo
dispositivo Mali.

## Condiciones

| Campo | Valor |
|---|---|
| Dispositivo | Google Pixel 9a, GPU Mali-G715/Tensor |
| Resolución | `800x450` |
| Driver gráfico | Vortek + Gladio |
| Wrapper probado | WineD3D |
| Ejecución asociada | [EXEC-024](../ejecuciones/24-investigacion-forks-pixel/matriz.md), variante F-02 |

## Mensaje exacto

```text
Failed to initialize player
Failed to initialize graphics.
Make sure you have DirectX 11 installed, have up to date drivers for your graphics card and have not disabled 3D acceleration in display settings.
InitializeEngineGraphics failed
```

## Interpretación y decisión

El mensaje confirma que el ejecutable no completó la inicialización de
gráficos bajo esta combinación. La resolución baja no corrigió el problema;
WineD3D se descarta como fallback automático para este Cuphead Unity/D3D11.
Se conserva DXVK como ruta necesaria y se investigan variantes Sarek/BCn por
separado.

## Alcance

No se midieron FPS ni consumo comparable durante esta variante y no se afirma
que WineD3D sea incompatible con todos los juegos o dispositivos Mali.

## Evidencia

- Captura de la sesión: `/tmp/pixel-v33.png` (no se incorpora al repositorio).
- [Matriz EXEC-024](../ejecuciones/24-investigacion-forks-pixel/matriz.md).
