# INFINITY ERMA

ERMA es una base inicial para un asistente personal fisico pensado para ejecutarse en una Raspberry Pi 5 con pantalla tactil, microfono y parlante. Esta primera version se enfoca en texto, estado interno, comandos simples y una interfaz web minima.

## Alcance actual

- Backend con Python + FastAPI.
- Frontend con React + Vite + TypeScript + TailwindCSS.
- Persistencia inicial en archivos JSON.
- Comunicacion por HTTP REST.
- Interpretacion de comandos por palabras clave.
- Modulos simples para sistema, descanso y frases.

No incluye voz, wake word, clima real, alarmas, SQLite ni WebSockets.

## Estructura

```text
erma/
├── backend/
│   ├── app/
│   ├── api/
│   ├── core/
│   ├── modules/
│   ├── data/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── docs/
```

## Backend en Windows

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
cd erma/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Para el frontend:

```bash
cd erma/frontend
npm install
npm run dev -- --host 0.0.0.0
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

## Commit recomendado

```text
feat: crear base inicial de infinity erma
```
