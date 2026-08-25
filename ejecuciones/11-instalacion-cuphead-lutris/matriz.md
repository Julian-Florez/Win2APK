# Ejecución 11: instalación visible de Cuphead mediante Lutris

- **ID:** `EXEC-011`
- **Fecha:** 2026-08-24
- **Tipo:** instalación controlada y observación de cambios
- **Resultado general:** Aprobado para revisión de carpeta; ejecución del juego pendiente
- **Método:** instalación visible de `setup.exe` desde Lutris mediante UMU y GE-Proton

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | Carpeta local declarada por el usuario |
| Versión | N/R | No se ha confirmado desde el instalador |
| Ejecutable | `setup.exe` | `/home/julian/Tesis/Win2APK/cuphead/setup.exe` |
| Publicación/hash | N/R | No calculado en esta ejecución |
| Método | Manual, visible | Ventana del instalador mostrada al usuario |
| Entorno | Lutris `0.5.22`, UMU, GE-Proton | Procesos observados |
| Versión de Winlator | N/A | No es una prueba en Android/Winlator |
| Contenedor/configuración | Prefijo Wine `win64` | `/home/julian/Games/cuphead` |
| Dispositivo/variante | N/A | Equipo Linux de instalación |
| Android/API | N/A | No aplica |
| ABI | N/A | No aplica |
| Resolución | N/R | No registrada |
| Fecha y hora de inicio | 2026-08-24 13:39, aproximadamente | Hora local observada en el proceso |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Instalación | Aprobada | 5,5 GB; 815 archivos observados | Destino `C:\Program Files\Cuphead` | [log](./logs/instalacion.md) | El instalador terminó y no quedaron procesos de instalación activos |
| M-02 | Primer inicio | Aprobado provisional | Proceso activo; log Unity disponible | Lutris + GE-Proton11-5-x86_64 | [log](./logs/instalacion.md) | Direct3D 11 e inicialización del juego observadas |
| M-03 | Aperturas posteriores | N/R | N/R | Requiere primer inicio | N/R | Pendiente |
| M-04 | Operación básica | N/R | N/R | Requiere ejecutar el juego | N/R | Pendiente |
| M-05 | Aislamiento de archivos | Aprobado provisional | Prefijo `/home/julian/Games/cuphead` | Prefijo Lutris dedicado | [log](./logs/instalacion.md) | Los archivos del juego quedaron bajo `drive_c/Program Files/Cuphead`; las cachés y logs de primer inicio quedaron fuera de la publicación |
| M-06 | Persistencia de archivos | N/R | N/R | Requiere finalizar y reabrir | N/R | Pendiente |
| M-07 | Tamaño del APK | N/A | N/R | Esta ejecución no compila APK | N/A | Se medirá en una ejecución posterior |
| M-08 | Tiempo de instalación | Observado | Aproximadamente 10 min 07 s | Desde el lanzamiento de comandos de Lutris hasta su código 0 | [log](./logs/instalacion.md) | Medición basada en marcas del log de Lutris; no incluye preparación previa |
| M-09 | Tiempo de primer inicio | N/R | N/R | Requiere terminar la instalación | N/R | Pendiente |
| M-10 | Tiempo de aperturas posteriores | N/R | N/R | Requiere primer inicio | N/R | Pendiente |
| M-11 | Tasa de éxito | N/R | N/R | Numerador/denominador aún no definidos para esta prueba | N/R | Pendiente |
| M-12 | Pasos manuales | Registrados parcialmente | N/R | Instalador visible y selección de ruta | [log](./logs/instalacion.md) | Se desmarcaron acciones opcionales de actualización web/DirectX y lanzamiento automático antes de pulsar Finish |

## Fallos y decisiones

- **Limitación relacionada:** La instalación previa con Wine 11.0 temporal no avanzó; véase [Limitación 07](../../limitaciones/07-instalador-cuphead-no-avanza-en-wine.md).
- **Mensaje exacto:** N/A en esta ejecución.
- **Decisión:** Conservar esta carpeta como candidata para el asset de Win2APK. Antes de empaquetar se debe probar el ejecutable con el runner y excluir temporales o auxiliares no requeridos.

## Evidencias

- Captura: N/A
- Log: [registro de observación](./logs/instalacion.md)
- Hash/configuración: N/R

## Repetibilidad y pendientes

- [x] Registrar el resultado final de la instalación.
- [x] Confirmar `Cuphead.exe`, `Cuphead_Data` y tamaño de la carpeta final.
- [x] Revisar dependencias, accesos directos y archivos temporales que deban excluirse.
- [x] Probar el ejecutable con el mismo prefijo.
- [ ] Generar el asset `.tzst` y configurar Win2APK solo después de validar la carpeta.
