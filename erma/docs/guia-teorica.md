# Guia teorica de INFINITY ERMA

Esta guia explica como funciona el proyecto en su estado actual de MVP textual.
La idea es que puedas mirar una carpeta o un archivo y entender para que existe,
como se conecta con el resto y que parte tendrias que tocar para cambiar algo.

## Vision general

INFINITY ERMA es una base para un asistente personal local. En esta etapa no
usa voz, sensores ni IA conversacional. El MVP funciona con comandos escritos,
estado interno, historial, notas, frases y fecha/hora.

El flujo general es:

1. El usuario abre la interfaz web.
2. El usuario escribe un comando o toca un boton.
3. El frontend manda el comando al backend por HTTP.
4. El backend detecta la intencion del texto.
5. El backend elige un modulo capaz de responder.
6. El modulo actualiza estado, notas o historial segun corresponda.
7. El backend devuelve una respuesta estandar.
8. El frontend actualiza la pantalla.

La separacion principal es:

```text
frontend = pantalla y experiencia visual
backend = logica de ERMA
core = piezas centrales reutilizables del backend
modules = comportamientos concretos de ERMA
data = memoria simple en JSON
scripts = comandos para levantar o apagar el proyecto
docs = explicaciones y plan del proyecto
```

## Estructura del proyecto

```text
erma/
|-- backend/
|   |-- api/
|   |-- app/
|   |-- core/
|   |-- data/
|   |-- modules/
|   |-- tests/
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   `-- package.json
`-- docs/

scripts/
|-- dev.cmd
|-- dev.ps1
|-- dev.sh
|-- stop.cmd
|-- stop.ps1
`-- stop.sh
```

## Como se levanta ERMA

En Windows se usa:

```powershell
.\scripts\dev.cmd
```

Si hay procesos viejos ocupando puertos:

```powershell
.\scripts\dev.cmd -StopExisting
```

En Raspberry/Linux se usa:

```bash
./scripts/dev.sh
```

Si es la primera vez:

```bash
./scripts/dev.sh --install
```

El frontend queda en:

```text
http://127.0.0.1:5173
```

El backend queda en:

```text
http://127.0.0.1:8000
```

En la Raspberry, el script escucha en `0.0.0.0`, asi que tambien se puede abrir
desde otra maquina de la misma red:

```text
http://IP_DE_LA_RASPBERRY:5173
```

## Backend

El backend vive en:

```text
erma/backend
```

Usa FastAPI. FastAPI permite crear endpoints HTTP, que son URLs a las que el
frontend puede llamar.

Ejemplos:

```text
GET /state
POST /command
GET /history
GET /notes
POST /wake
POST /sleep
```

## App: arranque y configuracion

La carpeta:

```text
erma/backend/app
```

contiene piezas de arranque.

### `app/main.py`

Crea la aplicacion FastAPI:

```text
app = FastAPI(...)
```

Tambien configura CORS. CORS permite que el frontend, que corre en el puerto
`5173`, pueda hablar con el backend, que corre en el puerto `8000`.

Sin CORS, el navegador podria bloquear los pedidos del frontend.

### `app/config.py`

Define rutas importantes:

```text
STATE_FILE
COMMANDS_FILE
PHRASES_FILE
HISTORY_FILE
NOTES_FILE
```

Es decir, le dice al backend donde estan los JSON que ERMA usa como memoria.

### `app/bootstrap.py`

Arma las piezas principales:

- crea stores;
- crea el registry;
- registra intents con handlers;
- conecta modulos concretos con el core.

Este archivo responde a la pregunta:

```text
Que capacidades tiene ERMA cargadas al iniciar?
```

Ejemplo conceptual:

```text
sleep -> SleepHandler
wake -> SleepHandler
greeting -> SystemHandler
state -> SystemHandler
phrase -> PhrasesHandler
note_add -> NotesHandler
note_list -> NotesHandler
datetime -> DateTimeHandler
```

## API: puertas de entrada

La carpeta:

```text
erma/backend/api
```

contiene las rutas HTTP.

El archivo principal es:

```text
erma/backend/api/routes.py
```

Ese archivo define que pasa cuando alguien llama a:

```text
GET /state
GET /history
GET /notes
POST /command
POST /wake
POST /sleep
```

`POST /command` es el endpoint mas importante. Recibe texto, por ejemplo:

```json
{
  "text": "recordame comprar pilas"
}
```

y se lo pasa al router de comandos.

## Core: el corazon de ERMA

La carpeta:

```text
erma/backend/core
```

contiene la logica central que no pertenece a un modulo especifico. El `core` no
es "dormir", "notas" o "frases". El `core` es la infraestructura interna que hace
que cualquier modulo pueda existir.

Pensalo asi:

```text
core = motor
modules = habilidades
data = memoria
api = entradas/salidas por HTTP
```

### `core/intent_matcher.py`

Detecta la intencion del usuario.

Lee:

```text
erma/backend/data/commands.json
```

Ese JSON tiene una relacion entre intents y palabras clave:

```json
{
  "sleep": ["dormir", "dormite", "descansar"],
  "note_add": ["recordame", "anotar", "anota", "guardar nota"],
  "datetime": ["que hora es", "que dia es", "fecha", "hora"]
}
```

Si el usuario escribe:

```text
ERMA recordame comprar pilas
```

el matcher encuentra `recordame` y devuelve:

```text
intent = note_add
matched_keywords = ["recordame"]
```

Antes de comparar, normaliza texto:

- pasa a minusculas;
- quita espacios extra;
- quita acentos.

Por eso `que día es` puede coincidir con `que dia es`.

### `core/command_router.py`

Recibe el texto original y coordina el procesamiento.

Su trabajo es:

1. pedir al `IntentMatcher` que detecte el intent;
2. si no hay intent, crear una respuesta `unknown`;
3. si hay intent, pedir al `CommandRegistry` el handler correcto;
4. ejecutar el handler;
5. guardar el resultado en el historial;
6. devolver la respuesta.

Es una pieza central porque une deteccion, ejecucion e historial.

### `core/registry.py`

Guarda la relacion entre intents y handlers.

Un handler es una clase que sabe responder a una intencion. Por ejemplo:

```text
sleep -> SleepHandler
note_add -> NotesHandler
datetime -> DateTimeHandler
```

Si llega el intent `note_add`, el registry entrega el `NotesHandler`.

Si llega un intent que no fue registrado, lanza error. Esto ayuda a detectar
configuraciones incompletas.

### `core/response.py`

Define la respuesta estandar de ERMA.

Todas las respuestas importantes tienen esta forma:

```json
{
  "intent": "note_add",
  "status": "talking",
  "emotion": "alegre",
  "message": "Listo, guarde la nota 1: comprar pilas",
  "matched_keywords": ["recordame"]
}
```

Esto es clave porque el frontend siempre sabe que campos esperar.

### `core/state.py`

Lee y escribe el estado actual de ERMA.

Archivo de datos:

```text
erma/backend/data/state.json
```

Ejemplo:

```json
{
  "status": "sleep",
  "emotion": "cansado",
  "message": "Bueno Gianni, voy a descansar un rato."
}
```

El estado representa como esta ERMA ahora mismo. No es historial. Es la foto
actual.

Estados permitidos:

```text
idle
listening
thinking
talking
sleep
greeting
```

Emociones permitidas:

```text
neutral
alegre
cansado
curioso
```

### `core/history.py`

Guarda comandos procesados y respuestas.

Archivo de datos:

```text
erma/backend/data/history.json
```

Cada entrada guarda:

- fecha/hora;
- comando original;
- intent;
- status;
- emotion;
- message;
- palabras clave detectadas.

El historial sirve para mostrar actividad reciente en el frontend y para tener
una memoria basica de lo que se le pidio a ERMA.

### `core/notes.py`

Guarda y lista notas.

Archivo de datos:

```text
erma/backend/data/notes.json
```

Cada nota tiene:

- `id`;
- `text`;
- `created_at`.

Este core no decide cuando crear una nota. Solo ofrece operaciones simples:

```text
list_notes()
add_note(text)
```

La decision de "este comando significa crear nota" pertenece al `NotesHandler`.

## Modules: habilidades de ERMA

La carpeta:

```text
erma/backend/modules
```

contiene comportamientos concretos. Cada modulo responde a uno o mas intents.

### Sleep

Archivos:

```text
erma/backend/modules/sleep/handler.py
erma/backend/modules/sleep/commands.py
```

Intents:

```text
sleep
wake
```

Hace que ERMA pase a dormida o despierta.

### System

Archivos:

```text
erma/backend/modules/system/handler.py
erma/backend/modules/system/commands.py
```

Intents:

```text
greeting
state
```

Sirve para saludar y consultar como esta ERMA.

### Phrases

Archivos:

```text
erma/backend/modules/phrases/handler.py
erma/backend/modules/phrases/commands.py
```

Intent:

```text
phrase
```

Lee frases desde:

```text
erma/backend/data/phrases.json
```

y devuelve una al azar.

### Notes

Archivos:

```text
erma/backend/modules/notes/handler.py
erma/backend/modules/notes/commands.py
```

Intents:

```text
note_add
note_list
```

Ejemplos:

```text
recordame comprar pilas
anotar revisar el MVP
ver notas
```

Cuando se agrega una nota, el handler extrae el texto posterior a la palabra
clave. Por ejemplo:

```text
ERMA recordame comprar pilas
```

se convierte en nota:

```text
comprar pilas
```

### DateTime

Archivos:

```text
erma/backend/modules/datetime/handler.py
erma/backend/modules/datetime/commands.py
```

Intent:

```text
datetime
```

Ejemplos:

```text
que hora es
que dia es
fecha
hora
```

Devuelve dia, fecha y hora usando el reloj local donde corre el backend. En la
Raspberry, eso significa el reloj de la Raspberry.

## Data: memoria simple

La carpeta:

```text
erma/backend/data
```

contiene archivos JSON.

### `commands.json`

Configura intents y palabras clave.

Si queres que ERMA entienda otra frase para una accion existente, se suele tocar
este archivo.

### `state.json`

Guarda el estado actual.

### `phrases.json`

Guarda frases que el modulo de frases puede devolver.

### `history.json`

Guarda historial de comandos procesados.

### `notes.json`

Guarda notas creadas por comandos tipo `recordame`.

## Flujo completo: comando de nota

Supongamos que escribis:

```text
ERMA recordame comprar pilas
```

El flujo real es:

1. `Home.tsx` recibe el texto del input.
2. `api.ts` manda `POST /command` al backend.
3. `routes.py` recibe el request.
4. `CommandRouter` recibe el texto.
5. `IntentMatcher` normaliza el texto.
6. `IntentMatcher` busca palabras clave en `commands.json`.
7. Encuentra `recordame`.
8. Devuelve intent `note_add`.
9. `CommandRouter` pide al `CommandRegistry` el handler de `note_add`.
10. El registry devuelve `NotesHandler`.
11. `NotesHandler` extrae `comprar pilas`.
12. `NotesHandler` llama a `ErmaNotesStore.add_note(...)`.
13. `notes.json` se actualiza.
14. `NotesHandler` actualiza `state.json`.
15. `CommandRouter` guarda la respuesta en `history.json`.
16. El backend devuelve una `ErmaResponse`.
17. El frontend actualiza estado, respuesta, historial y notas.

Ese flujo muestra como se conectan frontend, API, core, modules y data.

## Frontend

El frontend vive en:

```text
erma/frontend
```

Usa:

- React;
- TypeScript;
- Vite;
- TailwindCSS.

### `src/main.tsx`

Entrada de React. Monta la pantalla principal.

### `src/screens/Home.tsx`

Pantalla principal de ERMA.

Maneja:

- estado actual;
- comando escrito;
- ultima respuesta;
- errores de conexion;
- historial reciente;
- notas recientes;
- botones rapidos.

Cuando carga, pide:

- `GET /state`;
- `GET /history`;
- `GET /notes`.

Cuando ejecuta un comando, despues refresca historial y notas.

### `src/services/api.ts`

Es el puente entre frontend y backend.

Define:

- `getState()`;
- `getHistory()`;
- `getNotes()`;
- `sendCommand(text)`;
- `wakeErma()`;
- `sleepErma()`.

La URL del backend se calcula con el mismo host desde donde se abrio el frontend:

```text
http://HOST_ACTUAL:8000
```

Esto importa en Raspberry. Si abris:

```text
http://192.168.1.27:5173
```

el frontend llama automaticamente a:

```text
http://192.168.1.27:8000
```

### `src/types/erma.ts`

Define los tipos TypeScript usados por la pantalla:

- `ErmaStatus`;
- `ErmaEmotion`;
- `ErmaState`;
- `ErmaResponse`;
- `ErmaHistoryEntry`;
- `ErmaNote`.

## Scripts

Los scripts existen para no tener que levantar backend y frontend a mano.

### Windows

```text
scripts/dev.cmd
scripts/dev.ps1
scripts/stop.cmd
scripts/stop.ps1
```

Uso normal:

```powershell
.\scripts\dev.cmd
```

Reiniciar limpio:

```powershell
.\scripts\dev.cmd -StopExisting
```

Apagar:

```powershell
.\scripts\stop.cmd
```

### Raspberry/Linux

```text
scripts/dev.sh
scripts/stop.sh
```

Primera ejecucion:

```bash
chmod +x scripts/dev.sh scripts/stop.sh
./scripts/dev.sh --install
```

Uso normal:

```bash
./scripts/dev.sh
```

Reiniciar limpio:

```bash
./scripts/dev.sh --stop-existing
```

Apagar:

```bash
./scripts/stop.sh
```

## Tests

Los tests del backend viven en:

```text
erma/backend/tests
```

Se ejecutan con:

```powershell
cd erma/backend
.\.venv\Scripts\python.exe -m pytest
```

En Linux/Raspberry:

```bash
cd erma/backend
.venv/bin/python -m pytest
```

Los tests actuales validan:

- `GET /state`;
- comando `sleep`;
- comando desconocido;
- agregar nota;
- comando de fecha/hora.

## Donde tocar segun lo que quieras cambiar

Agregar palabras clave:

```text
erma/backend/data/commands.json
```

Cambiar frases:

```text
erma/backend/data/phrases.json
```

Cambiar respuestas de dormir/despertar:

```text
erma/backend/modules/sleep/handler.py
```

Cambiar como se guardan notas:

```text
erma/backend/core/notes.py
erma/backend/modules/notes/handler.py
```

Cambiar como se detectan comandos:

```text
erma/backend/core/intent_matcher.py
```

Cambiar el flujo general de comandos:

```text
erma/backend/core/command_router.py
```

Cambiar la pantalla:

```text
erma/frontend/src/screens/Home.tsx
erma/frontend/src/components
```

Cambiar conexion frontend/backend:

```text
erma/frontend/src/services/api.ts
```

Agregar una habilidad nueva:

1. Crear carpeta en `erma/backend/modules`.
2. Crear `handler.py`.
3. Crear `commands.py` si queres documentar constantes.
4. Agregar intent y keywords en `data/commands.json`.
5. Registrar el handler en `app/bootstrap.py`.
6. Si hace falta, agregar botones o vistas en el frontend.
7. Agregar tests.

## Como debuggear

Si un comando no responde como esperabas, revisa en este orden:

1. El frontend manda el texto correcto?
2. `commands.json` tiene una palabra clave que coincida?
3. `IntentMatcher` esta encontrando el intent correcto?
4. El intent esta registrado en `bootstrap.py`?
5. El handler devuelve una `ErmaResponse` valida?
6. El estado se actualiza en `state.json`?
7. El historial se actualiza en `history.json`?
8. El frontend refresca historial/notas despues del comando?

Si ERMA no levanta:

1. Revisa si los puertos `8000` o `5173` estan ocupados.
2. Usa `dev.cmd -StopExisting` en Windows.
3. Usa `dev.sh --stop-existing` en Raspberry/Linux.
4. Mira los logs en `.logs/`.

## Que todavia no existe

Esta version todavia no incluye:

- voz;
- wake word real;
- parlante;
- clima real;
- alarmas;
- SQLite;
- WebSockets;
- IA conversacional;
- autenticacion;
- panel de configuracion.

Eso es intencional. El objetivo actual es tener una base simple, entendible y
modular. Cuando esta base sea comoda, se puede crecer hacia voz, eventos en
tiempo real, base de datos e IA sin reescribir todo desde cero.
