import json
import random

from app.config import PHRASES_FILE
from core.response import ErmaResponse
from core.state import ErmaStateStore


class PhrasesHandler:
    def __init__(self, state_store: ErmaStateStore):
        self.state_store = state_store

    def handle(self, intent: str, matched_keywords: list[str]) -> ErmaResponse:
        phrase = self._get_phrase()
        state = self.state_store.update_state(
            status="talking",
            emotion="alegre",
            message=phrase,
        )
        return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

    def _get_phrase(self) -> str:
        with open(PHRASES_FILE, "r", encoding="utf-8") as file:
            phrases = json.load(file)

        if not phrases:
            return "No tengo frases cargadas todavia."

        return random.choice(phrases)
