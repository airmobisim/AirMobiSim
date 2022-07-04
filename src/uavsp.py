from .basemobility import Basemobility
from .splinemobility import Splinemobility

class UavSp:
    _uid = -1
    _mobility = Basemobility

    def __init__(self, uid,  waypointX, waypointY, waypointZ,speed,polygon_file_path):
        self._uid = uid
        self._mobility = Splinemobility(uid, waypointX, waypointY, waypointZ, speed, polygon_file_path)

    def getMobility(self):
        return self._mobility
