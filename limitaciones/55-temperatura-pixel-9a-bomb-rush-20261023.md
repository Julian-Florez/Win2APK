# 55. Estado térmico elevado del Pixel 9a tras pruebas consecutivas de Bomb Rush

## Descripción

Durante las pruebas de Bomb Rush en el Pixel 9a, el servicio térmico de Android
reportó estado 3 al terminar fases de cinco minutos en RUN-061 a RUN-064 y
RUN-066.
Después de detener las apps al concluir RUN-062 y RUN-064, consultas posteriores
reportaron estado 4 y baterías a 43.9 °C y 43.6 °C, respectivamente. En RUN-063
el estado global posterior fue 3 (batería 43.5 °C), aunque un sensor individual
marcó nivel 4. Se detuvieron las apps entre parejas y se enfrió el teléfono. La
proximidad temporal no demuestra por sí sola que el juego sea la causa única del
aumento térmico.

## Contexto técnico

- Dispositivo: Google Pixel 9a, Android 17/API 37, ABI `arm64-v8a`, SoC Tensor
  G4, 8 núcleos, resolución 1080×2424.
- Aplicación: Bomb Rush Cyberfunk, paquete
  `com.win2apk.bombrushcyberfunk`, proceso `Bomb Rush Cyberfunk.exe`.
- Artefacto: `bomb-rush-cyberfunk-gog-56774571391351451.apks`, SHA-256
  `fb7fc6114b39b3187af6b84807e6db09982195cd87719dedb33e8d013a172f54`.
- Protocolo: instalación fría y segunda apertura, cada fase observada durante
  300 s, muestreo nominal de 1 s, pruebas secuenciales por USB y sin root.
- Estado térmico antes de RUN-061: 1; batería 39.7 °C. Antes de RUN-062, después
  del enfriamiento: estado 1; batería 41.1 °C. Antes de RUN-063, tras reposo y
  desbloqueo manual: estado 0; batería 36.2 °C. Antes de RUN-064: estado 1;
  batería 40.4 °C. Antes de RUN-066: estado 0; batería 35.9 °C; Pixel despierto y
  desbloqueado.

## Reproducción o evidencia

1. RUN-061 (`EXEC-140`) completó 301 muestras en ambas fases. La batería alcanzó
   42.6 °C en frío y 43.3 °C en la segunda apertura. Inmediatamente después de
   cada fase, `dumpsys thermalservice` reportó `Thermal Status: 3`.
2. Se detuvo la app y se esperó hasta estado térmico 1 (batería 40.1 °C) antes de
   iniciar RUN-062.
3. RUN-062 (`EXEC-141`) también completó 301 muestras en ambas fases. La batería
   alcanzó 43.4 °C en frío y 43.8 °C en la segunda apertura; tras la fase, el
   servicio reportó estado 3.
4. Después de `am force-stop` al terminar RUN-062, la consulta siguiente reportó
   `Thermal Status: 4` y 43.9 °C de batería. Entre los sensores que mostraban
   nivel 4 estaban `VIRTUAL-SKIN` y `VIRTUAL-SKIN-DISPLAY` (46.52 °C), y
   `VIRTUAL-SKIN-CHARGE` (45.79 °C). El Pixel seguía despierto y sin bloqueo; el
   proceso del juego estaba detenido.
5. Se apagó la pantalla con `input keyevent 26` y no se inició otra carga hasta
   que el Pixel bajó a estado 0 (batería 36.3 °C). El usuario lo desbloqueó
   manualmente antes de retomar.
6. RUN-063 (`EXEC-142`) completó 301 muestras por fase. La batería alcanzó
   41.3 °C en frío y 43.5 °C en la segunda apertura. El estado térmico fue 2 al
   concluir la fase fría y 3 tras la segunda apertura; una consulta posterior al
   `force-stop` mantuvo estado global 3, con el sensor
   `VIRTUAL-SKIN-CHARGE` a 46.05 °C y estado individual 4. La app quedó detenida.
7. RUN-064 (`EXEC-143`) completó 301 muestras por fase, con primer frame frío a
   120.992 s. La captura fría T+60 muestra el splash «TEAM REPTILE» (`other`),
   mientras que la segunda apertura muestra el título y «PRESS ANY KEY». La
   batería alcanzó 42.8 °C en frío y 43.2 °C en la segunda apertura; el estado
   global fue 3 tras las fases. Después de detener la app se observó estado 4,
   batería a 43.6 °C y sensores `VIRTUAL-SKIN`/`VIRTUAL-SKIN-DISPLAY` a
   46.54/46.51 °C y `VIRTUAL-SKIN-CHARGE` a 46.15 °C.
8. RUN-065 no llegó a lanzar el juego por un paquete de validación incorrecto y
   no aportó carga térmica de juego. RUN-066 completó 301 muestras frías; la
   batería llegó a 41.0 °C y, después de la fase, el estado global era 2. Se
   detuvo la app y se esperó hasta estado 1/batería 38.8 °C antes de la segunda
   apertura. Esta completó otras 301 muestras, con máximo de batería 42.6 °C;
   después de la fase se observó estado global 3. Tras detener la app y apagar
   la pantalla, el Pixel seguía en estado 3; una lectura posterior marcó
   batería 42.9 °C (la primera lectura posterior al apagado fue 43.3 °C).
9. Tras dejar el Pixel en reposo, el servicio bajó a estado 1 y la batería a
   38.6 °C. La pantalla quedó en `Dozing`; ADB reportó `showing=true`, por lo
   que se requerirá desbloqueo manual antes de cualquier nueva prueba.
   No se observó un crash. Las capturas T+60 de ambas fases muestran el mismo
   logotipo de Bomb Rush sin invitación a comenzar (`other`); una captura
   suplementaria posterior al monitor, aproximadamente T+382 s, muestra el
   mismo estado visual.

Los CSV de RUN-061 a RUN-064 y RUN-066 registran las temperaturas máximas de
batería por fase. El campo `thermal_max_c` no fue recogido por el monitor y queda
como `N/R`; los estados térmicos anteriores proceden de consultas ADB posteriores
a las fases, no de muestras incorporadas retrospectivamente al CSV. Cada fase
conserva sus 301 muestras y su captura T+60. Las capturas frías de RUN-061/062
fueron negras; RUN-063 mostró el título; RUN-064 el splash «TEAM REPTILE»; y
RUN-066 el logotipo de Bomb Rush. En RUN-061 a RUN-064 las segundas aperturas
mostraron el título; en RUN-066 se mantuvo el logotipo durante el monitoreo y en
la comprobación suplementaria.

Evidencia: [RUN-061](../metricas/runs/RUN-20261023-061/),
[EXEC-140](../ejecuciones/140-metricas-bomb-rush-cold-second-open-trial-02-20261023/matriz.md),
[RUN-062](../metricas/runs/RUN-20261023-062/),
[EXEC-141](../ejecuciones/141-metricas-bomb-rush-cold-second-open-trial-03-20261023/matriz.md),
[RUN-063](../metricas/runs/RUN-20261023-063/),
[EXEC-142](../ejecuciones/142-metricas-bomb-rush-cold-second-open-trial-04-20261023/matriz.md),
[RUN-064](../metricas/runs/RUN-20261023-064/),
[EXEC-143](../ejecuciones/143-metricas-bomb-rush-cold-second-open-trial-05-20261023/matriz.md),
[RUN-066](../metricas/runs/RUN-20261023-066/),
[EXEC-145](../ejecuciones/145-metricas-bomb-rush-cold-second-open-trial-06-retry-01-20261023/matriz.md).

## Impacto

Cualquier medición adicional queda pausada hasta que el Pixel se enfríe.
Continuar sin enfriamiento podría introducir estrangulamiento térmico y alterar
la comparabilidad del rendimiento; esto es un riesgo metodológico, no una causa
confirmada de los resultados gráficos ni de la duración de arranque. No se
registró cierre de la app durante RUN-061 a RUN-064 ni RUN-066.

## Análisis técnico

Se observó una subida térmica tras varias fases consecutivas y un estado 4
posterior a RUN-062 y RUN-064; RUN-066 terminó en estado 3. El desfase entre el
final de la medición, el `force-stop` y la lectura térmica impide ubicar el
instante exacto de ese máximo. La carga USB,
la pantalla, la actividad del juego y la acumulación de calor pueden contribuir;
no se aisló experimentalmente ninguna de esas variables. Una observación anterior
de estado 4 está descrita en la [limitación 53](53-interrupcion-monitor-bomb-rush-pixel-9a-20261023.md).

## Solución aplicada

Para RUN-066 se detuvo el proceso entre fases y se esperó hasta estado 1 antes de
la segunda apertura. Al terminar se detuvo Bomb Rush y se apagó la pantalla; las
lecturas posteriores bajaron de estado 3/batería 43.3 °C a estado 1/batería
38.6 °C. La pantalla quedó en `Dozing` con keyguard visible. No se modificó la
configuración del juego ni del contenedor. Cualquier nueva prueba debe comenzar
con estado térmico 1 o menor y requerirá que el usuario desbloquee el Pixel.

## Resultado

RUN-061 a RUN-064 y RUN-066 conservaron 301 muestras por fase y el primer frame
frío apareció dentro de 300 s. Las segundas aperturas también produjeron un
primer frame. RUN-066 quedó parcial respecto al estado visual esperado: en ambas
fases y en la captura suplementaria seguía visible el logotipo sin invitación a
comenzar. La observación térmica requiere reposo entre fases y queda en
investigación.

## Limitaciones pendientes

- Antes de una prueba adicional, confirmar estado térmico 1 o menor y pedir al
  usuario que desbloquee manualmente el Pixel.
- Si al despertar aparece la pantalla de autenticación, solicitar al usuario que
  lo desbloquee manualmente; no eludir el bloqueo.
- Medir y registrar temperatura y estado térmico antes y después de cada fase
  restante, sin atribuir causalidad a partir de lecturas posteriores.
- Si se exige que el Pixel llegue a la pantalla de título, investigar el estado
  `other` de RUN-066 en una nueva sesión, sin atribuirlo a la temperatura por
  correlación únicamente.

## Referencias

- [RUN-061](../metricas/runs/RUN-20261023-061/)
- [RUN-062](../metricas/runs/RUN-20261023-062/)
- [RUN-063](../metricas/runs/RUN-20261023-063/)
- [RUN-064](../metricas/runs/RUN-20261023-064/)
- [RUN-066](../metricas/runs/RUN-20261023-066/)
- [Limitación 53: interrupciones y lectura térmica posterior](53-interrupcion-monitor-bomb-rush-pixel-9a-20261023.md)

## Ejecuciones asociadas

- [EXEC-140](../ejecuciones/140-metricas-bomb-rush-cold-second-open-trial-02-20261023/matriz.md): RUN-061, estado térmico 3 tras ambas fases.
- [EXEC-141](../ejecuciones/141-metricas-bomb-rush-cold-second-open-trial-03-20261023/matriz.md): RUN-062, estado 3 tras las fases y estado 4 en la comprobación posterior.
- [EXEC-142](../ejecuciones/142-metricas-bomb-rush-cold-second-open-trial-04-20261023/matriz.md): RUN-063, estado térmico 3 tras la segunda apertura; estado individual 4 en el sensor de carga.
- [EXEC-143](../ejecuciones/143-metricas-bomb-rush-cold-second-open-trial-05-20261023/matriz.md): RUN-064, estado térmico 3 tras las fases y estado global 4 en la comprobación posterior.
- [EXEC-145](../ejecuciones/145-metricas-bomb-rush-cold-second-open-trial-06-retry-01-20261023/matriz.md): RUN-066, estado 2 después del frío, 1 antes de second-open, y 3 después de second-open y al terminar.
