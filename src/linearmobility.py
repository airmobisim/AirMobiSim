import math

from .basemobility import Basemobility
from .simulationparameter import Simulationparameter

import logging

class Linearmobility(Basemobility):

    def __init__(self, uid, startPos, endPos, angle,speed=10, polygon_file_path=None):
        super().__init__(uid, startPos, endPos, polygon_file_path)
        self._angle = angle
        self._acceleration = 0 #acceleration not considered yet
        self._move.setStart(startPos, 0)
        self._move.setEndPos(endPos)
        self._move.setTempStartPos(startPos)
        self._move.setSpeed(speed)
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

        if passedTime < self._totalFlightTime:
            if self._collisionAction != 2:
                self.manageObstacles( passedTime)

        return True if self._obstacleDetector_flag and self._collisionAction == 3 else False   # obstacle->remove/not remove node indicator


    def computeTotalFlightTime(self):
        move = self.getMove()
        if self._acceleration==0 and move.getSpeed()==0.0:
            return  0.0
        
        distance = math.sqrt((self._endPos.x - self._startPos.x) ** 2 + (self._endPos.y - self._startPos.y) ** 2 + (
                    self._endPos.z - self._startPos.z) ** 2)
        final_velocity = math.sqrt(self.getMove().getSpeed()**2 + 2*self._acceleration*distance) # v^2=u^2+2as
        average_velocity= (self.getMove().getSpeed()+final_velocity)/2
        assert average_velocity != 0, 'average velocity can not be 0'
        return distance/average_velocity

    def manageObstacles(self, passedTime):
        if self._obstacle == None:
            return
        futureTime= passedTime + Simulationparameter.stepLength

        currentDirection = self.getMove().getCurrentDirection()
        previousPos = self.getMove().getTempStartPos()
        x = previousPos.x + (currentDirection.x * self.getMove().getSpeed() * Simulationparameter.stepLength)
        y = previousPos.y + (currentDirection.y * self.getMove().getSpeed() * Simulationparameter.stepLength)
        # z = previousPos.z + (currentDirection.z * self.getMove().getSpeed() * Simulationparameter.stepLength) # no need since building height not given

        futureCoordinate = (x, y)

        # self._obstacleDetector_flag = self._obstracles[0].contains_point(futureCoordinate)
        # warnings.filterwarnings('once')
        detectObstacle = self._obstacle[0].contains_point(futureCoordinate)
        if not self._obstacleDetector_flag and detectObstacle and self._collisionAction==1:
            # warnings.warn('uav is going to collide in collide')
            logging.debug('WARNING!!!!')
            logging.debug('currentTime: %s, uav is going to collide at %s', str(passedTime), str(futureTime))

        self._obstacleDetector_flag = True if detectObstacle == True else self._obstacleDetector_flag

