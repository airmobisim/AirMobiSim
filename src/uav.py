import math

from .basemobility import Basemobility
from .splinemobility import Splinemobility
from .linearmobility import Linearmobility

class Uav:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid, startPos, endPos, totalFlightTime=0, waypointTime=0, waypointX=0, waypointY=0, angle=0, speed=10):
        self._uid = uid
        #This angle calculation overwrites the provided angle!!	
        self._angle = math.atan2(endPos.y - startPos.y, endPos.x - startPos.x) * 180 / math.pi
        #self._mobility = Splinemobility(uid, startPos, endPos, totalFlightTime, waypointTime, waypointX, waypointY)
        self._mobility  =  Linearmobility(uid, startPos, endPos, self._angle, speed)
    

    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

