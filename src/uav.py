import math

from .basemobility import Basemobility
from .linearmobility import Linearmobility

import src.logWrapper as logWrapper
from shapely.geometry import Point

class Uav:
    _uid = -1
    _mobility = Basemobility
    _waypoints = []
    def __init__(self, uid, startPos, endPos, speed, polygon_file_path=None,collision_action=None,angle=0):
        self._uid = uid
        self._angle = self.calculateAngle(startPos, endPos) 
        self.addWaypoint(Point(startPos.x, startPos.y, startPos.z))
        self.addWaypoint(Point(endPos.x, endPos.y, endPos.z))
        self_currentWaypointIndex = 0
        self._mobility  =  Linearmobility(self, uid, self._angle, speed, polygon_file_path,collision_action)


    def getMobility(self):
        return self._mobility

    def logPosition(self):
        logWrapper.info("UAV: " + str(self._uid) + " Position: " + str(self._mobility.getCurrentPosition()))

    def addWaypoint(self, waypoint, index = -1):
        if isinstance(waypoint, Point):
            if index == -1:
                self._waypoints.append(waypoint)
            elif index > -1:
                self._waypoints.insert(index, waypoint)
        else:
            logWrapper.error("Waypoint is not a Point")
            raise Exception("Waypoint is not a Point")
        pass    

    def calculateAngle(self, startPos, endPos):
        deltaY = endPos.y-startPos.y
        deltaX = endPos.x-startPos.x

        result = math.atan2(deltaY, deltaX)
       
        if result < 0: 
           result =  360 + result

        return result
