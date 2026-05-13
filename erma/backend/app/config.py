from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

STATE_FILE = DATA_DIR / "state.json"
COMMANDS_FILE = DATA_DIR / "commands.json"
PHRASES_FILE = DATA_DIR / "phrases.json"
HISTORY_FILE = DATA_DIR / "history.json"
NOTES_FILE = DATA_DIR / "notes.json"

ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
