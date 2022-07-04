import math
from .basemobility import Basemobility
from .splinemobility import Splinemobility

class UavSp:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid,  waypointX, waypointY, waypointZ,speed,polygon_file_path,collision_action):
        self._uid = uid
        self._angle = self.calculateAngle(waypointX, waypointY)
        # print('angle: ',self._angle)
        self._mobility = Splinemobility(uid, waypointX, waypointY, waypointZ, speed, polygon_file_path,collision_action)

    def getMobility(self):
        return self._mobility

    def calculateAngle(self, waypointX, waypointY):
        deltaY = waypointY[-1] - waypointY[0]
        deltaX = waypointX[-1] - waypointX[0]

        result = math.atan2(deltaY, deltaX)

        if result < 0:
            result = 360 + result

        return result
