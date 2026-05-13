import json
from datetime import datetime
from typing import TypedDict

from app.config import NOTES_FILE


class Note(TypedDict):
    id: int
    text: str
    created_at: str


class ErmaNotesStore:
    def __init__(self):
        self.notes_file = NOTES_FILE
        self._ensure_notes_file()

    def list_notes(self) -> list[Note]:
        return self._read_notes()

    def add_note(self, text: str) -> Note:
        notes = self._read_notes()
        next_id = max((note["id"] for note in notes), default=0) + 1
        note: Note = {
            "id": next_id,
            "text": text,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        notes.append(note)
        self._write_notes(notes)
        return note

    def _read_notes(self) -> list[Note]:
        with open(self.notes_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_notes(self, notes: list[Note]) -> None:
        with open(self.notes_file, "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=2)

    def _ensure_notes_file(self) -> None:
        if self.notes_file.exists():
            return

        self.notes_file.parent.mkdir(parents=True, exist_ok=True)
        self._write_notes([])
