import math

from .basemobility import Basemobility
from .splinemobility import Splinemobility
from .linearmobility import Linearmobility

class Uav:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid, startPos, endPos, totalFlightTime=0, waypointTime=0, waypointX=0, waypointY=0, angle=0, speed=20):
        self._uid = uid
        #self._mobility = Splinemobility(uid, startPos, endPos, totalFlightTime, waypointTime, waypointX, waypointY)
        self._angle = self.calculateAngle(startPos, endPos)
        self._mobility  =  Linearmobility(uid, startPos, endPos, self._angle, speed)
    

    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

    def calculateAngle(self, startPos, endPos):
        deltaY = endPos.y-startPos.y
        deltaX = endPos.x-startPos.x

        result = math.atan2(deltaY, deltaX)*180/math.pi
       
        if result < 0:
           result =  360 + result
        else:
           pass

        return result
