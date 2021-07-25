import importlib
import sys
import os

dependency_id = "map"

state_registry = {}
__all__ = [state_registry]


def register_state(name):
    """add resolver class to registry"""
    def add_class(clazz):
        # used by state machine as an id        
        clazz.name =  getattr(clazz, "name", name)

        module = sys.modules[clazz.__module__]
        if hasattr(module, '__all__'):
            module.__all__.append(clazz.__name__)
        else:
            module.__all__ = [clazz.__name__]

        state_registry[name] = clazz
        return clazz

    return add_class


def load_modules():
    # load all modules in package
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename == '__init__.py' or filename[-3:] != '.py':
            continue

        # import module
        module = importlib.import_module(f".{filename[:-3]}", package=__name__)
        names = getattr(module, '__all__', [n for n in dir(module)
                                            if not n.startswith('_')])

        # copy to current namespace
        for name in names:
            # supports 'from <package> import symbol' (for convenience)
            globals()[name] = getattr(module, name)

            # propagation of exported symbols to the top level of the package
            # supports 'from <package> import *' (for convenience)
            __all__.append(name)


load_modules()
