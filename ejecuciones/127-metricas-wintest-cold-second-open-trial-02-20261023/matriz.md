# EXEC-127: Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos

- **Run de métricas:** `RUN-20261023-048`
- **Fecha:** 2026-10-23
- **Tipo:** instalación fría seguida de segunda apertura sin reinstalación; medición temporal
- **Resultado general:** fallido; instalación fría bloqueada y sin medición de ejecución
- **Método:** `bundletool-install-apks-cold`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `org.win2apk.testapp` | `run.csv` |
| Artefacto | `/tmp/win2apk-metodologia-20261022/wintest/win2apk-test-0.1.0.apks` | Archivo medido |
| SHA-256 | `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1` | Calculado antes de instalar |
| Escenario | `wintest-cold-second-open-trial-02` | Instalación fresca de WinTest en Pixel 9a; observar primer inicio durante 5 minutos y luego medir segunda apertura durante 5 minutos |
| Estado esperado | `other` | Hipótesis previa |
| Duración | 300 s por dispositivo | Reloj monótono del host |
| Intervalo nominal | 1.0 s | ADB sin root |
| Captura canónica | T+60 s | Clasificación visual posterior |

## Instalación fría

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| pixel-9a | failed | No completada; 551.283 s hasta interrumpir el comando | N/R s | N/R ms | N/R ms | N/R | N/R | N/R | failed_install |

## Segunda apertura sin reinstalar

| Dispositivo | Tiempo observado | Primer frame | App activa | Juego activo | FPS medio | Captura T+60 | Resultado |
|---|---:|---:|---:|---:|---:|---|---|
| N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R |

## Observación

Durante la instalación apareció una pantalla de Google Play Protect con el texto
«Se bloqueó la app no segura» y «Esta app se diseñó para una versión anterior de
Android, por lo que no incluye las protecciones de la privacidad más recientes.»
La jerarquía de accesibilidad no mostró controles accionables. Tras más de nueve
minutos, `pm path` y `pm list packages` no mostraban `org.win2apk.testapp`; el
cliente de Bundletool seguía esperando. Se interrumpió el cliente a los 551.283 s
para no dejarlo colgado. Ese valor es el tiempo hasta la interrupción, no una
instalación completada. No hubo fase de monitorización, captura canónica T+60,
muestras ni segunda apertura; sus métricas permanecen `N/R`.

## Interpretación

La coincidencia temporal entre el aviso de Play Protect, la ausencia del paquete
y la espera de Bundletool sugiere que la protección pudo bloquear o interrumpir
la instalación. No se obtuvo un error de Package Manager que confirme por sí
solo esa causalidad. El cliente se detuvo manualmente después de verificar que el
paquete seguía ausente; por tanto, el código de salida 130 refleja esa
interrupción, no un crash del juego.

## Decisión

No se desactivó Play Protect ni se cambiaron ajustes de seguridad. El intento se
conserva como fallido y no cuenta entre las cinco repeticiones válidas. Resolver
el aviso o acordar un método de instalación que no requiera debilitar la
seguridad antes de repetir.

## Evidencias

- `pixel-9a`: [captura del aviso de Play Protect](../../metricas/runs/RUN-20261023-048/evidencias/pixel-9a/play-protect-block.png); [logs y CSV](../../metricas/runs/RUN-20261023-048/).

- [Carpeta estructurada del run](../../metricas/runs/RUN-20261023-048)
