# 47. Detección inicial de pantalla negra de WinTest en Mi A3: reclasificada

## Descripción

En la primera revisión visual se marcaron como `black_screen` la segunda apertura
de RUN-017 y RUN-018, y la instalación fría de RUN-019. Una revisión ampliada de
las capturas mostró que las tres contienen la ventana Win2APK Test, “Hola mundo”
y “Cambiar texto”. Las etiquetas iniciales eran falsos positivos y fueron
reemplazadas; las métricas de instalación y proceso no se modificaron.

## Contexto técnico

- Dispositivo: Xiaomi Mi A3, LineageOS, Android 16/API 36, SoC SM6125, GPU Adreno
  610.
- Aplicación: WinTest (`org.win2apk.testapp`); proceso: `Win2APKTest.exe`.
- Escenarios afectados: RUN-017/EXEC-096 second-open, RUN-018/EXEC-097
  second-open y RUN-019/EXEC-098 instalación fría.
- Capturas: 1560×720, T+60 s; las tres clasificadas inicialmente como negras
  están enlazadas en el informe de revisión [49](./49-clasificacion-visual-falsa-pantalla-negra-wintest-mi-a3-20261023.md).

## Resultado corregido

Las tres capturas afectadas quedaron clasificadas como `other`, con descripción
de la ventana Win2APK Test visible. Las seis capturas disponibles de esos tres
pares contienen los textos de interfaz. Los CSV de cada fase se volvieron a
validar y las matrices EXEC-096, EXEC-097 y EXEC-098 se regeneraron a partir de
las clasificaciones corregidas.

## Impacto y solución

La lectura a tamaño completo hizo pasar por negra una interfaz pequeña centrada
en la captura. Se corrigió revisando un recorte ampliado y contrastándolo con
OCR; la causa no era un fallo del dispositivo. Se añadió este caso a las
instrucciones de clasificación para exigir la inspección de la zona de la
aplicación antes de usar `black_screen`.

## Estado

Corregida experimentalmente. No se conserva evidencia de pantalla negra en
estas capturas una vez revisada la interfaz; no debe citarse como crash o fallo
de WinTest.

## Referencias

- [Informe de revisión 49](./49-clasificacion-visual-falsa-pantalla-negra-wintest-mi-a3-20261023.md)
- [Matriz EXEC-096](../ejecuciones/96-metricas-wintest-cold-second-open-trial-01-20261023/matriz.md)
- [Matriz EXEC-097](../ejecuciones/97-metricas-wintest-cold-second-open-trial-02-20261023/matriz.md)
- [Matriz EXEC-098](../ejecuciones/98-metricas-wintest-cold-second-open-trial-03-20261023/matriz.md)
