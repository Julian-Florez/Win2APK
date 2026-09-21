# Documentación de Win2APK

Esta carpeta reúne las decisiones, avances y evidencias del desarrollo del proyecto de tesis **Win2APK**.

## Documentos

0. [00. Contexto general del proyecto](./00-contexto-del-proyecto.md)
1. [01. Aplicación mínima y dispositivos objetivo](./01-app-minima-y-dispositivos-objetivo.md)
2. [02. Plan de Winlator Core](./02-plan-winlator-core.md)
3. [Especificación de la aplicación mínima](../especificaciones/app-minima.md)
4. [Plan de distribución segmentada para Cuphead](./03-plan-distribucion-segmentada-cuphead.md)
5. [Plan de acceso directo a asset packs de Cuphead](./04-plan-acceso-directo-assetpack-cuphead.md)
6. [Decisión de perfil gráfico para Pixel Tensor/Mali](./05-decision-perfil-grafico-pixel-tensor-mali.md)
7. [Integración de fuentes para el estado del arte](./06-integracion-fuentes-estado-arte.md)
8. [Decisión experimental de DXVK 2.4.1 para Mali y Adreno](./07-decision-dxvk241-multidispositivo.md)
9. [Decisión sobre la capa BCn Android para Pixel Tensor/Mali](./08-decision-capa-bcn-android-pixel.md)
10. [Compatibilidad de API moderna y páginas de 16 KB](./09-decision-compatibilidad-api36-y-paginas-16kb.md)
11. [Target API 28 para la ejecución del entorno de compatibilidad](./10-decision-target-api28-para-winlator-exec.md)
12. [Automatización del icono de launcher](./11-automatizacion-iconos-launcher.md)
13. [Manual HTML para empaquetar una carpeta e instalarla en Android](./12-guia-empaquetado-win2apk.html)
14. [CLI Linux y configuración declarativa v2](./13-decision-cli-linux-configuracion-v2.md)
15. [Interfaz Android Material 3 adaptativa](./14-decision-interfaz-material3-adaptativa.md)

## Criterio de organización

El documento `00-contexto-del-proyecto.md` establece el problema, el propósito, el alcance, las restricciones, la planificación y las decisiones base de la tesis.

Los documentos numerados posteriores registran las decisiones y avances principales en el orden en que se incorporan al proyecto. Las especificaciones técnicas se mantienen en la carpeta `especificaciones/` para servir como referencia durante la implementación y las pruebas.

## Registro experimental

- [Bitácora de fallos y limitaciones](../bitacora/index.md)
- [Ejecuciones y matrices de prueba](../ejecuciones/index.md)
- [Plantilla de métricas](../ejecuciones/plantilla-metricas.md)
- [Especificación de distribución de datos del juego](../especificaciones/distribucion-datos-juego.md)
- [Limitación 01: inicialización de CoreCLR en Winlator](../limitaciones/01-error-coreclr-gc-winlator.md)
