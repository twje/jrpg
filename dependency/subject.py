from .weak_list import WeakList


class Subject:
    injectors = WeakList()

    @classmethod
    def get_dependency(cls, identifier):
        for injector in cls.injectors:
            dependency = injector.get_dependency(identifier)
            if dependency is not None:
                return dependency

    @classmethod
    def register_as_dependency_injector(cls, injector):
        cls.injectors.append(injector)
