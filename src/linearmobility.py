import math 
import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility

from .simulationparameter import Simulationparameter

class Linearmobility(Basemobility):
    def __init__(self, uid, angle, startPos, endPos):
        super().__init__(uid, startPos, endPos)
        self._angle = angle
        self._acceleration = 0
        self._move.setStart(startPos, 0)
        self._move.setEndPos(endPos)
        self._move.setTempStartPos(startPos)

        self._move.setSpeed(50)
        self._uid = uid
        self._stepTarget = ""
        self._totalFlightTime= self.computeTotalFlightTime()

    def makeMove(self):
        move = self.getMove()
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        move.setDirectionByTarget()
        newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength

        if passedTime>= self._totalFlightTime:
            newSpeed=0.0
            self._acceleration=0.0
            self.getMove().setFinalFlag(True)
         
        move.setSpeed(newSpeed)
        move.setPassedTime(passedTime)
        super().makeMove()


    def computeTotalFlightTime(self):
        distance = math.sqrt((self._endPos.x - self._startPos.x) ** 2 + (self._endPos.y - self._startPos.y) ** 2 + (
                    self._endPos.z - self._startPos.z) ** 2)
        final_velocity = math.sqrt(self.getMove().getSpeed()**2 + 2*self._acceleration*distance) # v^2=u^2+2as
        average_velocity= (self.getMove().getSpeed()+final_velocity)/2
        return distance/average_velocity

