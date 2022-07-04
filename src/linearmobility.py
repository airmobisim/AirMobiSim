import math

from .basemobility import Basemobility
from .simulationparameter import Simulationparameter

import src.logWrapper as logWrapper

class Linearmobility(Basemobility):

    def __init__(self, uid, startPos, endPos, angle, speed=10, polygon_file_path=None,collision_action=None):
        super().__init__(uid, startPos, endPos, polygon_file_path,collision_action)
        self._angle = angle
        self._acceleration = 0  # acceleration not considered yet
        self._move.setStart(startPos, 0)
        self._move.setEndPos(endPos)
        self._move.setTempStartPos(startPos)
        self._move.setSpeed(speed)
        self._uid = uid

        self._move.setTotalDistance(self.computeTotalDistance())
        self._totalFlightTime = self.computeTotalFlightTime(0.0,speed,self._acceleration)


    def makeMove(self):
        move = self.getMove()
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        move.setDirectionByTarget()
        newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength

        if passedTime >= self._totalFlightTime:
            newSpeed = 0.0
            self._acceleration = 0.0
            self.getMove().setFinalFlag(True)


        move.setSpeed(newSpeed)
        move.setPassedTime(passedTime)
        super().makeMove()

        if passedTime < self._totalFlightTime:
            if self._collisionAction != 2:
                # move.setFutureTime( passedTime + Simulationparameter.stepLength)
                future_time = passedTime + Simulationparameter.stepLength
                self.setFutureCoordinate()

                self.manageObstacles(passedTime, future_time)

        return True if self._obstacleDetector_flag and self._collisionAction == 3 else False  # obstacle->remove/not remove node indicator

    def computeTotalDistance(self):
        return math.sqrt((self._endPos.x - self._startPos.x) ** 2 + (self._endPos.y - self._startPos.y) ** 2 + (
                self._endPos.z - self._startPos.z) ** 2)

    # set future x,y coordinate for building detection
    def setFutureCoordinate(self):
        currentDirection = self.getMove().getCurrentDirection()
        previousPos = self.getMove().getTempStartPos()
        x = previousPos.x + (currentDirection.x * self.getMove().getSpeed() * Simulationparameter.stepLength)
        y = previousPos.y + (currentDirection.y * self.getMove().getSpeed() * Simulationparameter.stepLength)

        futureCoordinate = (x, y)

        self.getMove().setFutureCoordinate(futureCoordinate)




