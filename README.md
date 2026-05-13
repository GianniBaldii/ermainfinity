# INFINITY ERMA

ERMA es una base inicial para un asistente personal fisico pensado para ejecutarse en una Raspberry Pi 5 con pantalla tactil, microfono y parlante. Esta primera version se enfoca en texto, estado interno, comandos simples, notas, historial y una interfaz web minima.

## Alcance actual

- Backend con Python + FastAPI.
- Frontend con React + Vite + TypeScript + TailwindCSS.
- Persistencia inicial en archivos JSON.
- Comunicacion por HTTP REST.
- Interpretacion de comandos por palabras clave.
- Modulos simples para sistema, descanso, frases, notas y fecha/hora.
- Historial basico de comandos.

No incluye voz, wake word, clima real, alarmas, SQLite ni WebSockets.

## Estructura

```text
erma/
|-- backend/
|   |-- app/
|   |-- api/
|   |-- core/
|   |-- modules/
|   |-- data/
|   |-- tests/
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   `-- package.json
`-- docs/
```

## Backend en Windows

Desde la raiz del repo:

```powershell
.\scripts\dev.cmd
```

Tambien se puede ejecutar el script de PowerShell directamente:

```powershell
.\scripts\dev.ps1
```

Eso levanta backend y frontend juntos. Si es la primera vez, o queres reinstalar dependencias:

```powershell
.\scripts\dev.cmd -Install
```

Si queres que el backend se reinicie automaticamente al editar archivos:

```powershell
.\scripts\dev.cmd -Reload
```

Si quedo un backend o frontend viejo ocupando puertos:

```powershell
.\scripts\dev.cmd -StopExisting
```

Para apagar ERMA manualmente:

```powershell
.\scripts\stop.cmd
```

Frontend:

```text
http://127.0.0.1:5173
```

Backend:

```text
http://127.0.0.1:8000
```

Para apagar ERMA, presiona `Ctrl+C` en esa terminal.

## Backend manual en Windows

Desde la raiz del repo:

```powershell
cd erma\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API disponible en:

```text
http://127.0.0.1:8000
```

## Frontend en Windows

En otra terminal:

```powershell
cd erma\frontend
npm install
npm run dev
```

Abrir:

```text
http://127.0.0.1:5173
```

## Ejecutar luego en Raspberry Pi

En la Raspberry, despues de clonar o actualizar el repo:

```bash
cd ermainfinity
git pull
chmod +x scripts/dev.sh scripts/stop.sh
./scripts/dev.sh --install
```

Eso levanta backend y frontend juntos. Si ya instalaste dependencias antes:

```bash
./scripts/dev.sh
```

Si quedaron puertos ocupados:

```bash
./scripts/dev.sh --stop-existing
```

Para apagar ERMA:

```bash
./scripts/stop.sh
```

Desde la Raspberry:

```text
http://127.0.0.1:5173
```

Desde otra maquina de la misma red:

```text
http://IP_DE_LA_RASPBERRY:5173
```

## Endpoints

### GET /state

Devuelve el estado actual:

```json
{
  "status": "idle",
  "emotion": "neutral",
  "message": "ERMA esta activa"
}
```

### GET /history

Devuelve los ultimos comandos procesados.

### GET /notes

Devuelve las notas guardadas.

### POST /command

Ejemplo:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/command -ContentType "application/json" -Body '{"text":"ERMA dormite un rato"}'
```

Respuesta esperada:

```json
{
  "intent": "sleep",
  "status": "sleep",
  "emotion": "cansado",
  "message": "Bueno Gianni, voy a descansar un rato.",
  "matched_keywords": ["dormite"]
}
```

### POST /wake

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/wake
```

### POST /sleep

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/sleep
```

## Comandos de prueba

Probar desde el frontend o con `POST /command`:

- `ERMA dormite un rato`
- `despertar`
- `hola ERMA`
- `motivame`
- `como estas`
- `que hora es`
- `recordame comprar pilas`
- `ver notas`

## Tests

Desde `erma/backend`:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Commit recomendado

```text
feat: ampliar mvp textual de erma
```
