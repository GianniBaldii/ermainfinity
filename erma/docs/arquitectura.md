# Arquitectura inicial

INFINITY ERMA esta organizada como una aplicacion local-first con frontend web y backend REST.

## Backend

El backend vive en `erma/backend` y usa FastAPI.

- `app/main.py`: crea la aplicacion FastAPI y configura CORS.
- `api/routes.py`: expone los endpoints HTTP.
- `core/state.py`: lee y escribe el estado actual en `data/state.json`.
- `core/intent_matcher.py`: busca palabras clave dentro del texto recibido.
- `core/command_router.py`: envia cada intent al modulo correspondiente.
- `core/registry.py`: mantiene la relacion entre intents y handlers.
- `core/response.py`: define la respuesta estandar.
- `modules/`: contiene handlers por responsabilidad.

## Flujo de comando

1. El frontend envia texto a `POST /command`.
2. `IntentMatcher` normaliza el texto y busca palabras clave.
3. `CommandRouter` toma el intent detectado.
4. `CommandRegistry` entrega el handler correspondiente.
5. El handler actualiza o consulta estado.
6. El backend devuelve una respuesta estandar.

## Persistencia

La persistencia inicial es JSON para mantener el sistema simple:

- `state.json`: estado actual.
- `commands.json`: intents y palabras clave.
- `phrases.json`: frases disponibles.

SQLite queda reservado para una etapa futura.

## Frontend

El frontend vive en `erma/frontend` y usa React, Vite, TypeScript y TailwindCSS.

La pantalla inicial muestra avatar, estado, emocion, mensaje, input de comando, botones rapidos y ultima respuesta del backend.
