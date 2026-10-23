# 46. Clasificación visual errónea por previsualización inconsistente de capturas WinTest

## Descripción

En una revisión inicial, una previsualización inconsistente llevó a etiquetar las capturas T+60 de WinTest en `RUN-20261023-002` y la reapertura de `RUN-20261023-003` como `black_screen`. La revisión explícita posterior de los PNG originales, apoyada por OCR/Tesseract que detecta “Hola mundo” y por inspección de la ventana y sus píxeles, confirmó que las cuatro imágenes muestran la consola y la ventana gráfica Win2APK Test. Las cuatro clasificaciones se corrigieron a `other` y se marcaron `human_review_status=confirmed`. No se modificaron las imágenes. `RUN-20261023-004` frío y second-open también muestran “Hola mundo” en OCR y se clasificaron `other`.

La clasificación negra anterior queda registrada aquí como error de revisión causado por la vista previa, no como fallo reproducido de la aplicación. Los ensayos no se repitieron por esa etiqueta equivocada.

## Contexto técnico

- Dispositivo: Lenovo TB-J606F, Android 16; detalles en `metricas/runs/RUN-20261023-002/dispositivos.csv`.
- Paquete: `org.win2apk.testapp`; ejecutable: `Win2APKTest.exe`.
- Artefacto: `win2apk-test-0.1.0.apks`, SHA-256 `a7e3e0e252df496924c0a81845b54a11be95a04a1224f8b8a68c5eea2c10bae1`.
- Pruebas: RUN-002, RUN-003 y RUN-004, cada una con apertura fría y reapertura, 300 s por fase, captura T+60 s.

## Reproducción o evidencia

1. La revisión OCR sobre los PNG originales de RUN-002 frío y second-open detecta “Hola mundo” y texto de consola. Los SHA-256 son `dbda5287241d368b5cfb57f74cd25c94544c08469d53a3b5a96aa0a4a36a9c3d` y `4312142ac87f2298de759595693ed7beb8dc978bc8c5e8facf347de1573e0e41`.
2. Los PNG frío y second-open de RUN-003 son byte a byte idénticos, ambos SHA-256 `13fc4f45dc21f3803668302cf06875777c2aeb7745deb79f20e35dc1f2854dde`; OCR de cada archivo detecta “Hola mundo”.
3. Los PNG RUN-004 frío y second-open también fueron revisados individualmente; OCR detecta “Hola mundo” en ambos. Sus SHA-256 son `1be871c62948892c8712ddf60ccff6bc50c55c47ddfe07a3656a381bb1b5bd6b` y `13fc4f45dc21f3803668302cf06875777c2aeb7745deb79f20e35dc1f2854dde`.
4. Los CSV conservan `primary_class=other`, `human_review_status=confirmed` y descripciones específicas para cada PNG. Las capturas originales permanecen intactas; las métricas, eventos y logs se conservan en [RUN-002](../metricas/runs/RUN-20261023-002/), [RUN-003](../metricas/runs/RUN-20261023-003/) y [RUN-004](../metricas/runs/RUN-20261023-004/).
5. El historial previo de clasificación `black_screen` y su revocación queda documentado en esta limitación y las matrices EXEC-081/082.

## Impacto

No se confirmó una pantalla negra ni un fallo visual de WinTest en estos PNG. La revisión incorrecta podía inducir a descartar ensayos válidos; se rectificó antes de continuar la serie.

## Análisis técnico

La previsualización renderizada fue inconsistente/engañosa respecto de los PNG originales y llevó a una lectura visual incorrecta. OCR, texto visible, coordenadas e inspección del contenido original corroboran la ventana “Hola mundo”. La etiqueta negra no era evidencia del estado real de la captura ni de un crash.

## Solución aplicada

Se revisaron y corrigieron a `other` las cuatro filas de RUN-002/003, se marcaron confirmadas y se regeneraron los resúmenes. RUN-004 fue clasificado `other` desde sus PNG originales. Se actualizaron las matrices y el índice conservando el historial de la clasificación anterior. No se modificaron ni reemplazaron capturas.

## Resultado

No se confirmó un fallo de pantalla negra de la aplicación. Las seis fases capturadas entre RUN-002/003/004 muestran “Hola mundo” y quedan clasificadas `other`; sus ejecuciones son válidas. La discrepancia correspondió a la previsualización de la evidencia.

## Limitaciones pendientes

- Evitar clasificar basándose exclusivamente en la previsualización de la app; revisar el PNG original y contrastar OCR cuando haya discrepancia.
- La limitación sobre una supuesta falla visual queda resuelta como error de revisión; no queda pendiente de medición para RUN-002/003/004.

## Referencias

- [Matriz EXEC-081](../ejecuciones/81-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md)
- [Matriz EXEC-082](../ejecuciones/82-metricas-wintest-cold-second-open-trial-03-20261023/matriz.md)
- [Matriz EXEC-083](../ejecuciones/83-metricas-wintest-cold-second-open-trial-04-20261023/matriz.md)
- [Captura T+60](../metricas/runs/RUN-20261023-002/screenshots/lenovo-tb-j606f/t060.png)
- [Clasificación y captura](../metricas/runs/RUN-20261023-002/capturas.csv)
- [Resumen second-open](../metricas/runs/RUN-20261023-002/second-open/resumen.csv), [clasificación second-open](../metricas/runs/RUN-20261023-002/second-open/capturas.csv), [captura second-open](../metricas/runs/RUN-20261023-002/second-open/screenshots/lenovo-tb-j606f/t060.png)
- [Log uninstall](../metricas/runs/RUN-20261023-002/logs/lenovo-tb-j606f/uninstall.log)
- [Verificación del estado previo](../metricas/runs/RUN-20261023-002/logs/lenovo-tb-j606f/preflight-package-state.txt)

## Ejecuciones asociadas

- [EXEC-081](../ejecuciones/81-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md) / [RUN-20261023-002](../metricas/runs/RUN-20261023-002/)
