from abc import ABC
from abc import abstractmethod


class IRenderable(ABC):
    @abstractmethod
    def draw(self, surface, offset_x, offset_y):
        pass
