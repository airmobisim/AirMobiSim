import math 

from .simpleapp import Simpleapp
from .simplemissioncontrol import Simplemissioncontrol 
from .simplemobility import Simplemobility
from .linearmobility import Linearmobility
from .basemobility import Basemobility

class Uav:
    _uid = -1
    _mobility = Basemobility 
    def __init__(self,uid, startPos, endPos):
        self._uid = uid
        angle = math.atan2(endPos.y - startPos.y, endPos.x - startPos.x) * 180 / math.pi
        self._mobility = Linearmobility(uid, angle, startPos, endPos)

    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

