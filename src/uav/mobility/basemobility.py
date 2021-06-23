from abc import ABC, abstractmethod

class Basemobility(ABC):
    
    def __init__(self):
        pass

    def get_x(self):
        return self._posX

    def set_x(self, posX):
        self._posX = posX

    def get_y(self):
        return self._posY

    def set_x(self, posY):
        self._posY = posY
    
    def makeMove():
        pass
