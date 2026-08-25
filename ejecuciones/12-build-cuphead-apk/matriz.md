# Ejecución 12: compilación de APK con asset de Cuphead

- **ID:** `EXEC-012`
- **Fecha:** 2026-08-24
- **Tipo:** compilación automatizada
- **Resultado general:** Fallido por límite de tamaño durante el empaquetado de assets
- **Método:** `ANDROID_HOME=/home/julian/Android/Sdk ANDROID_SDK_ROOT=/home/julian/Android/Sdk bash gradlew assembleDebug --console=plain`

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | Cuphead | Configuración `config/win2apk.json` |
| Ejecutable | `Cuphead.exe` | Asset generado desde la instalación Lutris |
| Asset | `winlator/app/app/src/main/assets/cuphead.tzst` | 4.782.573.186 bytes |
| Hash SHA-256 del asset | `33aad774c30e07be8088160d35bacdd191eae7d06ed0fd507f396c726d7eff93` | Medición local |
| Entorno | Linux; Gradle daemon; Android Gradle Plugin 7.2.2 | Salida de Gradle |
| Android SDK | `/home/julian/Android/Sdk` | SDK localizado localmente |
| Compile SDK | 34 | Configuración de `winlator/app/app/build.gradle` |
| NDK | `24.0.8215888` | SDK local y configuración del proyecto |
| Dispositivo Android | N/A | No se generó APK utilizable |
| ABI | `arm64-v8a` configurada | `build.gradle`; no llegó a validar APK Cuphead |
| Fecha y hora | 2026-08-24, aproximadamente 14:03–14:04 -0500 | Registro de la ejecución |

## Matriz de criterios

| ID | Criterio | Resultado | Valor/unidad | Condiciones | Evidencia | Observaciones |
|---|---|---|---|---|---|---|
| M-01 | Configuración de Cuphead | Aprobada | `Cuphead`, `C:\Cuphead\Cuphead.exe` | Configuración del proyecto actualizada | [log](./logs/build.md) | El descriptor apunta al asset generado |
| M-02 | Preparación de assets Core | Aprobada | 447 reemplazos en `rootfs.tzst` | Gradle con SDK localizado | [log](./logs/build.md) | La tarea `prepareCoreAssets` terminó |
| M-03 | Compresión de assets APK | Fallida | `Required array size too large` | Tarea `:app:compressDebugAssets` | [log](./logs/build.md) | El asset de 4,45 GiB supera la capacidad del empaquetador usado |
| M-04 | APK Cuphead utilizable | No generada | N/A | La compilación terminó con error | [log](./logs/build.md) | El APK existente en `build/outputs` es anterior y contiene `test_app.tzst` |
| M-05 | Instalación en Android | N/A | N/A | No hay APK Cuphead | N/A | Pendiente de estrategia de distribución |
| M-06 | Tamaño del APK | N/R | N/R | No se obtuvo artefacto nuevo | N/A | No usar el APK histórico de 2026-08-18 como resultado |
| M-07 | Tasa de éxito | 0/1 para esta compilación | Una ejecución | Condiciones documentadas en este registro | [log](./logs/build.md) | No representa compatibilidad universal |

## Fallos y decisiones

- **Limitación relacionada:** [Limitación 08](../../limitaciones/08-asset-cuphead-excede-empaquetado-apk.md).
- **Mensaje exacto:** `Required array size too large`.
- **Decisión:** No usar el APK histórico ni declarar generado un APK de Cuphead. Investigar una distribución del asset fuera del APK o una segmentación compatible antes de volver a compilar.

## Evidencias

- Log: [registro de build](./logs/build.md)
- Asset: `winlator/app/app/src/main/assets/cuphead.tzst` (local, no se incorpora como evidencia Markdown)
- APK nuevo: N/A

## Pendientes

- [ ] Determinar una estrategia de asset externo/OBB/descarga posterior compatible con el alcance del proyecto.
- [ ] Definir si el builder debe rechazar automáticamente publicaciones por encima del límite del empaquetador.
- [ ] Repetir la compilación solo después de resolver la distribución del asset.
