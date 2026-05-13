from core.notes import ErmaNotesStore
from core.response import ErmaResponse
from core.state import ErmaStateStore


class NotesHandler:
    def __init__(self, state_store: ErmaStateStore, notes_store: ErmaNotesStore):
        self.state_store = state_store
        self.notes_store = notes_store

    def handle(
        self,
        intent: str,
        matched_keywords: list[str],
        text: str = "",
    ) -> ErmaResponse:
        if intent == "note_list":
            return self._list_notes(intent, matched_keywords)

        return self._add_note(intent, matched_keywords, text)

    def _list_notes(self, intent: str, matched_keywords: list[str]) -> ErmaResponse:
        notes = self.notes_store.list_notes()

        if not notes:
            message = "No tengo notas guardadas todavia."
        else:
            preview = "; ".join(f"{note['id']}. {note['text']}" for note in notes[-5:])
            message = f"Tengo estas notas: {preview}"

        state = self.state_store.update_state(
            status="talking",
            emotion="neutral",
            message=message,
        )
        return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

    def _add_note(
        self,
        intent: str,
        matched_keywords: list[str],
        text: str,
    ) -> ErmaResponse:
        note_text = self._extract_note_text(text, matched_keywords)

        if not note_text:
            state = self.state_store.update_state(
                status="talking",
                emotion="curioso",
                message="Decime que queres que anote.",
            )
            return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

        note = self.notes_store.add_note(note_text)
        state = self.state_store.update_state(
            status="talking",
            emotion="alegre",
            message=f"Listo, guarde la nota {note['id']}: {note['text']}",
        )
        return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

    def _extract_note_text(self, text: str, matched_keywords: list[str]) -> str:
        clean_text = text.strip()
        lower_text = clean_text.lower()

        for keyword in sorted(matched_keywords, key=len, reverse=True):
            lower_keyword = keyword.lower()
            if lower_text.startswith(lower_keyword):
                return clean_text[len(keyword):].strip(" :,-")

            keyword_index = lower_text.find(lower_keyword)
            if keyword_index >= 0:
                start_index = keyword_index + len(keyword)
                return clean_text[start_index:].strip(" :,-")

        return clean_text
