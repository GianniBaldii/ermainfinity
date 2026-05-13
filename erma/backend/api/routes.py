from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.bootstrap import create_registry, create_state_store
from core.command_router import CommandRouter
from core.intent_matcher import IntentMatcher
from core.response import ErmaResponse


router = APIRouter()

state_store = create_state_store()
intent_matcher = IntentMatcher()
registry = create_registry(state_store)
command_router = CommandRouter(intent_matcher, registry)


class CommandRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=300)


@router.get("/state")
def get_state():
    return state_store.get_state()


@router.post("/command", response_model=ErmaResponse)
def send_command(command: CommandRequest):
    try:
        return command_router.handle(command.text)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/wake", response_model=ErmaResponse)
def wake():
    return registry.get("wake").handle("wake", ["despertar"])


@router.post("/sleep", response_model=ErmaResponse)
def sleep():
    return registry.get("sleep").handle("sleep", ["dormir"])
