import json
import unicodedata
from dataclasses import dataclass

from app.config import COMMANDS_FILE


@dataclass
class IntentMatch:
    intent: str
    matched_keywords: list[str]


class IntentMatcher:
    def __init__(self):
        self.commands = self._load_commands()

    def match(self, text: str) -> IntentMatch | None:
        clean_text = self._normalize(text)

        for intent, keywords in self.commands.items():
            matched = [
                keyword
                for keyword in keywords
                if self._normalize(keyword) in clean_text
            ]

            if matched:
                return IntentMatch(intent=intent, matched_keywords=matched)

        return None

    def _load_commands(self) -> dict[str, list[str]]:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _normalize(self, value: str) -> str:
        value = value.lower().strip()
        value = unicodedata.normalize("NFD", value)
        value = "".join(char for char in value if unicodedata.category(char) != "Mn")
        return value
