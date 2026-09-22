# Fuentes y trazabilidad

Fecha de consulta externa: **22 de septiembre de 2026**.

## Fuentes del proyecto

| Uso | Fuente principal | Alcance |
|---|---|---|
| Problema y objetivo | `documentacion/00-contexto-del-proyecto.md` | Contexto y formulación inicial; pregunta e hipótesis pendientes. |
| Alcance de la CLI | `documentacion/13-decision-cli-linux-configuracion-v2.md`, `especificaciones/cli-empaquetado.md`, `cli/src/` | Estado reciente de la herramienta. |
| Winlator Core | `documentacion/02-plan-winlator-core.md`, `especificaciones/winlator-core.md`, `winlator/app/` | Preparación de contenedor, acceso directo y arranque. |
| Interfaz | `documentacion/14-decision-interfaz-material3-adaptativa.md`, `especificaciones/interfaz-material3.md` | UI adaptativa y controles. |
| Distribución | `especificaciones/distribucion-datos-juego.md`, `EXEC-012`, `EXEC-047`, `EXEC-049` | Límite monolítico, asset packs y entrega. |
| CoreCLR | `limitaciones/01-error-coreclr-gc-winlator.md`, `EXEC-001` | Error, cambio y evidencia posterior. |
| Demo estable | `EXEC-075`, `RUN-20260922-002` | Resultado observado en Redmi. |
| Fallo más reciente | `EXEC-074`, `RUN-20260922-001`, limitación 43 | Error de pack local-testing en Lenovo. |
| Método | `ejecuciones/plantilla-metricas.md`, `metricas/README.md` | Condiciones, medición y reglas de interpretación. |
| Estado del arte | `review_output/executive_review_report.md`, `review_output/gap_analysis.md`, `review_output/prisma_summary.md` | Síntesis de 48 estudios incluidos. |

## Procedencia de assets

| Asset de la presentación | Origen inmutable | Uso |
|---|---|---|
| `win2apktest-ejecucion-manual.png` | `ejecuciones/01-linea-base-manual-winlator-tb-j606f/evidencias/01-win2apktest-winlator-tb-j606f.png` | Línea base manual. |
| `cuphead-aab-segmentado.png` | `ejecuciones/14-aab-segmentado-cuphead-lenovo/evidencias/cuphead-game-menu.png` | Evidencia de payload segmentado, disponible para respaldo documental. |
| `bomb-rush-redmi-t060.png` | `metricas/runs/RUN-20260922-002/screenshots/redmi-note-8/t060.png` | Prototipo y resultado actual. |
| `error-pack-lenovo-t060.png` | `metricas/runs/RUN-20260922-001/screenshots/lenovo-tb-j606f/t060.png` | Limitación reciente. |
| `gamepad-dpad-presionado.png` | `metricas/runs/RUN-20260921-008/screenshots/redmi-note-8/interactive-dpad-up-pressed.png` | Evidencia suplementaria de feedback táctil. |
| `gamepad-dpad-liberado.png` | `metricas/runs/RUN-20260921-008/screenshots/redmi-note-8/interactive-dpad-up-released.png` | Evidencia suplementaria de retorno visual. |
| `panel-runtime-lenovo.png` | `metricas/runs/RUN-20260920-015/screenshots/lenovo-tb-j606f/panel-no-exit.png` | Panel del runtime en tablet. |
| `demo-redmi-bomb-rush-18s.mp4` | Derivado de `RUN-20260922-002/.../demo-45s.mp4` | Respaldo de demo, recortado a 18 s y escalado a 1920 px. |

SHA-256 del video de respaldo:

```text
e370ede6a58ac0c14b1e8447b9ec667a19510d9048ee9dbee73aff05e2723864
```

No se incorporaron imágenes obtenidas de la web.

## Documentación técnica externa, APA 7

Android Developers. (2026). *About Android App Bundles*. Google.
https://developer.android.com/guide/app-bundle

Uso: sustenta que el AAB es un formato de publicación y que Google Play genera
APK optimizados. No se usa para afirmar que Win2APK ya esté publicado.

Android Developers. (2026). *Play Asset Delivery*. Google.
https://developer.android.com/guide/playcore/asset-delivery

Uso: sustenta los modos `install-time`, `fast-follow` y `on-demand`, y la
entrega de recursos grandes mediante asset packs.

Android Developers. (2026). *Test asset delivery*. Google.
https://developer.android.com/guide/playcore/asset-delivery/test

Uso: sustenta el flujo de pruebas locales con `bundletool --local-testing`.

Android Developers. (2026). *Behavior changes: Apps targeting API 29 and
higher*. Google.
https://developer.android.com/about/versions/10/behavior-changes-10

Uso: contexto oficial para la restricción W^X y ejecución desde el directorio
de datos. La causa específica de Win2APK se basa en sus AVC y ejecuciones, no
solo en esta página.

Android Developers. (2026). *Meet Google Play's target API level requirement*.
Google. https://developer.android.com/google/play/requirements/target-sdk

Uso: sustenta que target 28 no cumple los requisitos modernos de publicación.
La fecha límite es temporal y debe verificarse de nuevo antes de una entrega a
Play.

Box64 contributors. (2026). *Box64: Linux userspace x86-64 emulator with a
twist* [Software]. GitHub. https://github.com/ptitSeb/box64

Uso: sustenta el rol de Box64 al ejecutar programas x86-64 de espacio de
usuario en sistemas no x86-64, incluido ARM64.

Mesa contributors. (2026). *Freedreno*. The Mesa 3D Graphics Library.
https://docs.mesa3d.org/drivers/freedreno.html

Uso: sustenta que Turnip es un driver Vulkan de Mesa para GPU Adreno 6xx. No se
generaliza a todo hardware Qualcomm.

Rebohle, P., & DXVK contributors. (2026). *DXVK* [Software]. GitHub.
https://github.com/doitsujin/dxvk

Uso: sustenta que DXVK traduce Direct3D 8, 9, 10 y 11 a Vulkan para ejecutar
aplicaciones 3D en Linux con Wine.

The Wine Project. (2026). *About Wine*. WineHQ. https://www.winehq.org/about

Uso: sustenta que Wine es una capa de compatibilidad y traduce llamadas de API
Windows a POSIX; no es una máquina virtual.

Winlator contributors. (2026). *Winlator* [Software]. GitHub.
https://github.com/brunodev85/winlator

Uso: sustenta la descripción del proyecto base como una aplicación Android que
usa Wine y Box86/Box64 para aplicaciones Windows. La arquitectura específica
de Win2APK se verifica en su fork y no se infiere del README upstream.

## Referencias académicas seleccionadas, APA 7

Lefeuvre, H., Gain, G., Bădoiu, V.-A., Dinca, D., Schiller, V.-R., Raiciu, C.,
Huici, F., & Olivier, P. (2024). Loupe: Driving the development of OS
compatibility layers. In *Proceedings of the 29th ACM International Conference
on Architectural Support for Programming Languages and Operating Systems,
Volume 1* (pp. 249-267). Association for Computing Machinery.
https://doi.org/10.1145/3617232.3624861

Uso: sustenta que una capa de compatibilidad debe evaluarse contra aplicaciones,
cargas y criterios explícitos; no prueba compatibilidad Windows-Android.

Yen, J., Wang, J., Huang, Z., Wei, Z., Zhang, Z., Chen, C., Yu, S., Wang, Y.,
Wang, H., & Qi, Z. (2025). ARMing x86 games: Accelerating binary translation
using software-only validated flag speculation. In *Proceedings of the 23rd
Annual International Conference on Mobile Systems, Applications and Services*.
Association for Computing Machinery. https://doi.org/10.1145/3711875.3729163

Uso: evidencia reciente sobre Box64 y traducción x86 a ARM64 en juegos. La
plataforma del estudio es Ubuntu ARM64, no Android, por lo que sus métricas no
se trasladan a Win2APK.

Zimmermann, M., Breitenbücher, U., Harzenetter, L., Leymann, F., & Yussupov, V.
(2020). Self-contained service deployment packages. In *Proceedings of the
10th International Conference on Cloud Computing and Services Science* (pp.
371-381). SciTePress. https://doi.org/10.5220/0009414903710381

Uso: antecedente del patrón de trasladar resolución de dependencias al builder.
No cubre Android, Wine ni traducción entre ISA.

## Reglas para citar durante la sustentación

- Resultados propios: mencionar `EXEC-###` o `RUN-...`.
- Arquitectura de terceros: mencionar el proyecto y dejar la referencia
  completa en backup.
- Cifras de artículos: no usarlas como predicción de Win2APK.
- Afirmaciones temporales de Android o Google Play: verificar de nuevo antes de
  publicar.
