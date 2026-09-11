# AGENTS.md

Instrucciones para el agente de IA que abra este repositorio (Claude Code, Cursor, Codex, Copilot, Gemini). Se cargan solas: no hay que pegar nada en ningun chat.

## Que es este repositorio

Es el codigo base de un reto de aprendizaje de Pragma: **Implementación de un sistema de respuestas normativas con modelos generativos**.

| | |
|---|---|
| Tema | aplicaciones sobre modelos generativos |
| Nivel | senior-l2 |
| Chapter | Ciencia de Datos — Ingeniero de IA |
| Especialidad | Ingeniero de IA |
| Stack | Python 3.13 / FastAPI 0.115 |
| Patron arquitectonico | Patrón RAG con capas de recuperación, generación y evaluación, orquestado con LangGraph |
| Tiempo estimado | 2 semanas |

## Tu tarea

Dejar este proyecto en estado **verificable**: que el comando de verificacion corra sin errores. Escribi los archivos en disco, en este repositorio. No generes ZIPs ni archivos adjuntos.

En orden:

1. Corre `pip install -r requirements.txt && pytest -q` y mira que falla.
2. Completa lo que falte de la lista de abajo: manifiesto de dependencias, punto de entrada, capa de interfaz y las capas del patron declarado.
3. Arregla SOLO los errores que impiden compilar o arrancar.
4. Volve a correr `pip install -r requirements.txt && pytest -q` hasta que pase.
5. Pará ahí.

## Regla dura: las fases son trabajo del humano

**PROHIBIDO implementar los entregables de las fases.** El valor del reto esta en que la persona los resuelva. Tu trabajo es que tenga un proyecto que arranca; el hueco pedagogico se queda como esta.

No resuelvas nada de esto:

- **Fase 1 — Configuración del entorno y recuperación de contexto**: Entorno configurado y mecanismo de recuperación de contexto funcional.
- **Fase 2 — Generación de respuestas estructuradas**: Mecanismo de generación de respuestas estructuradas funcional.
- **Fase 3 — Evaluación y optimización del sistema**: Sistema optimizado con evaluación medible de la precisión y relevancia de las respuestas.

Distincion operativa:

- **Arreglar** (si): import faltante, tipo que no existe, dependencia sin declarar, error de sintaxis, archivo referenciado que no existe.
- **No tocar** (no): logica de negocio incompleta, validaciones ausentes, secretos hardcodeados, APIs deprecadas que funcionan, concurrencia insegura, patrones mejorables. Eso es lo que la persona tiene que encontrar.

## Lo que falta y tenes que completar

### 1. Archivos que la arquitectura declara (2 de 19)

La propuesta arquitectonica del reto los lista y no llegaron al repo. Crealos con implementacion real, respetando la capa en la que viven:

- [ ] `app/retrieval/vector_store.py`
- [ ] `app/chains/normative_chain.py`

### 2. Referencias colgando (7)

Salieron de un analisis estatico del codigo que SI esta en el repo. Cada una rompe la compilacion:

- [ ] `app/utils/aws_client.py` — `Settings.info`
      Se invoca `info` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/aws_client.py` — `Settings.debug`
      Se invoca `debug` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/aws_client.py` — `Settings.error`
      Se invoca `error` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/aws_client.py` — `Settings.warning`
      Se invoca `warning` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/error_handler.py` — `ErrorResponse.log`
      Se invoca `log` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/error_handler.py` — `ErrorResponse.info`
      Se invoca `info` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/utils/error_handler.py` — `ErrorResponse.error`
      Se invoca `error` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

### Presentes (17)

- `pyproject.toml`
- `app/main.py`
- `app/config/settings.py`
- `app/retrieval/normative_repository.py`
- `app/models/schemas.py`
- `app/prompts/normative_query_template.txt`
- `app/eval/evaluation_dataset.json`
- `app/eval/metrics.py`
- `app/utils/aws_client.py`
- `app/utils/error_handler.py`
- `tests/test_retrieval.py`
- `tests/test_chain.py`
- `tests/test_eval.py`
- `infra/terraform/main.tf`
- `infra/terraform/iam_policy.json`
- `Dockerfile`
- `docker-compose.yml`

### Capas del patron declarado

Cada una tiene que existir como directorio real con al menos un archivo. Codigo plano en la raiz no satisface el patron.

- `app`
- `app/prompts`
- `app/retrieval`
- `app/chains`
- `app/eval`
- `app/models`
- `app/config`
- `app/utils`
- `tests`
- `infra`

## Verificacion

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando pasando es la definicion de "terminado" para vos.

## Convenciones que tenes que respetar

- Un solo ecosistema: no declares librerias de otro lenguaje ni mezcles gestores de paquetes.
- Toda libreria que uses tiene que estar declarada en el manifiesto de dependencias.
- Todo import declarado tiene que usarse; todo tipo usado tiene que existir o venir de una dependencia declarada.
- El patron es **Patrón RAG con capas de recuperación, generación y evaluación, orquestado con LangGraph**: los contratos (interfaces, puertos) los define la capa interna y los implementa la externa, nunca al revés.
- Los archivos que crees llevan implementacion real, no stubs: sin `TODO`, sin cuerpos vacios, sin `// getters y setters`.

## Contexto del candidato

Sirve para calibrar el nivel del codigo, no para resolver las fases.

- Perfil: Chapter Ciencia de Datos, Especialidad Ingeniero de IA, Tecnología AWS Bedrock, Senior
- Brecha que el reto ataca: Construye soluciones sobre modelos generativos con recuperacion de contexto, salida estructurada y evaluacion medible
- Mision: Responder consultas sobre la normativa interna

---

*Generado por Challenge Generator — Pragma. `README.md` tiene el enunciado completo del reto para la persona. `PROMPT_MEJORA.md` es la variante para pegar en un chat, si se prefiere ese flujo.*
