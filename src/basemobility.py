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
        x = self.getMove().getStartPos().x + (currentDirection[0] * self.getMove().getSpeed() * passedTime)
        y = self.getMove().getStartPos().y + (currentDirection[1] * self.getMove().getSpeed() * passedTime)
        z = self.getMove().getStartPos().z + (currentDirection[2] * self.getMove().getSpeed() * passedTime)
        '''
        print("Speed: " + str(self.getMove().getSpeed()))
        print("CurrentDirection.x: " + str(currentDirection[0]))
        print("CurrentDirection.y: " + str(currentDirection[1]))
        print("CurrentDirection.z: " + str(currentDirection[2]))
        print("Passed Time: " + str(passedTime))
        '''
        currentPos = Point(x, y, z)
        return currentPos

    def makeMove(self):
        self.doLog()

    def doLog(self):
        #print("do log")
        self._resultcollection.logCurrentPosition(self._uid,self.getCurrentPos())
        pass
