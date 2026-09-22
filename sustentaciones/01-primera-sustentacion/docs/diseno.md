# Decisiones de diseño

## Design read

Presentación académica tecnológica para una profesora de Ingeniería de
Sistemas, basada en capas, evidencia y transformación. Debe sentirse como una
ponencia técnica clara, no como un sitio comercial.

- ENERGY: 2. Sobria y concentrada.
- RHYTHM: 3. Alterna evidencia a pantalla completa, diagramas y contraste.
- MOTION: 2. Solo transiciones cortas y revelado de arquitectura.

## Identidad

El símbolo une dos marcos desplazados mediante una pieza central. El marco
izquierdo representa la aplicación de origen; el derecho, el paquete y entorno
de destino; la pieza intermedia expresa traducción e integración. No reproduce
las ventanas de Microsoft ni la silueta de Android.

Archivos maestros:

- `assets/logo/win2apk-symbol.svg`
- `assets/logo/win2apk-logo.svg`

## Paleta

| Uso | Color | Razón |
|---|---|---|
| Texto y estructura | `#172033` | Contraste alto y tono técnico formal. |
| Acción y resultado | `#50C878` / `#2FAA69` | Continuidad con la paleta ya documentada del proyecto. |
| Fondo | `#FBFCFA` | Superficie clara sin blanco agresivo. |
| Decisión o cautela | `#B45309` | Separa decisión de resultado. |
| Limitación | `#A93226` | Uso reservado para fallos y límites. |

No se usan gradientes. El color verde no significa “éxito universal”; marca
componentes propios, resultados observados o navegación.

## Tipografía

Se usa la pila local `Segoe UI, Arial, Helvetica, sans-serif`. No se descarga
ninguna fuente y no se incorpora un binario tipográfico adicional. Esto reduce
dependencias entre Linux y Windows. Los títulos se mantienen entre 48 y 78 px
en el lienzo base de 1600 × 900.

## Composición

- Lienzo fijo 16:9 escalado al viewport.
- Barra lateral de 18 px como firma visual y orientación de sección.
- Una afirmación dominante por diapositiva.
- Evidencia fotográfica grande, con pie que identifica ejecución y alcance.
- Bloques sin decoración ornamental; cada borde indica estructura o estado.
- Se evita repetir una captura salvo cuando el contraste entre resultado y
  limitación es el argumento de la diapositiva.

## Accesibilidad

- Contraste alto entre texto y fondo.
- Navegación completa por teclado.
- Foco visible de 4 px.
- Texto alternativo en capturas y logo.
- Respeto por `prefers-reduced-motion`.
- El video tiene botón, tecla dedicada y póster estático para el PDF.
- El significado de resultado, decisión, pendiente y limitación no depende solo
  del color: cada estado está escrito.
