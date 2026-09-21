# Decisión: interfaz Android Material 3 adaptativa

- **Fecha:** 2026-09-20
- **Estado:** aceptada; implementación y validación multidispositivo en curso
- **Propósito:** unificar la interfaz general y el flujo Core de Win2APK con un
  sistema visual Android coherente, adaptable y verificable.

## Problema

La aplicación heredada usa una combinación de temas AppCompat, estilos propios,
diálogos y controles programáticos. No tiene recursos adaptativos para tablet,
varias superficies usan dimensiones fijas y parte del runtime fuerza
orientación horizontal. La interfaz general y el flujo Core tampoco parten de
los mismos tokens de color y componentes.

## Decisión

Se conserva la arquitectura Java/XML y se migra gradualmente a Material 3 para
Views mediante Material Components 1.12.0. La aplicación aplicará colores
dinámicos cuando el sistema los ofrezca y usará como respaldo una paleta propia
derivada del icono: azul oscuro `#172033`, verde `#50C878` y superficie clara
`#F4F7FB`.

La decisión cubre:

1. temas claro y oscuro con roles semánticos de Material 3;
2. colores dinámicos aplicados antes de crear cada actividad;
3. componentes táctiles con objetivo mínimo de 48 dp y estados accesibles;
4. navegación y listas adaptadas a móvil y tablet;
5. diseños comprobables en vertical y horizontal;
6. diálogos y progreso compartidos entre la interfaz general y Core;
7. conservación del orden de superficies, eventos e integración nativa del
   entorno de compatibilidad.

## Restricciones técnicas

Se mantiene `targetSdk=28` porque elevarlo bloqueó experimentalmente la
ejecución de Box64 desde el rootfs. La interfaz puede compilarse con un SDK
moderno sin cambiar ese contrato de ejecución.

Material Components 1.14.0 exige una versión de Android Gradle Plugin superior
a la 8.5.1 usada por el proyecto. La versión 1.12.0 permite introducir Material
3 sin ampliar simultáneamente el riesgo del toolchain. Esta selección no se
interpreta como una promesa de compatibilidad universal.

Los lienzos de XServer y controles táctiles se conservan como superficies
especializadas. Material 3 se aplica a las capas Android, barras, paneles,
diálogos y controles que las rodean, sin sustituir el protocolo de entrada ni
el renderizado del entorno de compatibilidad.

## Justificación

Una migración incremental evita reescribir el runtime y permite comprobar cada
familia de pantallas en dispositivos reales. Los roles semánticos hacen que el
modo claro, oscuro y dinámico compartan jerarquía visual, mientras que los
recursos por ancho evitan tratar una tablet como un teléfono ampliado.

## Evidencia inicial

EXEC-050 confirmó el flujo Core en Redmi Note 8 horizontal y mostró que la
interfaz general requiere una compilación separada con `coreMode=false`. El
inventario ADB identificó además una Lenovo TB-J606F en vertical, por lo que la
aceptación exige cubrir ambos tamaños y orientaciones.

## Decisiones pendientes

- Confirmar visualmente la variante general después de su instalación temporal.
- Medir las cuatro combinaciones móvil/tablet y vertical/horizontal.
- Evaluar TalkBack o un inspector equivalente en los controles programáticos
  que no exponen semántica mediante XML.

## Trazabilidad

- [Especificación de interfaz Material 3](../especificaciones/interfaz-material3.md)
- [EXEC-050: línea base Core en Redmi](../ejecuciones/50-metricas-ui-base-nocore-redmi-horizontal-20260920/matriz.md)
- [Limitación 33: target API 36 y Box64](../limitaciones/33-target-api36-bloquea-ejecucion-box64-desde-rootfs.md)
- [Limitación 37: clasificación de ejecuciones preinstaladas](../limitaciones/37-agregador-confunde-ejecucion-preinstalada-con-fallo.md)
- [Especificación de Winlator Core](../especificaciones/winlator-core.md)
