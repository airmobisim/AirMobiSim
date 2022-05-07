import math

from .basemobility import Basemobility
#from .splinemobility import Splinemobility
from .linearmobility import Linearmobility

class Uav:
    _uid = -1
    _mobility = Basemobility
    def __init__(self, uid, startPos, endPos, angle=0, speed=50):
        self._uid = uid
        self._angle = self.calculateAngle(startPos, endPos) 
        self._mobility  =  Linearmobility(uid, startPos, endPos, self._angle, speed)

    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

    def calculateAngle(self, startPos, endPos):
        deltaY = endPos.y-startPos.y
        deltaX = endPos.x-startPos.x

        result = math.atan2(deltaY, deltaX)
       
        if result < 0: 
           result =  360 + result
        print("I am calculating the angle", flush=True)
        print(result, flush=True)
        return result
