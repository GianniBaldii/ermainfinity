from datetime import datetime

from core.response import ErmaResponse
from core.state import ErmaStateStore


DAY_NAMES = [
    "lunes",
    "martes",
    "miercoles",
    "jueves",
    "viernes",
    "sabado",
    "domingo",
]


class DateTimeHandler:
    def __init__(self, state_store: ErmaStateStore):
        self.state_store = state_store

    def handle(
        self,
        intent: str,
        matched_keywords: list[str],
        text: str = "",
    ) -> ErmaResponse:
        now = datetime.now()
        day_name = DAY_NAMES[now.weekday()]
        message = (
            f"Hoy es {day_name} {now.day:02d}/{now.month:02d}/{now.year} "
            f"y son las {now.hour:02d}:{now.minute:02d}."
        )
        state = self.state_store.update_state(
            status="talking",
            emotion="neutral",
            message=message,
        )
        return ErmaResponse(intent=intent, matched_keywords=matched_keywords, **state)
