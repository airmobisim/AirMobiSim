import math

from .basemobility import Basemobility
from .splinemobility import Splinemobility
from .linearmobility import Linearmobility


class Uav:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid, startPos, endPos, waypointTime=0, waypointX=0, waypointY=0, waypointZ=0,linearMobilityFlag=False,splineMobilityFlag=False):
        self._uid = uid
        # self._angle = math.atan2(endPos.y - startPos.y, endPos.x - startPos.x) * 180 / math.pi

        if splineMobilityFlag:
            self._mobility = Splinemobility(uid,  waypointTime, waypointX, waypointY, waypointZ)
        else:
            self._mobility = Linearmobility(self._uid, self._angle, startPos, endPos)
    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

