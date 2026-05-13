import json
from datetime import datetime
from typing import TypedDict

from app.config import HISTORY_FILE
from core.response import ErmaResponse


class HistoryEntry(TypedDict):
    timestamp: str
    command: str
    intent: str
    status: str
    emotion: str
    message: str
    matched_keywords: list[str]


class ErmaHistoryStore:
    def __init__(self):
        self.history_file = HISTORY_FILE
        self._ensure_history_file()

    def get_history(self, limit: int = 20) -> list[HistoryEntry]:
        entries = self._read_entries()
        return entries[-limit:]

    def add_entry(self, command: str, response: ErmaResponse) -> HistoryEntry:
        entries = self._read_entries()
        entry: HistoryEntry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "command": command,
            "intent": response.intent,
            "status": response.status,
            "emotion": response.emotion,
            "message": response.message,
            "matched_keywords": response.matched_keywords,
        }
        entries.append(entry)
        self._write_entries(entries[-100:])
        return entry

    def _read_entries(self) -> list[HistoryEntry]:
        with open(self.history_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_entries(self, entries: list[HistoryEntry]) -> None:
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(entries, file, ensure_ascii=False, indent=2)

    def _ensure_history_file(self) -> None:
        if self.history_file.exists():
            return

        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self._write_entries([])
