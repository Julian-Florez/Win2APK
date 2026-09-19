# Resultado de la integración BCn dentro del rootfs

## Configuración observada

- Perfil: `Mali/unknown / Vortek + Gladio / DXVK-Sarek 1.13.0 + Leegao BCn ETC2`.
- `libbcn_layer.so`: SHA-256 `fcefa3fa97028c8f8317f95db9f4d7c7c0d5da0c40bb12493f93db408434f8d2`.
- Ubicación: `files/rootfs/usr/lib/libbcn_layer.so` con manifiesto Vulkan dentro del rootfs.
- Resolución: `1280x720`.

## Observación

La imagen de Cuphead apareció a los 30–40 s. En ese corte:

- proceso Android: PSS `2083160 KiB`, RSS `2111520 KiB`, Graphics `2017904 KiB`;
- `Cuphead.exe`: PSS `659746 KiB`, RSS `572572 KiB`;
- PSS combinado calculado: `2742906 KiB`.

La presión de memoria siguió creciendo:

- `ION_heap`: de `3999388 KiB` a `4378744 KiB` y después `4419380 KiB`;
- `MemAvailable`: de `104312 KiB` a `59668 KiB` y después `0 KiB`.

Android terminó el proceso a las `2026-09-18 22:17:57.081` con el mensaje exacto:

```text
reason=3 (LOW_MEMORY) subreason=0 (UNKNOWN) status=0
```

## Interpretación

Restaurar los binarios históricos recuperó el render, pero no la estabilidad cuando la capa BCn se integró dentro del rootfs. Esta variante incumple el criterio de permanencia de 90 s.
