import geopandas
import numpy as np

from abc import ABC, abstractmethod
from shapely.geometry import Point

from .movement import Movement
from .resultcollection import Resultcollection
from .simulationparameter import Simulationparameter

class Basemobility(ABC):
    
    def __init__(self, uid,  startPos, endPos):
        self._uid = uid
        self._move = Movement()
        self._resultcollection =  Resultcollection()
        self._startPos = startPos
        self._endPos = endPos 
        pass

    def getMove(self):
        return self._move

    def getCurrentPos(self):
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime() 
        currentDirection = self.getMove().getCurrentDirection()
        #x = self.getMove().getStartPos().x + (currentDirection.x * self.getMove().getSpeed() * passedTime)
        #y = self.getMove().getStartPos().y + (currentDirection.y * self.getMove().getSpeed() * passedTime)
        #z = self.getMove().getStartPos().z + (currentDirection.z * self.getMove().getSpeed() * passedTime)
        #print("Speed: " + str(self.getMove().getSpeed()))
        #print("CurrentDirection.x: " + str(currentDirection.x))
        #print("CurrentDirection.y: " + str(currentDirection.y))
        #print("CurrentDirection.z: " + str(currentDirection.z))
        #print("Passed Time: " + str(passedTime))
        #currentPos = Point(x, y, z)
        return -1#currentPos

    def makeMove(self):
        self.doLog()

    def doLog(self):
        print("do log")
        self._resultcollection.logCurrentPosition(self._uid,self.getCurrentPos())
        pass
