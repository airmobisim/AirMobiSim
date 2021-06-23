from abc import ABC, abstractmethod
from .movement import Movement
class Basemobility(ABC):
    
    def __init__(self):
        self.move = Movement
        pass

    def get_x(self):
        return self._posX

    def set_x(self, posX):
        self._posX = posX

    def get_y(self):
        return self._posY

    def set_x(self, posY):
        self._posY = posY

    @abstractmethod
    def makeMove():
        pass
