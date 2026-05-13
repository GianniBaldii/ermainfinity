from core.response import ErmaResponse
from core.state import ErmaStateStore


class SystemHandler:
    def __init__(self, state_store: ErmaStateStore):
        self.state_store = state_store

    def handle(
        self,
        intent: str,
        matched_keywords: list[str],
        text: str = "",
    ) -> ErmaResponse:
        if intent == "greeting":
            state = self.state_store.update_state(
                status="greeting",
                emotion="alegre",
                message="Hola Gianni, estoy aca.",
            )
            return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)

        state = self.state_store.get_state()
        message = (
            f"Estoy en estado {state['status']} con emocion {state['emotion']}. "
            f"{state['message']}"
        )
        return ErmaResponse(
            intent=intent,
            status=state["status"],
            emotion=state["emotion"],
            message=message,
            matched_keywords=matched_keywords,
        )
