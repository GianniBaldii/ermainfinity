from core.intent_matcher import IntentMatcher
from core.registry import CommandRegistry
from core.response import ErmaResponse


class CommandRouter:
    def __init__(
        self,
        matcher: IntentMatcher,
        registry: CommandRegistry,
        history_store=None,
    ):
        self.matcher = matcher
        self.registry = registry
        self.history_store = history_store

    def handle(self, text: str) -> ErmaResponse:
        match = self.matcher.match(text)

        if match is None:
            response = ErmaResponse(
                intent="unknown",
                status="idle",
                emotion="curioso",
                message="No entendi ese comando todavia.",
                matched_keywords=[],
            )
            self._record(text, response)
            return response

        handler = self.registry.get(match.intent)
        response = handler.handle(match.intent, match.matched_keywords, text)
        self._record(text, response)
        return response

    def _record(self, text: str, response: ErmaResponse) -> None:
        if self.history_store is None:
            return

        self.history_store.add_entry(command=text, response=response)
