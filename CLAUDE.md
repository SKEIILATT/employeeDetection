# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Simulador de Entrevistas

> Estado actual: el repositorio solo contiene este archivo. Todavía no hay código, comandos de build ni tests; agregarlos aquí a medida que existan.

Plataforma para practicar entrevistas de trabajo frente a una entrevistadora virtual ("Laura") en una videollamada con cámara y micrófono. Al terminar, el estudiante recibe un informe con feedback sobre lo que dijo, cómo lo dijo y su lenguaje no verbal.

## Contexto

- **Usuarios:** estudiantes de un bootcamp (grupos de 15 a 40 personas).
- **Tipo de entrevista:** solo habilidades blandas por ahora. La entrevista técnica queda para más adelante.
- **Sesiones:** 10 a 15 minutos (modo estándar). Una pregunta de apertura, 4 preguntas de competencias distintas y una de cierre. Hay repreguntas cuando una respuesta queda incompleta.
- **Banco de preguntas y rúbricas:** https://claude.ai/artifact/RXZCRe21wbEPEseywCmvhJ
  - 42 preguntas en 7 competencias, basadas en las Career Readiness Competencies de NACE: comunicación, trabajo en equipo, pensamiento crítico, profesionalismo y presión, liderazgo, aprendizaje y adaptabilidad, y desarrollo de carrera.
  - Escala de 1 a 5 según el método STAR (Situación, Tarea, Acción, Resultado).
- **Mockup de pantallas (videollamada e informe):** https://claude.ai/artifact/3BqhXhUgSaqsqCPY65PmcT

## Qué evalúa el informe

| Área | Fuente | ¿Visión por computadora? |
|---|---|---|
| Contenido | Transcripción + LLM con la rúbrica | No |
| Forma de hablar (muletillas, velocidad, pausas) | Transcripción con marcas de tiempo | No |
| Voz (volumen, monotonía) | Audio | No |
| Lenguaje no verbal (mirada, postura, movimiento) | MediaPipe en el navegador | Sí |

## Stack

- **Frontend:** Angular, con MediaPipe (Face y Pose Landmarker) en el navegador. Avatar 2D en SVG o Lottie, con la boca animada según el volumen del audio.
- **Backend:** ASP.NET Core, PostgreSQL y SignalR. Arquitectura hexagonal: el dominio (sesiones, rúbricas, puntajes) no depende de los proveedores externos (LLM, almacenamiento).
- **Agente de voz:** Python. Pipecat en la fase 0; para el MVP se evalúa seguir con Pipecat o pasar a LiveKit Agents.
  - Voz a texto: faster-whisper
  - Texto a voz: Piper (voz en español)
  - Cerebro de Laura: Qwen
- **LLM:** Qwen local con LM Studio para el desarrollo (servidor compatible con OpenAI en `http://localhost:1234/v1`). Más adelante, por API o en un servidor propio con vLLM. Usar siempre la interfaz compatible con OpenAI para poder cambiar de proveedor solo con la URL.
  - Conversación: un modelo mediano y rápido.
  - Evaluación con la rúbrica: un modelo más grande, porque corre una sola vez al final.
- **Infraestructura futura:** MinIO para las grabaciones y Keycloak (o la autenticación de .NET) para el login.
- **Preferencia:** usar herramientas open source siempre que se pueda.

## Arquitectura (MVP)

1. Angular le pide a .NET iniciar una sesión.
2. .NET elige las preguntas del banco y devuelve los datos para conectarse a la sala.
3. Angular se conecta; MediaPipe analiza la cámara en el navegador.
4. El agente de Python conduce la entrevista como Laura.
5. Al terminar, el agente envía la transcripción a .NET y Angular envía las métricas de visión.
6. .NET evalúa con la rúbrica y genera el informe.

## Fases

- **Fase 0 (ACTUAL): prueba de concepto de voz.** Un script en Python: micrófono → faster-whisper → Qwen (LM Studio) → Piper → parlantes. Sin avatar, sin Angular y sin .NET. Objetivo: validar que la conversación en español se sienta natural (respuesta en ~1 a 2 segundos, sin interrumpir al estudiante en sus pausas).
- **Fase 1: MVP.** Angular + .NET + agente de voz, avatar 2D simple e informe de contenido con la rúbrica.
- **Fase 2: no verbal.** MediaPipe con mirada, postura y movimiento, y momentos clave en el informe.
- **Fase 3: pulido.** Historial de progreso, panel para instructores y un mejor avatar.

Estructura prevista de la fase 0:

```
fase0-laura/
├── .env                # URL de LM Studio y nombre del modelo
├── requirements.txt
├── prompt_laura.md     # personaje y reglas de la entrevista
└── bot.py
```

## Entorno de desarrollo

- Windows con Git Bash (MINGW64).
- GPU: NVIDIA RTX 5050 Laptop (8 GB VRAM). También hay una Radeon integrada: asegurarse de usar siempre la NVIDIA (runtime CUDA en LM Studio).
- RAM: 16 GB. CPU: AMD Ryzen 5 240.
- Disco: poco espacio libre (~27 GB). No descargar modelos innecesarios.
- Configuración de modelos recomendada:
  - Qwen 4B para empezar, luego probar 8B. Cuantización Q4_K_M, GPU offload al máximo y contexto de 4K a 8K.
  - faster-whisper `small` en int8, en la GPU. Si no hay memoria suficiente, pasarlo a la CPU.
  - Piper en la CPU.
  - Desactivar el modo de razonamiento de Qwen (`/no_think`) para reducir la latencia.
- La serie RTX 50 es nueva: si hay errores de CUDA, actualizar los drivers y los paquetes.
- Context7 está instalado como servidor MCP: usarlo para consultar la documentación actualizada de Pipecat, LiveKit, MediaPipe, etc.

## Reglas de diseño

- El feedback no verbal describe **conductas observables** ("miraste fuera de cámara el 40% del tiempo"), nunca emociones ni personalidad ("parecías nervioso"). Se presenta como sugerencias, no como penalizaciones rígidas, considerando diferencias culturales, neurodivergencia o discapacidad.
- La IA solo usa preguntas del banco. Puede adaptar la redacción al puesto, pero no inventa preguntas.
- **Privacidad:** datos de estudiantes sujetos a la Ley Orgánica de Protección de Datos Personales de Ecuador. Pedir consentimiento explícito, definir cuánto tiempo se guardan las grabaciones y permitir borrarlas. El análisis de video corre en el navegador y solo se guardan las métricas.
- Las API keys van en `.env`, que está en `.gitignore` desde el primer commit.

## Convenciones

- El código y los comentarios pueden estar en inglés; los textos que ve el usuario, en español.
- Trabajar en pasos pequeños y verificables. En la fase 0, priorizar que funcione de punta a punta antes de optimizar.
