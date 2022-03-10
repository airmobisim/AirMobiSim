import geopandas
import math 
from shapely.geometry import Point
import numpy as np

class Movement:

    def __init__(self):
        self._startPos = Point(0, 0, 0)
        self._lastPos = Point(0, 0, 0)
        self._startTime = 0
        self._orientationX = 0
        self._orientationY = 0
        self._orientationZ = 0
        self._currentDirection = Point(0, 0, 0)
        self._speed = 0
        self._passedTime = 0

        self._nextCoordinate = Point(0, 0, 0)
        self._startPosCircle = Point(0, 0, 0)
        self._finalFlag = False
        self._linear_mobility_sp = False
        self._waypointsInsertedFlag=False

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

    def getLastPos(self):
        return self._lastPos

    def setLastPos(self, lastPos):
        self._lastPos = lastPos

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
    
    def setDirectionByTarget(self, target):
        '''
        print("Target.x: " + str(target.x))
        print("Target.y: " + str(target.y))
        print("Target.z: " + str(target.z))
        print("Start.x: " + str(self._startPos.x))
        print("Start.y: " + str(self._startPos.y))
        print("Start.z: " + str(self._startPos.z))
        '''
        direction = Point(target.x - self._startPos.x, target.y - self._startPos.y, target.z - self._startPos.z)
        distance = math.sqrt((target.x - self._startPos.x)**2 + (target.y - self._startPos.y)**2 + (target.z - self._startPos.z)**2)
        
        # Need to convert it into numpy arrays
        direction = np.array([direction.x, direction.y, direction.z])
        distance = np.array([distance, distance, distance]) 
    
        array = np.divide(direction, distance)
        newDirection = Point(array[0], array[1], array[2])
        #print("old direction: " + str(direction) + " new direction " + str(newDirection))
        self.setCurrentDirection(newDirection)
    


