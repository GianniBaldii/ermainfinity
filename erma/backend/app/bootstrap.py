from core.registry import CommandRegistry
from core.history import ErmaHistoryStore
from core.notes import ErmaNotesStore
from core.state import ErmaStateStore
from modules.datetime.handler import DateTimeHandler
from modules.notes.handler import NotesHandler
from modules.phrases.handler import PhrasesHandler
from modules.sleep.handler import SleepHandler
from modules.system.handler import SystemHandler


def create_state_store() -> ErmaStateStore:
    return ErmaStateStore()


def create_history_store() -> ErmaHistoryStore:
    return ErmaHistoryStore()


def create_notes_store() -> ErmaNotesStore:
    return ErmaNotesStore()


def create_registry(
    state_store: ErmaStateStore,
    notes_store: ErmaNotesStore | None = None,
) -> CommandRegistry:
    if notes_store is None:
        notes_store = create_notes_store()
    registry = CommandRegistry()
    registry.register("sleep", SleepHandler(state_store))
    registry.register("wake", SleepHandler(state_store))
    registry.register("greeting", SystemHandler(state_store))
    registry.register("state", SystemHandler(state_store))
    registry.register("phrase", PhrasesHandler(state_store))
    registry.register("note_list", NotesHandler(state_store, notes_store))
    registry.register("note_add", NotesHandler(state_store, notes_store))
    registry.register("datetime", DateTimeHandler(state_store))
    return registry
