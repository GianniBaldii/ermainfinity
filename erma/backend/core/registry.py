from typing import Protocol

from core.response import ErmaResponse


class CommandHandler(Protocol):
    def handle(self, intent: str, matched_keywords: list[str]) -> ErmaResponse:
        pass


class CommandRegistry:
    def __init__(self):
        self._handlers: dict[str, CommandHandler] = {}

    def register(self, intent: str, handler: CommandHandler) -> None:
        self._handlers[intent] = handler

    def get(self, intent: str) -> CommandHandler:
        if intent not in self._handlers:
            raise ValueError(f"No hay un modulo registrado para el intent: {intent}")
        return self._handlers[intent]
