from core.intent_matcher import IntentMatcher
from core.registry import CommandRegistry
from core.response import ErmaResponse


class CommandRouter:
    def __init__(self, matcher: IntentMatcher, registry: CommandRegistry):
        self.matcher = matcher
        self.registry = registry

    def handle(self, text: str) -> ErmaResponse:
        match = self.matcher.match(text)

        if match is None:
            return ErmaResponse(
                intent="unknown",
                status="idle",
                emotion="curioso",
                message="No entendi ese comando todavia.",
                matched_keywords=[],
            )

        handler = self.registry.get(match.intent)
        return handler.handle(match.intent, match.matched_keywords)
