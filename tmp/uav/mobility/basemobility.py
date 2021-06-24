import geopandas

from abc import ABC, abstractmethod
from shapely.geometry import Point

from .movement import Movement
from ....utils.resultcollection import Resultcollection

class Basemobility(ABC):
    _stepLength = -1 
    _currentPos = Point(0, 0, 0)
    
    def __init__(self, stepLength):
        self._move = Movement
        self._stepLength = stepLength
        self._resultcollection =  Resultcollection
        pass

    def getMove(self):
        return self._move

    def getCurrentPos(self):
        return self._currentPos

    @abstractmethod
    def makeMove(self):
        pass
    def doLog():
        pass
