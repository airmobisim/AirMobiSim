import math 
import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility

from .simulationparameter import Simulationparameter

class Linearmobility(Basemobility):
    def __init__(self, uid, startPos, endPos, angle,speed=10):
        super().__init__(uid, startPos, endPos)
        self._angle = angle
        self._acceleration = 0 #acceleration not considered yet
        self._move.setStart(startPos, 0)
        self._move.setSpeed(speed)
        self._move.setLastPos(startPos)
        self._uid = uid
        self._stepTarget = ""
    def makeMove(self):
        move = self.getMove()
        """
        print("----------------------------------------------------")
        print("self._uid: "            + str(self._uid))
        print("move.getSpeed(): "      + str(move.getSpeed()))
        print("move.getStartPos().x: " + str(move.getStartPos().x))
        print("move.getStartPos().y: " + str(move.getStartPos().y))
        print("move.getStartPos().z: " + str(move.getStartPos().z))
        print("angle: " + str(self._angle))
        print("move.getLastPos().x: "  + str(move.getLastPos().x)) 
        print("move.getLastPos().y: "  + str(move.getLastPos().y))         
        """
        # This part is redundant code with the one in setDirectionbyTarget
        # Also this one is not working - is not used further

        #stepTargetX = move.getLastPos().x + move.getSpeed() * math.cos(math.pi*(self._angle/180)) * Simulationparameter.stepLength
        #stepTargetY = move.getLastPos().y + move.getSpeed() * math.sin(math.pi*(self._angle/180)) * Simulationparameter.stepLength
        
        
        # This calculation of stepTarget is ONLY  allowed when the movement is linear
        stepTarget = Point(self._endPos.x, self._endPos.y, self._startPos.z)

        #stepTarget = Point(stepTargetX, stepTargetY, self._startPos.z)
        self._stepTarget = stepTarget
        move.setDirectionByTarget(stepTarget)

        newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength 
        move.setSpeed(newSpeed)
        super().makeMove()
        pass
