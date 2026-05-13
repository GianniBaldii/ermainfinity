import json
from typing import TypedDict

from app.config import STATE_FILE


ALLOWED_STATUSES = {"idle", "listening", "thinking", "talking", "sleep", "greeting"}
ALLOWED_EMOTIONS = {"neutral", "alegre", "cansado", "curioso"}


class ErmaState(TypedDict):
    status: str
    emotion: str
    message: str


DEFAULT_STATE: ErmaState = {
    "status": "idle",
    "emotion": "neutral",
    "message": "ERMA esta activa",
}


class ErmaStateStore:
    def __init__(self):
        self.state_file = STATE_FILE
        self._ensure_state_file()

    def get_state(self) -> ErmaState:
        with open(self.state_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def update_state(self, status: str, emotion: str, message: str) -> ErmaState:
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Estado no permitido: {status}")

        if emotion not in ALLOWED_EMOTIONS:
            raise ValueError(f"Emocion no permitida: {emotion}")

        new_state: ErmaState = {
            "status": status,
            "emotion": emotion,
            "message": message,
        }

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(new_state, file, ensure_ascii=False, indent=2)

        return new_state

    def _ensure_state_file(self) -> None:
        if self.state_file.exists():
            return

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_STATE, file, ensure_ascii=False, indent=2)
