from collections import ChainMap
from itertools import chain
from .state_machine import StateMachine
from .state_machine import NullState
from .character import state_registry as str1
from .character import dependency_id as str1_dep
from .menu import state_registry as str2
from .menu import dependency_id as str2_dep
from .combat.event import state_registry as str3
# from .combat.event import dependency_id as str3_dep
from .combat.state import state_registry as str4
from .combat.state import dependency_id as str4_dep

state_registry = dict(ChainMap(
    str1,
    str2,
    str3,
    str4
))

state_dependencies = dict(ChainMap(    
    {key: str1_dep for key in str1},
    {key: str2_dep for key in str2},
    # {key: str3_dep for key in str3},
    {key: str4_dep for key in str4},
))

__all__ = [
    StateMachine,
    NullState,
    state_registry
]
