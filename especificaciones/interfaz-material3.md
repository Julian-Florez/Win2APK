# Especificación de interfaz Android Material 3

- **Identificador:** `WIN2APK-UI-001`
- **Versión:** 0.1
- **Fecha:** 2026-09-20
- **Estado:** implementación y validación en curso
- **Decisión relacionada:** [Interfaz Android Material 3 adaptativa](../documentacion/14-decision-interfaz-material3-adaptativa.md)

## Alcance

Esta especificación cubre las superficies Android de la interfaz general de
Winlator y del flujo Winlator Core. No sustituye el renderizado de XServer ni
presenta el entorno de compatibilidad como una aplicación Android nativa.

## Requisitos funcionales

| ID | Requisito verificable |
|---|---|
| UI-RF-01 | En Android 12 o posterior, cada actividad deberá aplicar colores dinámicos cuando el sistema los ofrezca. |
| UI-RF-02 | Cuando los colores dinámicos no estén disponibles, la interfaz deberá usar la paleta de respaldo documentada sin perder legibilidad. |
| UI-RF-03 | La preferencia de tema claro u oscuro deberá aplicarse antes de inflar la primera pantalla, incluido el modo Core. |
| UI-RF-04 | La interfaz general deberá conservar acceso a contenedores, shortcuts, gestor de archivos, ajustes y ayuda después de la migración visual. |
| UI-RF-05 | El modo Core deberá conservar el arranque directo y no exponer navegación general durante su flujo normal. |
| UI-RF-06 | Los diálogos de confirmación, contenido, progreso y error deberán usar componentes y roles de color Material 3. |
| UI-RF-07 | Las listas deberán conservar sus acciones existentes y mostrar estados vacío, seleccionado, pulsado, deshabilitado y progreso cuando correspondan. |
| UI-RF-08 | La capa Android del runtime deberá conservar las acciones de salir, teclado, controles y edición de controles sin alterar la entrega de entrada a XServer. |

## Requisitos adaptativos y de accesibilidad

| ID | Requisito verificable |
|---|---|
| UI-RNF-01 | La pantalla principal deberá disponer de una composición específica para anchos de tablet de al menos 600 dp. |
| UI-RNF-02 | Las pantallas Android deberán ser utilizables en móvil y tablet, tanto vertical como horizontal, sin controles esenciales fuera del área visible. |
| UI-RNF-03 | Los controles táctiles Android interactivos deberán tener un objetivo mínimo de 48 × 48 dp, salvo controles del entorno Windows cuya geometría pertenezca al runtime. |
| UI-RNF-04 | Los botones basados solo en iconos deberán exponer una descripción accesible o una etiqueta equivalente. |
| UI-RNF-05 | El foco, selección y rango de controles personalizados deberán ser operables mediante las APIs de accesibilidad o teclado cuando el componente lo admita. |
| UI-RNF-06 | Barras, paneles y diálogos deberán respetar insets de sistema y no depender del tamaño físico completo de la pantalla. |
| UI-RNF-07 | Texto de interfaz Android deberá expresarse en `sp`; las dimensiones visuales deberán expresarse en `dp`. |
| UI-RNF-08 | El contraste de texto y controles deberá mantenerse en temas claro, oscuro y dinámico. |

## Criterios de aceptación

| ID | Prueba observable | Evidencia |
|---|---|---|
| UI-CA-01 | Instalar una variante `coreMode=false` con paquete independiente y abrir la interfaz general en Redmi Note 8. | Pendiente |
| UI-CA-02 | Repetir UI-CA-01 en Lenovo TB-J606F sin reemplazar las aplicaciones de tesis ya instaladas. | Pendiente |
| UI-CA-03 | Capturar a T+60 móvil horizontal y tablet vertical con métricas y clasificación visual. | Pendiente |
| UI-CA-04 | Comprobar móvil vertical y tablet horizontal, restaurando la rotación original al finalizar. | Pendiente |
| UI-CA-05 | Alternar tema claro y oscuro; verificar superficies, texto, diálogos y barras de sistema. | Pendiente |
| UI-CA-06 | Con colores dinámicos habilitados, verificar que la paleta cambia; con ellos no disponibles, verificar la paleta de respaldo. | Pendiente |
| UI-CA-07 | Ejecutar una variante Core y comprobar que llega al entorno de compatibilidad sin mostrar navegación general. | [EXEC-050](../ejecuciones/50-metricas-ui-base-nocore-redmi-horizontal-20260920/matriz.md), pendiente repetir con la nueva compilación |

## Exclusiones

- Reescritura de la aplicación en Jetpack Compose.
- Sustitución del protocolo de entrada de XServer.
- Cambio de `targetSdk=28` dentro de esta migración visual.
- Afirmación de compatibilidad universal a partir de los dos dispositivos
  utilizados para aceptación.

## Trazabilidad

- [Decisión de interfaz Material 3](../documentacion/14-decision-interfaz-material3-adaptativa.md)
- [Especificación de Winlator Core](./winlator-core.md)
- [Limitación 33](../limitaciones/33-target-api36-bloquea-ejecucion-box64-desde-rootfs.md)
- [Limitación 37](../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md)
