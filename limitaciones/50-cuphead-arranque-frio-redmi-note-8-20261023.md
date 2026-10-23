# 50. Cuphead permanece cargando en el primer arranque frío del Redmi Note 8

## Descripción

En cinco instalaciones frías consecutivas de Cuphead en el Xiaomi Redmi Note 8,
Bundletool terminó correctamente (204.656 s, 206.969 s, 208.067 s, 207.993 s y
207.886 s en `RUN-20261023-037` a `RUN-20261023-041`), pero en los 300 s
posteriores no se observó `Cuphead.exe` ni un primer frame; las cinco capturas
T+60 muestran carga. En las segundas aperturas el juego presentó frames con
tiempos variables: 25.859 s, 214.500 s, 25.837 s, 24.525 s y 204.010 s,
respectivamente. RUN-037 y RUN-040 muestran el título a T+60; RUN-039 muestra
una animación introductoria; RUN-038 y RUN-041 aún muestran carga. El
comportamiento frío queda reproducido en estos cinco ensayos; su causa sigue
pendiente. Ninguno cuenta como arranque frío satisfactorio.

## Contexto técnico

- Dispositivo: Xiaomi Redmi Note 8, Android 16/API 36, ABI `arm64-v8a`, SoC
  Qualcomm SM6125, 8 núcleos, 3.73 GiB de RAM total, GPU Adreno 610 y resolución
  1080×2340; inventario en [dispositivos.csv](../metricas/runs/RUN-20261023-037/dispositivos.csv).
- Aplicación: paquete `com.cuphead`; ejecutable observado: `Cuphead.exe`.
- Artefacto: `cuphead-11.1-direct-files-auto-gpu-recovery-v15-pixel-bcn-legacy-exec-16k-cuphead-core.apks`.
- SHA-256: `b143bfdfa9ed56d760a921c70fc5bd287f3b533da29bab5d1939732e8a249489`.
- Método: desinstalación completa e instalación fría con Bundletool 1.18.3,
  seguida por 300 s de medición; después, reapertura sin reinstalar y otros
  300 s. Winlator y la configuración interna del contenedor: N/R en estas
  ejecuciones.

## Reproducción o evidencia

1. En `RUN-20261023-037`, la fila `install_apks` de
   [instalaciones.csv](../metricas/runs/RUN-20261023-037/instalaciones.csv)
   registra `success`, código de salida 0 y 204.656 s.
2. La fase fría contiene 301 muestras durante 300 s. `app_alive_ratio=1.000`,
   `game_alive_ratio=0.000`, y no existe evento
   `game_process_first_seen` ni `first_game_frame_observed` en
   [eventos.csv](../metricas/runs/RUN-20261023-037/eventos.csv). El resumen deja
   `delivery_to_first_frame_seconds` como N/R; no se infiere un tiempo exacto.
3. La captura canónica [T+60 fría](../metricas/runs/RUN-20261023-037/screenshots/redmi-note-8/t060.png)
   muestra el texto `Cargando` y el indicador circular de Cuphead.
4. En la segunda apertura, `Cuphead.exe` apareció a los 22.552 ms y el primer
   frame a los 25.859 ms desde el relanzamiento; la captura
   [T+60 second-open](../metricas/runs/RUN-20261023-037/second-open/screenshots/redmi-note-8/t060.png)
   muestra la pantalla de título. Su resumen registra 300 s, app activa 1.000,
   juego activo 0.930 y resultado `approved_experimental`.
5. En `RUN-20261023-038`, Bundletool también terminó con `success` (206.969 s).
   La fase fría volvió a registrar 301 muestras sin `Cuphead.exe` ni primer
   frame; su captura T+60 muestra carga. En la segunda apertura, `Cuphead.exe`
   apareció a los 212.442 s y el primer frame a los 214.500 s. La captura T+60
   de esa fase aún muestra carga y el resultado queda `partial`; no se afirma
   que hubiera llegado al título dentro de la ventana.
6. En `RUN-20261023-039`, Bundletool terminó con `success` (208.067 s). La fase
   fría volvió a registrar 301 muestras sin proceso del juego ni primer frame.
   En la reapertura, el primer frame apareció a los 25.837 s; T+60 muestra la
   animación/splash de apertura de Cuphead, anterior a la pantalla de título.
7. Bundletool registró en la instalación el aviso exacto:

   ```text
   Failed to remove working directory with local testing splits. Your app might still have been installed correctly but have previous version of dynamic feature modules. If you see legacy versions of dynamic feature modules installed try to uninstall and install the app again.
   ```

   El comando terminó con código 0 y la instalación se marcó `success`. Este
   aviso ya está documentado por separado en la
   [limitación 41](./41-bundletool-local-testing-release-no-debuggable.md); no
   hay evidencia suficiente para atribuirle el arranque frío incompleto.
8. En `RUN-20261023-040`, Bundletool terminó con `success` (207.993 s). La fase
   fría volvió a registrar 301 muestras sin proceso del juego ni primer frame;
   T+60 muestra la pantalla `Cargando`. En la segunda apertura el primer frame
   apareció a los 24.525 s y T+60 muestra el título (`Press Any Button`); ambas
   fases permanecieron activas durante los 300 s observados.
9. En `RUN-20261023-041`, Bundletool terminó con `success` (207.886 s). La fase
   fría volvió a registrar 301 muestras sin proceso del juego ni primer frame;
   T+60 muestra `Cargando`. En la segunda apertura, el proceso del juego apareció
   a los 202.631 s y el primer frame a los 204.010 s. Su captura T+60 aún muestra
   carga y el resultado es `partial`.

## Impacto

La instalación por sí sola no demuestra que Cuphead llegue a ejecutarse en un
primer arranque. En cinco pruebas consecutivas no hubo primer frame dentro de los
300 s de observación fría posteriores a la instalación. La reapertura exitosa o
tardía no corrige ni reemplaza ese resultado frío.

## Análisis técnico

La evidencia confirma que la app Android contenedora siguió activa mientras la
captura mostraba la pantalla de carga. No se observó el proceso del juego durante
las fases frías ni un mensaje de crash concluyente en la evidencia revisada. En
las segundas aperturas el comportamiento fue variable: RUN-037, RUN-039 y
RUN-040 presentaron primer frame en aproximadamente 25 s; RUN-038 y RUN-041
tardaron 214.500 s y 204.010 s, respectivamente, y sus capturas T+60 todavía
mostraban carga. La causa queda sin determinar; una preparación inicial lenta,
presión de almacenamiento u otro estado del entorno son hipótesis, no
conclusiones de estos runs.

## Solución aplicada

No se cambió la configuración ni se manipuló la pantalla durante la medición.
Se conservó la instalación para completar la segunda apertura y comparar ambas
fases. La ejecución no se repitió con otra configuración.

## Resultado

Limitación reproducida en cinco arranques fríos del Redmi Note 8; causa pendiente.
`EXEC-116` a `EXEC-120` son registros experimentales válidos, pero sus fases
frías son parciales: instalación correcta, sin primer frame dentro de 300 s. Las
segundas aperturas sí produjeron frames, con latencias variables. No deben
contarse como cinco arranques fríos satisfactorios.

## Limitaciones pendientes

- Determinar si el arranque frío del Redmi requiere más de 300 s o queda detenido
  en la pantalla de carga bajo estas condiciones.
- Comprobar si el comportamiento se repite en los siguientes ensayos fríos sin
  alterar el protocolo de 300 s.
- Confirmar el estado visual final de la segunda apertura tardía de RUN-038; la
  captura canónica T+60 aún mostraba carga.
- Distinguir la animación/splash de estudio del título del juego para futuras
  clasificaciones visuales del primer frame.
- Identificar si el aviso de limpieza de Bundletool guarda alguna relación; por
  ahora no hay evidencia causal.

## Referencias

- [Matriz EXEC-116](../ejecuciones/116-metricas-cuphead-cold-second-open-trial-01-20261023/matriz.md)
- [Matriz EXEC-117](../ejecuciones/117-metricas-cuphead-cold-second-open-trial-02-20261023/matriz.md)
- [Matriz EXEC-118](../ejecuciones/118-metricas-cuphead-cold-second-open-trial-03-20261023/matriz.md)
- [Matriz EXEC-119](../ejecuciones/119-metricas-cuphead-cold-second-open-trial-04-20261023/matriz.md)
- [Matriz EXEC-120](../ejecuciones/120-metricas-cuphead-cold-second-open-trial-05-20261023/matriz.md)
- [RUN-20261023-037](../metricas/runs/RUN-20261023-037/)
- [RUN-20261023-038](../metricas/runs/RUN-20261023-038/)
- [RUN-20261023-039](../metricas/runs/RUN-20261023-039/)
- [RUN-20261023-040](../metricas/runs/RUN-20261023-040/)
- [RUN-20261023-041](../metricas/runs/RUN-20261023-041/)
- [Limitación 41: aviso de Bundletool](./41-bundletool-local-testing-release-no-debuggable.md)

## Ejecuciones asociadas

- [EXEC-116](../ejecuciones/116-metricas-cuphead-cold-second-open-trial-01-20261023/matriz.md) /
  [RUN-20261023-037](../metricas/runs/RUN-20261023-037/)
- [EXEC-117](../ejecuciones/117-metricas-cuphead-cold-second-open-trial-02-20261023/matriz.md) /
  [RUN-20261023-038](../metricas/runs/RUN-20261023-038/)
- [EXEC-118](../ejecuciones/118-metricas-cuphead-cold-second-open-trial-03-20261023/matriz.md) /
  [RUN-20261023-039](../metricas/runs/RUN-20261023-039/)
- [EXEC-119](../ejecuciones/119-metricas-cuphead-cold-second-open-trial-04-20261023/matriz.md) /
  [RUN-20261023-040](../metricas/runs/RUN-20261023-040/)
- [EXEC-120](../ejecuciones/120-metricas-cuphead-cold-second-open-trial-05-20261023/matriz.md) /
  [RUN-20261023-041](../metricas/runs/RUN-20261023-041/)
