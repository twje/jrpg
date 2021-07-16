
from abc import ABC
from abc import abstractmethod

class Injector(ABC):
    @abstractmethod
    def get_dependency(self, identifier):
        pass
