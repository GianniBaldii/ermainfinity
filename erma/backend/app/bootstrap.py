from core.registry import CommandRegistry
from core.state import ErmaStateStore
from modules.phrases.handler import PhrasesHandler
from modules.sleep.handler import SleepHandler
from modules.system.handler import SystemHandler


def create_state_store() -> ErmaStateStore:
    return ErmaStateStore()


def create_registry(state_store: ErmaStateStore) -> CommandRegistry:
    registry = CommandRegistry()
    registry.register("sleep", SleepHandler(state_store))
    registry.register("wake", SleepHandler(state_store))
    registry.register("greeting", SystemHandler(state_store))
    registry.register("state", SystemHandler(state_store))
    registry.register("phrase", PhrasesHandler(state_store))
    return registry
