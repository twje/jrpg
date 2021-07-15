from itertools import chain
from .state_machine import StateMachine
from .state_machine import NullState
from .character import state_registry as str1
from .menu import state_registry as str2
from .combat.event import state_registry as str3
from .combat.state import state_registry as str4

state_registry = dict(chain(
    str1.items(),
    str2.items(),
    str3.items(),
    str4.items()
))

__all__ = [
    StateMachine,
    NullState,
    state_registry
]
