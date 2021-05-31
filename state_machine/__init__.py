from itertools import chain
from .state_machine import StateMachine
from .state_machine import NullState
from .character import state_registry as str1
from .menu import state_registry as str2

state_registry = dict(chain(
    str1.items(),
    str2.items()
))

__all__ = [
    StateMachine,
    NullState,
    state_registry
]
