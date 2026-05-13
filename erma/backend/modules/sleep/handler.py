from core.response import ErmaResponse
from core.state import ErmaStateStore


class SleepHandler:
    def __init__(self, state_store: ErmaStateStore):
        self.state_store = state_store

    def handle(
        self,
        intent: str,
        matched_keywords: list[str],
        text: str = "",
    ) -> ErmaResponse:
        if intent == "sleep":
            state = self.state_store.update_state(
                status="sleep",
                emotion="cansado",
                message="Bueno Gianni, voy a descansar un rato.",
            )
            return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

        state = self.state_store.update_state(
            status="idle",
            emotion="neutral",
            message="Ya estoy despierta y lista.",
        )
        return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)
