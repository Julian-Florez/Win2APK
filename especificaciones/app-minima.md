# Especificación de la aplicación mínima

- **Identificador:** WIN2APK-TEST-001
- **Nombre:** Win2APK Test
- **Versión inicial:** 0.1
- **Ejecutable:** `Win2APKTest.exe`
- **Estado:** especificación inicial

## 1. Propósito

Proporcionar una aplicación Windows propia y controlada para validar que Win2APK puede empaquetar una aplicación preparada junto con un entorno de compatibilidad y generar un APK instalable en Android.

La aplicación no pretende representar la complejidad de una aplicación Windows real. Su función es producir un caso reproducible para verificar el flujo básico de construcción y ejecución.

## 2. Entrada esperada para Win2APK

La aplicación se entregará como una carpeta portable que contenga, como mínimo:

```text
Win2APKTest/
└── Win2APKTest.exe
```

No se utilizará un instalador. La primera versión debe poder ejecutarse desde la carpeta de entrega en un entorno Windows compatible.

## 3. Requisitos funcionales

| ID | Requisito |
|---|---|
| RF-01 | La aplicación debe iniciar mediante `Win2APKTest.exe`. |
| RF-02 | Al iniciar debe mostrar una ventana gráfica. |
| RF-03 | La ventana debe mostrar inicialmente el texto “Hola mundo”. |
| RF-04 | La ventana debe incluir un botón visible e interactivo. |
| RF-05 | Al activar el botón, el texto debe cambiar a “Texto cambiado”. |
| RF-06 | Al activar nuevamente el botón, el texto debe volver a “Hola mundo”. |
| RF-07 | El cambio de texto debe poder repetirse sin reiniciar la aplicación. |
| RF-08 | La aplicación debe poder cerrarse mediante los controles normales de la ventana. |

## 4. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | La aplicación debe ser portable y no requerir un instalador. |
| RNF-02 | La compilación inicial debe estar orientada a Windows x64. |
| RNF-03 | Las dependencias deben ser mínimas, conocidas y documentadas. |
| RNF-04 | La aplicación no debe requerir permisos de administrador. |
| RNF-05 | La aplicación no debe depender de conexión a Internet. |
| RNF-06 | La respuesta del botón debe ser determinista para facilitar la medición. |
| RNF-07 | La aplicación debe permitir repetir la prueba de interacción al menos diez veces consecutivas. |

## 5. Elementos excluidos

La versión 0.1 no incluirá:

- persistencia de datos;
- acceso a archivos del usuario;
- servicios o procesos en segundo plano;
- drivers;
- base de datos;
- red;
- audio o video;
- instalador;
- actualización automática;
- funciones específicas de Android.

Estas exclusiones evitan introducir dependencias que dificulten atribuir los resultados al proceso de empaquetado.

## 6. Flujo de interacción

```text
Inicio
  ↓
Mostrar “Hola mundo”
  ↓
Usuario activa el botón
  ↓
Mostrar “Texto cambiado”
  ↓
Usuario activa nuevamente el botón
  ↓
Mostrar “Hola mundo”
```

## 7. Criterios de aceptación

La aplicación mínima se considera válida antes de empaquetarla cuando:

- inicia correctamente en Windows;
- muestra la ventana principal;
- muestra “Hola mundo” al iniciar;
- cambia a “Texto cambiado” después de activar el botón;
- vuelve a “Hola mundo” después de una segunda activación;
- repite el ciclo diez veces sin error;
- se cierra sin generar un fallo inesperado;
- puede copiarse y ejecutarse desde otra carpeta sin instalador.

El caso se considera validado dentro de Win2APK cuando el APK generado reproduce estos criterios en cada dispositivo definido en [`documentacion/01-app-minima-y-dispositivos-objetivo.md`](../documentacion/01-app-minima-y-dispositivos-objetivo.md).

## 8. Evidencias que deben conservarse

Para cada prueba se conservarán:

- versión o hash del ejecutable utilizado;
- configuración de empaquetado;
- tamaño del APK generado;
- dispositivo y versión de Android;
- resultado de instalación;
- resultado del primer inicio;
- resultado de las interacciones;
- tiempo de inicio;
- capturas de pantalla o video cuando sea necesario;
- registro de errores.

## 9. Relación con la tesis

Esta aplicación sirve como caso controlado para medir la viabilidad inicial del empaquetado automatizado. No se utilizará para afirmar que Win2APK es compatible con todo el software Windows ni para evaluar aplicaciones con dependencias que todavía estén fuera del alcance del prototipo.
