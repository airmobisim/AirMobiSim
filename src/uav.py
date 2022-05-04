import math

from .basemobility import Basemobility
from .splinemobility import Splinemobility
from .linearmobility import Linearmobility


class Uav:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid, startPos, endPos, polygon_file_path):
        self._uid = uid
        self._angle = math.atan2(endPos.y - startPos.y, endPos.x - startPos.x) * 180 / math.pi
        self._mobility = Linearmobility(self._uid, self._angle, startPos, endPos, polygon_file_path)

    def getMobility(self):
        return self._mobility

    def logPosition(self):
        pass 

