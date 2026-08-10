# Bitácora de fallos y limitaciones

Este índice reúne los fallos y restricciones técnicas detectados durante el desarrollo de Win2APK. Los detalles se conservan en `../limitaciones/` y las pruebas asociadas en `../ejecuciones/`.

| Nº | Limitación | Fecha | Estado | Ejecución relacionada | Informe detallado |
|---:|---|---|---|---|---|
| 01 | Inicialización de CoreCLR/GC en Winlator | 2026-08-07 | Resuelta experimentalmente | [EXEC-001](../ejecuciones/01-linea-base-manual-winlator-tb-j606f/matriz.md) | [01-error-coreclr-gc-winlator.md](../limitaciones/01-error-coreclr-gc-winlator.md) |

## Criterio de lectura

El informe 01 documenta el fallo de la publicación inicial y la corrección experimental. La ejecución `EXEC-001` documenta la prueba manual de la publicación por carpeta posterior a la corrección; no debe interpretarse como una repetición del fallo original.