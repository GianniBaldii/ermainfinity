from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.bootstrap import (
    create_history_store,
    create_notes_store,
    create_registry,
    create_state_store,
)
from core.command_router import CommandRouter
from core.intent_matcher import IntentMatcher
from core.response import ErmaResponse


router = APIRouter()

state_store = create_state_store()
history_store = create_history_store()
notes_store = create_notes_store()
intent_matcher = IntentMatcher()
registry = create_registry(state_store, notes_store)
command_router = CommandRouter(intent_matcher, registry, history_store)


class CommandRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=300)


@router.get("/state")
def get_state():
    return state_store.get_state()


@router.get("/history")
def get_history(limit: int = 20):
    return history_store.get_history(limit=limit)


@router.get("/notes")
def get_notes():
    return notes_store.list_notes()


@router.post("/command", response_model=ErmaResponse)
def send_command(command: CommandRequest):
    try:
        return command_router.handle(command.text)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/wake", response_model=ErmaResponse)
def wake():
    response = registry.get("wake").handle("wake", ["despertar"], "despertar")
    history_store.add_entry("despertar", response)
    return response


@router.post("/sleep", response_model=ErmaResponse)
def sleep():
    response = registry.get("sleep").handle("sleep", ["dormir"], "dormir")
    history_store.add_entry("dormir", response)
    return response
