# Guia teorica de INFINITY ERMA

Esta guia explica como funciona el proyecto desde cero. La idea no es memorizar
todos los archivos, sino entender el mapa general: que parte recibe comandos,
que parte decide que significan, que parte cambia el estado y que parte lo muestra
en pantalla.

## La idea del proyecto

INFINITY ERMA esta pensada como una base para un asistente personal local. En esta
primera version no hay voz, inteligencia artificial conversacional ni sensores.
Por ahora ERMA funciona asi:

1. Una interfaz web muestra el estado de ERMA.
2. El usuario escribe un comando o toca un boton.
3. El frontend manda ese comando al backend.
4. El backend interpreta el texto usando palabras clave.
5. El backend actualiza el estado guardado en JSON.
6. El frontend recibe una respuesta y actualiza la pantalla.

La separacion mas importante es esta:

- `backend`: cerebro simple de ERMA.
- `frontend`: cara/pantalla de ERMA.
- `data`: memoria inicial guardada en archivos JSON.
- `docs`: explicaciones y plan del proyecto.

## Backend: el cerebro

El backend vive en:

```text
erma/backend
```

Usa FastAPI, que sirve para crear una API HTTP. Una API HTTP es una forma de que
otros programas hablen con el backend usando URLs como `/state`, `/command`,
`/wake` o `/sleep`.

### Que es un endpoint

Un endpoint es una puerta de entrada al backend. Por ejemplo:

```text
GET /state
```

significa: "dame el estado actual".

```text
POST /command
```

significa: "te mando un comando escrito para que lo proceses".

Los endpoints estan definidos en:

```text
erma/backend/api/routes.py
```

## Archivo principal del backend

El archivo:

```text
erma/backend/app/main.py
```

crea la aplicacion FastAPI.

Tambien configura CORS. CORS es el permiso para que el frontend, que corre en
`http://127.0.0.1:5173`, pueda hablar con el backend, que corre en
`http://127.0.0.1:8000`.

Sin CORS, el navegador podria bloquear la comunicacion entre frontend y backend.

## Estado de ERMA

El estado actual se guarda en:

```text
erma/backend/data/state.json
```

Ese archivo contiene algo parecido a esto:

```json
{
  "status": "idle",
  "emotion": "neutral",
  "message": "ERMA esta activa"
}
```

El codigo que lee y escribe ese estado esta en:

```text
erma/backend/core/state.py
```

Conceptualmente, ese archivo es la memoria simple de ERMA. Todavia no usa base de
datos; usa JSON para que sea facil de entender y modificar.

## Intents: que quiso decir el usuario

Un `intent` es la intencion detectada en un comando.

Ejemplos:

- Si escribis `ERMA dormite un rato`, el intent esperado es `sleep`.
- Si escribis `hola ERMA`, el intent esperado es `greeting`.
- Si escribis `motivame`, el intent esperado es `phrase`.
- Si escribis `como estas`, el intent esperado es `state`.

Los intents y sus palabras clave estan en:

```text
erma/backend/data/commands.json
```

Ejemplo simplificado:

```json
{
  "sleep": ["dormir", "dormite", "descansar"],
  "wake": ["despertar", "levantate", "activar"],
  "greeting": ["saludar", "hola", "buenas"]
}
```

El codigo que busca esas palabras clave esta en:

```text
erma/backend/core/intent_matcher.py
```

Ese archivo normaliza el texto. Por ejemplo, convierte a minusculas y quita
acentos para comparar mejor. Asi `como estas` y `como estas` pueden tratarse de
forma parecida aunque el usuario escriba con variantes.

## Router de comandos

El archivo:

```text
erma/backend/core/command_router.py
```

recibe el texto, pregunta que intent se encontro y despues manda el trabajo al
modulo correcto.

Pensalo como una recepcion:

1. Llega un texto.
2. Se detecta el intent.
3. Se busca quien sabe manejar ese intent.
4. Se ejecuta ese handler.
5. Se devuelve una respuesta.

Si no se encuentra ningun intent, ERMA responde con `unknown`.

## Registry: la lista de modulos disponibles

El archivo:

```text
erma/backend/core/registry.py
```

guarda una relacion entre intents y handlers.

Por ejemplo:

```text
sleep -> SleepHandler
wake -> SleepHandler
greeting -> SystemHandler
state -> SystemHandler
phrase -> PhrasesHandler
```

Esa relacion se arma en:

```text
erma/backend/app/bootstrap.py
```

El `bootstrap` es el lugar donde se conectan las piezas principales del backend.

## Handlers: los modulos que hacen cosas

Los handlers viven en:

```text
erma/backend/modules
```

Cada modulo sabe resolver una responsabilidad concreta.

### SleepHandler

Archivo:

```text
erma/backend/modules/sleep/handler.py
```

Maneja:

- `sleep`
- `wake`

Si el intent es `sleep`, cambia el estado a dormida. Si el intent es `wake`,
cambia el estado a despierta.

### SystemHandler

Archivo:

```text
erma/backend/modules/system/handler.py
```

Maneja:

- `greeting`
- `state`

Sirve para saludar o para preguntar como esta ERMA.

### PhrasesHandler

Archivo:

```text
erma/backend/modules/phrases/handler.py
```

Maneja:

- `phrase`

Lee frases desde:

```text
erma/backend/data/phrases.json
```

y devuelve una frase al azar.

## Respuesta estandar

Todas las respuestas importantes del backend usan este formato:

```json
{
  "intent": "sleep",
  "status": "sleep",
  "emotion": "cansado",
  "message": "Bueno Gianni, voy a descansar un rato.",
  "matched_keywords": ["dormite"]
}
```

Ese formato esta definido en:

```text
erma/backend/core/response.py
```

Esto es util porque el frontend siempre sabe que campos esperar.

## Ejemplo completo: "ERMA dormite un rato"

Supongamos que escribis:

```text
ERMA dormite un rato
```

El flujo interno es:

1. El frontend manda el texto a `POST /command`.
2. `api/routes.py` recibe el request.
3. `CommandRouter` llama a `IntentMatcher`.
4. `IntentMatcher` lee `commands.json`.
5. Encuentra la palabra clave `dormite`.
6. Decide que el intent es `sleep`.
7. `CommandRouter` pide al `CommandRegistry` el handler para `sleep`.
8. El registry devuelve `SleepHandler`.
9. `SleepHandler` actualiza `state.json`.
10. El backend devuelve una respuesta estandar.
11. El frontend actualiza avatar, estado, emocion y mensaje.

Ese es el corazon del proyecto.

## Frontend: la cara de ERMA

El frontend vive en:

```text
erma/frontend
```

Usa:

- React: para construir la interfaz.
- TypeScript: JavaScript con tipos.
- Vite: herramienta para correr y compilar el frontend.
- TailwindCSS: clases de estilos para disenar rapido.

El archivo de entrada es:

```text
erma/frontend/src/main.tsx
```

Ese archivo monta la pantalla principal `Home`.

## Pantalla principal

La pantalla principal esta en:

```text
erma/frontend/src/screens/Home.tsx
```

Ese archivo maneja:

- estado visual actual de ERMA;
- texto escrito por el usuario;
- ultima respuesta recibida;
- errores de conexion;
- botones rapidos como dormir, despertar, saludar y frase.

Cuando la pantalla carga, llama a `getState()` para pedirle al backend el estado
actual.

Cuando escribis un comando, llama a `sendCommand(text)`.

## Servicio API del frontend

El archivo:

```text
erma/frontend/src/services/api.ts
```

es el puente entre React y FastAPI.

Ahi estan funciones como:

- `getState()`
- `sendCommand(text)`
- `wakeErma()`
- `sleepErma()`

Todas usan `fetch`, que es la funcion del navegador para hacer pedidos HTTP.

Por ahora la API esta fija en:

```text
http://127.0.0.1:8000
```

Mas adelante conviene mover eso a una variable de entorno.

## Tipos del frontend

Los tipos viven en:

```text
erma/frontend/src/types/erma.ts
```

Ahi se define que formas pueden tener `status`, `emotion`, `ErmaState` y
`ErmaResponse`.

Esto ayuda a que TypeScript avise si el frontend espera un campo que el backend
no devuelve, o si se usa un estado invalido.

## Componentes visuales

Los componentes estan en:

```text
erma/frontend/src/components
```

Actualmente hay:

- `ErmaAvatar.tsx`: muestra la cara/avatar de ERMA segun estado y emocion.
- `StatusPanel.tsx`: muestra estado, emocion y mensaje.

La idea de React es dividir la pantalla en piezas pequenas. Cada componente se
ocupa de una parte visual.

## Donde tocar segun lo que quieras cambiar

Si queres agregar una palabra clave nueva:

```text
erma/backend/data/commands.json
```

Si queres cambiar una respuesta de dormir/despertar:

```text
erma/backend/modules/sleep/handler.py
```

Si queres agregar frases motivacionales:

```text
erma/backend/data/phrases.json
```

Si queres cambiar como se ve la pantalla:

```text
erma/frontend/src/screens/Home.tsx
erma/frontend/src/components
```

Si queres cambiar colores y estilos globales:

```text
erma/frontend/src/index.css
```

Si queres agregar un modulo nuevo:

1. Crear una carpeta en `erma/backend/modules`.
2. Crear su `handler.py`.
3. Agregar palabras clave en `commands.json`.
4. Registrar el nuevo handler en `app/bootstrap.py`.
5. Si hace falta, agregar botones o llamadas en el frontend.

## Como pensar el proyecto sin perderte

Una forma simple de recordarlo:

```text
Frontend = pantalla
Backend = logica
JSON = memoria/configuracion simple
Intent = intencion detectada
Handler = modulo que sabe que hacer
State = estado actual de ERMA
```

Cuando algo no funcione, preguntate:

1. El frontend esta mandando el pedido correcto?
2. El backend tiene un endpoint para recibirlo?
3. El intent existe en `commands.json`?
4. Hay un handler registrado para ese intent?
5. El handler devuelve una respuesta con el formato correcto?
6. El frontend sabe mostrar esa respuesta?

Con esas seis preguntas podes debuggear casi todo el proyecto actual.

## Que todavia no existe

Esta version todavia no incluye:

- voz;
- wake word real;
- parlante;
- clima real;
- alarmas;
- base de datos SQLite;
- WebSockets;
- IA conversacional;
- historial de conversaciones.

Eso no esta mal. Es intencional. Primero se esta construyendo una base simple,
entendible y modificable. Despues se puede hacer crecer sin romper todo.

