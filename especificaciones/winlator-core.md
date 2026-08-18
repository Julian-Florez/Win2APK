# Especificación de Winlator Core

- **Identificador:** `WIN2APK-CORE-001`
- **Versión:** 0.1 de planificación
- **Fecha:** 2026-08-18
- **Estado:** implementación funcional verificada en Lenovo TB-J606F para `TestApp`
- **Decisión relacionada:** [Plan de Winlator Core](../documentacion/02-plan-winlator-core.md)

## Requisitos funcionales

| ID | Requisito verificable |
|---|---|
| CORE-RF-01 | Después de una instalación normal, el usuario deberá tocar el icono una sola vez para iniciar el núcleo. |
| CORE-RF-02 | Después del primer toque, el núcleo deberá mostrar únicamente una pantalla de carga mínima mientras prepara el entorno. |
| CORE-RF-03 | El núcleo deberá instalar o validar el rootfs sin mostrar la interfaz general de Winlator. |
| CORE-RF-04 | El núcleo deberá crear o validar exactamente un contenedor predeterminado identificado como `Container-1`. |
| CORE-RF-05 | El núcleo deberá copiar la carpeta Windows indicada por la configuración al destino del contenedor. |
| CORE-RF-06 | El núcleo deberá crear el shortcut indicado por la configuración en el Desktop del contenedor. |
| CORE-RF-07 | Cuando la preparación termine, el núcleo deberá abrir automáticamente el shortcut configurado. |
| CORE-RF-08 | El usuario no deberá acceder a selector de contenedor, lista de shortcuts, menú lateral ni opciones generales de Winlator durante el flujo normal. |
| CORE-RF-09 | Las unidades `D:` y `E:` deberán conservarse según la configuración inicial. |
| CORE-RF-10 | Cuando la aplicación Windows termine, el núcleo deberá cerrar su actividad y devolver al usuario al launcher de Android. |
| CORE-RF-11 | Si una etapa falla, el núcleo deberá mostrar un mensaje técnico identificable. |

## Requisitos no funcionales

| ID | Requisito verificable |
|---|---|
| CORE-RNF-01 | La distribución deberá ser una APK Android normal y no podrá requerir root. |
| CORE-RNF-02 | Todas las opciones del contenedor y del arranque deberán estar declaradas en un archivo JSON utilizado antes de compilar. |
| CORE-RNF-03 | El `applicationId` y la etiqueta de la APK deberán derivarse del nombre de la carpeta durante la compilación, sin un límite artificial de longitud; los assets con rutas compiladas deberán transformarse al mismo paquete. |
| CORE-RNF-04 | Cambiar el `applicationId` deberá documentarse como una aplicación Android distinta, no como una actualización compatible. |
| CORE-RNF-05 | La configuración no deberá quedar expuesta mediante la interfaz final del núcleo. |
| CORE-RNF-06 | La primera implementación deberá poder depurarse mediante `adb install` antes de distribuirse como APK normal. |

## Contrato JSON implementado

El contrato implementado cubre las secciones de aplicación, Android/build, arranque, runtime, shortcut y contenedor:

```json
{
  "app": {},
  "android": {},
  "startup": {},
  "runtime": {},
  "shortcut": {},
  "container": {}
}
```

La sección `container` deberá representar todos los campos que hoy se guardan en `.container`, incluidos resolución, variables, CPU, gráficos, audio, componentes, unidades, HUD, inicio, Box64, tema y Wine.

## Exclusiones de esta versión

- No se requiere root ni una aplicación del sistema.
- No se requiere autoejecución inmediatamente al terminar la instalación Android.
- No se permitirá editar opciones desde la interfaz final.
- No se fija todavía la aplicación Windows definitiva que reemplazará a `TestApp`.

## Criterios pendientes de prueba

- Verificado: arranque oculto y aplicación automática en `EXEC-007`.
- Verificado: paquete derivado sin relleno ni truncamiento (`com.testapp`), transformación de rootfs mediante alias de descriptor y ejecución en `EXEC-009`.
- Implementado; prueba de cierre natural: `N/R`.
- Verificado parcialmente: Gradle valida la presencia del JSON, el asset y los campos de compilación requeridos.
