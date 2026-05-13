from pydantic import BaseModel


class ErmaResponse(BaseModel):
    intent: str
    status: str
    emotion: str
    message: str
    matched_keywords: list[str]
