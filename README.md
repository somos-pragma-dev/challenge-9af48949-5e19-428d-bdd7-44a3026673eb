# Implementación de un sistema de respuestas normativas con modelos generativos

El equipo de cumplimiento necesita un sistema que pueda responder consultas sobre la normativa interna utilizando modelos generativos. El sistema debe recuperar contexto relevante, generar una respuesta estructurada y permitir una evaluación medible de la precisión y relevancia de las respuestas. Los actores involucrados son el 'usuario del sistema de cumplimiento', el 'modelo generativo' y el'repositorio de normativas'. El sistema debe manejar un volumen de 100 consultas por hora con una latencia máxima de 5 segundos por respuesta. La consistencia de las respuestas debe mantenerse bajo condiciones de alta carga y la precisión debe ser verificable contra un conjunto de pruebas.

## Informacion General

| Campo | Valor |
|-------|-------|
| **Tema** | aplicaciones sobre modelos generativos |
| **Nivel** | senior-l2 |
| **Tipo** | practical |
| **Tiempo estimado** | 2 semanas |

## Fases del Reto

### Fase 0: Configuración del Proyecto

**Objetivo:** Obtener el proyecto base funcional enviando el Código Base a un asistente de IA, que lo analizará, corregirá errores y generará un ZIP listo para usar.

**Tiempo estimado:** 15-30 minutos

**Instrucciones:**

- Asegúrate de tener instalado para ejecutar el proyecto: Un IDE o editor de código.
- Copia todo el contenido del campo **Código Base** de este reto — incluyendo el texto de instrucciones que aparece al inicio.
- Abre un asistente de IA (Claude en claude.ai, ChatGPT o Gemini — se recomienda Claude), pega el contenido copiado en el chat y envíalo.
- El asistente analizará los archivos, corregirá errores y generará un archivo ZIP descargable. Descárgalo y extráelo en la carpeta donde quieras trabajar.
- Verifica que el proyecto arranca sin errores.

**Entregable:** El proyecto compila/arranca sin errores.

<details>
<summary>Pistas de conocimiento</summary>

- Copia el Código Base completo incluyendo el texto de instrucciones al inicio — esas instrucciones le indican al asistente exactamente qué hacer con los archivos.
- Si el asistente no genera el ZIP automáticamente al terminar el análisis, escríbele: "genera el ZIP ahora".
- Si el proyecto tiene errores al arrancar, comparte el mensaje de error con el mismo asistente para que lo corrija.

</details>

### Fase 1: Configuración del entorno y recuperación de contexto

**Objetivo:** Establecer el entorno de trabajo y recuperar contexto relevante para las consultas normativas.

**Tiempo estimado:** 3 días

**Instrucciones:**

- Configura el entorno para utilizar un modelo generativo.
- Implementa la recuperación de contexto relevante desde el repositorio de normativas.
- Asegura que el sistema pueda manejar un volumen de 100 consultas por hora con una latencia máxima de 5 segundos por respuesta.

**Entregable:** Entorno configurado y mecanismo de recuperación de contexto funcional.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la estructura del repositorio de normativas y cómo se puede acceder de manera eficiente.
- Piensa en cómo manejar la carga de consultas para mantener la latencia dentro del umbral especificado.

</details>

### Fase 2: Generación de respuestas estructuradas

**Objetivo:** Implementar la generación de respuestas estructuradas utilizando el modelo generativo.

**Tiempo estimado:** 5 días

**Instrucciones:**

- Utiliza el modelo generativo para generar respuestas a las consultas.
- Asegura que las respuestas sean estructuradas y coherentes con la normativa interna.
- Verifica que el sistema pueda mantener la consistencia de las respuestas bajo condiciones de alta carga.

**Entregable:** Mecanismo de generación de respuestas estructuradas funcional.

<details>
<summary>Pistas de conocimiento</summary>

- Considera cómo estructurar las respuestas para que sean coherentes y útiles para el usuario.
- Piensa en cómo mantener la consistencia de las respuestas bajo condiciones de alta carga.

</details>

### Fase 3: Evaluación y optimización del sistema

**Objetivo:** Evaluar la precisión y relevancia de las respuestas generadas y optimizar el sistema.

**Tiempo estimado:** 4 días

**Instrucciones:**

- Evalúa la precisión y relevancia de las respuestas generadas contra un conjunto de pruebas.
- Identifica áreas de mejora y optimiza el sistema para mejorar el rendimiento.
- Asegura que el sistema pueda manejar un aumento en el volumen de consultas sin comprometer la latencia y la precisión.

**Entregable:** Sistema optimizado con evaluación medible de la precisión y relevancia de las respuestas.

<details>
<summary>Pistas de conocimiento</summary>

- Considera cómo estructurar el conjunto de pruebas para evaluar la precisión y relevancia de las respuestas.
- Piensa en estrategias de optimización para mejorar el rendimiento del sistema.

</details>

## Dimensiones Evaluadas

- **queEs**: ¿Qué es un modelo generativo y cómo se utiliza en este contexto?
- **paraQueSirve**: ¿Para qué sirve la recuperación de contexto en este sistema?
- **comoSeUsa**: ¿Cómo se usa el modelo generativo para generar respuestas estructuradas?
- **erroresComunes**: ¿Cuáles son los errores comunes al generar respuestas con modelos generativos y cómo se pueden evitar?
- **queDecisionesImplica**: ¿Qué decisiones implica la optimización del sistema para manejar un aumento en el volumen de consultas?

## Criterios de Evaluacion

- Configuración correcta del entorno y recuperación eficiente de contexto.
- Generación de respuestas estructuradas coherentes y útiles.
- Evaluación medible de la precisión y relevancia de las respuestas.
- Optimización del sistema para manejar un aumento en el volumen de consultas sin comprometer la latencia y la precisión.

## Como trabajar con un asistente de IA

Hay dos caminos, elegi uno:

- **AGENTS.md** (recomendado) — instrucciones nativas del repo. Abri esta carpeta con tu agente local (Claude Code, Cursor, Codex, Copilot, Gemini) y las carga solo. Sabe que archivos faltan y con que comando se verifica, y completa el scaffold escribiendo en disco.
- **PROMPT_MEJORA.md** — para copiar y pegar en un chat (claude.ai, ChatGPT). Devuelve un ZIP con el proyecto. Sirve si no tenes un agente en el IDE.

Ninguno de los dos resuelve las fases del reto: eso es tu trabajo.

## Verificacion

El proyecto esta listo para trabajar cuando este comando corre sin errores:

```bash
pip install -r requirements.txt && pytest -q
```

---

*Reto generado automaticamente por Challenge Generator - Pragma*
