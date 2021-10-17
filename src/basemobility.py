import geopandas
import numpy as np

from abc import ABC, abstractmethod
from shapely.geometry import Point

from .movement import Movement
from .resultcollection import Resultcollection
from .simulationparameter import Simulationparameter

from .baseenergy import Baseenergy 

class Basemobility(ABC):
    
    def __init__(self, uid,  startPos, endPos):
        self._uid = uid
        self._move = Movement()
        self._resultcollection =  Resultcollection()
        self._baseenergy = Baseenergy()
        self._startPos = startPos
        self._endPos = endPos 
        pass

    def getMove(self):
        return self._move

    def getCurrentPos(self):
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        if self.getMove().getLinearMobilitySpFlag():

            currentPos = self.getMove().getNextCoordinate()

            if (self.getMove().getFinalFlag()):
                currentPos = self.getMove().getNextCoordinate()

            return currentPos




        elif self.getMove().getFinalFlag():
            # currentPos=Point(self.getMove().getTempStartPos().x, self.getMove().getTempStartPos().y, 0.0)
            # currentPos=Point(self.getMove().getNextCoordinate().x, self.getMove().getNextCoordinate().x, 0.0)
            currentPos = self.getMove().getNextCoordinate()

        return currentPos


    def makeMove(self):
        self.doLog()

    def doLog(self):
        #print("do log")
        self._resultcollection.logCurrentPosition(self._uid, self.getCurrentPos(), self.getMove())
        currentEnergy = self._baseenergy.getcurrentEnergy(self.getMove().getSpeed(), (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime())

        self._resultcollection.logCurrentEnergy(self._uid,currentEnergy[0], currentEnergy[1])

        pass
