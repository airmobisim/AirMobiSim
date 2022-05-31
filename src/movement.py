import math
from shapely.geometry import Point
import numpy as np

class Movement:


    def __init__(self):
        self._startPos = Point(0, 0, 0)
        self._endPos = Point(0, 0, 0)
        self._lastPos =  Point(0, 0, 0)
        self._startTime = 0
        self._orientationX = 0
        self._orientationY = 0
        self._orientationZ = 0
        self._currentDirection = Point(0, 0, 0)
        self._speed = 0
        self._passedTime = 0
        self._tempStartPos=Point(0, 0, 0)
        self._nextCoordinate = Point(0, 0, 0)
        self._startPosCircle = Point(0, 0, 0)
        self._finalFlag = False
        self._linear_mobility_sp = False
        self._waypointsInsertedFlag = False

    def setFinalFlag(self, flag):
        self._finalFlag = flag

    def getFinalFlag(self):
        return self._finalFlag

    def setLinearMobilitySpFlag(self, flag):
        self._linear_mobility_sp = flag

    def getLinearMobilitySpFlag(self):
        return self._linear_mobility_sp

    def setWaypointsInsertedFlag(self, flag):
        self._waypointsInsertedFlag = flag

    def getWaypointsInsertedFlag(self):
        return self._waypointsInsertedFlag

    def setStart(self, startPos, startTime):
        self._startPos = startPos
        self._startTime = startTime
    
    def getStartTime(self):
        return self._startTime
    
    def getStartPos(self):
        return self._startPos

    def setStartPos(self, startPos):
        self._startPos = startPos

    def getEndPos(self):
        return self._endPos

    def setEndPos(self, lastPos):
        self._endPos = lastPos

    def getTempStartPos(self):
        return self._tempStartPos

    def setTempStartPos(self, tempStartPos):
        self._tempStartPos = tempStartPos

    def setNextCoordinate(self, nc):
        self._nextCoordinate = nc

    def getNextCoordinate(self):
        return self._nextCoordinate

    def setPassedTime(self, passedTime):
        self._passedTime = passedTime

    def getPassedTime(self):
        return self._passedTime

    def setSpeed(self, speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def getCurrentDirection(self):
        return self._currentDirection
    
    def setCurrentDirection(self,currentDirection):
        self._currentDirection = currentDirection
    
    def setDirectionByTarget(self):
        direction = Point(self._endPos.x - self._startPos.x, self._endPos.y - self._startPos.y, self._endPos.z - self._startPos.z)
        distance = math.sqrt((self._endPos.x - self._startPos.x)**2 + (self._endPos.y - self._startPos.y)**2 + (self._endPos.z - self._startPos.z)**2)
 
        direction = np.array([direction.x, direction.y, direction.z])
        distance = np.array([distance, distance, distance]) 

        array = np.divide(direction, distance)
        newDirection = Point(round(array[0],2), round(array[1],2), round(array[2],2))

        self.setCurrentDirection(newDirection)


