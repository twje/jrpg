from collections import ChainMap
from .state_machine import StateMachine
from .state_machine import NullState
from .character import state_registry as str1
from .character import dependency_id as str1_dep
from .menu import state_registry as str2
from .menu import dependency_id as str2_dep
from .combat import state_registry as str3
from .combat import dependency_id as str3_dep

state_registry = dict(ChainMap(
    str1,
    str2,
    str3,    
))

state_dependencies = dict(ChainMap(    
    {key: str1_dep for key in str1},
    {key: str2_dep for key in str2},
    {key: str3_dep for key in str3},    
))

__all__ = [
    StateMachine,
    NullState,
    state_registry
]
