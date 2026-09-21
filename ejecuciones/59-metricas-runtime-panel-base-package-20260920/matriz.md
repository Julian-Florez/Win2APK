# EXEC-059: Carga de Container-1 y apertura del panel lateral mediante Atrás en la variante Material 3 con applicationId base

- **Run de métricas:** `RUN-20260920-010`
- **Fecha:** 2026-09-20
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** Aprobado experimentalmente para la observación visual del runtime y su panel lateral
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `com.winlator` | Parámetro de ejecución |
| Publicación/hash | `da86dbfdd270ef588b4a62fd2274bf9c056cf7f4fc9e73005882bbacb83b2487` | SHA-256 del artefacto |
| Método | `cold` | Automatización de la skill |
| Escenario | `runtime-panel-base-package` | Carga de Container-1 y apertura del panel lateral mediante Atrás en la variante Material 3 con applicationId base |
| Estado esperado | loading | Hipótesis previa; no sustituye la observación |
| Duración | 30 s por dispositivo | Reloj monótono del host |
| Intervalo | 1.0 s | Muestreo ADB |
| Captura canónica | T+1 s | Pantalla real sin navegación automática |

## Observación

- En Redmi Note 8, orientación horizontal, la carga muestra `Starting up...` y después de Atrás el panel lateral queda abierto con el escritorio Wine atenuado.
- En Lenovo TB-J606F, orientación vertical, la carga muestra `Starting up...` y el panel lateral queda abierto con el escritorio Wine atenuado.
- El panel contiene `Keyboard`, `Input Controls`, `Toggle Fullscreen`, `Task Manager`, `Active Windows`, `Magnifier`, `Screen Effect`, `PiP Mode`, `Touchpad Help` y `Exit`.
- Los tiempos de captura y métricas de FPS/RAM/CPU no se registraron en esta interacción manual; se conservan como `N/R`.

## Interpretación

La actividad de runtime y el drawer lateral son observables en ambos dispositivos cuando la variante se instala con el identificador base `com.winlator`, que coincide con las rutas usadas por el rootfs. La evidencia solo respalda esta combinación de artefacto, configuración y dispositivos.

## Decisión

La interfaz del panel lateral queda verificada visualmente en ambas orientaciones. La variante `com.win2apk.ui.preview` no debe usarse para concluir sobre la ejecución del runtime porque sus rutas de paquete no coinciden con las del rootfs.

## Evidencia

- [Datos estructurados](../../metricas/runs/RUN-20260920-010)
- Redmi Note 8: [carga](./evidencias/redmi-loading.png), [panel tras Atrás](./evidencias/redmi-panel-back.png), [log](./logs/redmi-manual-runtime-panel.log).
- Lenovo TB-J606F: [carga](./evidencias/lenovo-loading.png), [panel tras Atrás](./evidencias/lenovo-panel-back.png), [log](./logs/lenovo-manual-runtime-panel.log).
- Las capturas clasificadas y los CSV del run se conservan en `metricas/runs/RUN-20260920-010/`.
