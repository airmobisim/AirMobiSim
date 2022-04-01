import math 
import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility

from .simulationparameter import Simulationparameter

class Linearmobility(Basemobility):
    def __init__(self, uid, angle, startPos, endPos):
        super().__init__(uid, startPos, endPos)
        self._angle = angle
        self._acceleration = 0 #acceleration not considered yet
        self._move.setStart(startPos, 0)
        self._move.setEndPos(endPos)

        self._move.setSpeed(100)
        self._uid = uid
        self._stepTarget = ""
    def makeMove(self):
        move = self.getMove()
        passedTime = (
                                 Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        '''
        print("----------------------------------------------------")
        print("move.getSpeed(): "      + str(move.getSpeed()))
        print("move.getStartPos().x: " + str(move.getStartPos().x))
        print("move.getStartPos().y: " + str(move.getStartPos().y))
        print("move.getStartPos().z: " + str(move.getStartPos().z))
        print("angle: " + str(self._angle))
        '''
        # stepTargetX = move.getStartPos().x + move.getSpeed() * math.cos(math.pi * (self._angle/180)) * Simulationparameter.stepLength
        # stepTargetY = move.getStartPos().y + move.getSpeed() * math.sin(math.pi * (self._angle/180)) * Simulationparameter.stepLength
        ''' 
        print("stepTargetX: " + str(stepTargetX))
        print("stepTargetY: " + str(stepTargetY))
        '''
        # stepTarget = Point(stepTargetX, stepTargetY, self._startPos.z)
        # self._stepTarget = stepTarget
        # move.setDirectionByTarget(stepTarget)

        move.setDirectionByTarget()

        newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength
         
        move.setSpeed(newSpeed)
        move.setPassedTime(passedTime)
        super().makeMove()

        pass
