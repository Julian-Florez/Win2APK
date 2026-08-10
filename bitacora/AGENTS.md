# Guía para `bitacora/`

La bitácora es un índice cronológico de limitaciones. El informe técnico completo permanece en `../limitaciones/`; la bitácora no debe duplicarlo.

## Procedimiento

1. Leer `../AGENTS.md` y `index.md` antes de editar.
2. Añadir una fila por cada informe de limitación nuevo.
3. Conservar el número del informe, la fecha, el estado y el enlace al archivo detallado.
4. Enlazar la ejecución donde se detectó o verificó el problema.
5. Actualizar el estado solo con una nueva evidencia; no cerrar una limitación por decisión verbal.

## Estados permitidos

`detectada`, `reproducida`, `en investigación`, `resuelta experimentalmente`, `cerrada` y `no reproducida`.

## Formato de la tabla

| Nº | Limitación | Fecha | Estado | Ejecución relacionada | Informe detallado |
|---:|---|---|---|---|---|

Una misma limitación puede tener varias ejecuciones enlazadas. Mantener en la descripción de la fila únicamente la información necesaria para localizar el detalle.