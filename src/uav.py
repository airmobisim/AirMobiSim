#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
# Copyright (C) 2022 Dalisha Logan <dalisha@mail.uni-paderborn.de>
#
# Documentation for these modules is at http://veins.car2x.org/
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import math
import sys

from .basemobility import Basemobility
from .linearmobility import Linearmobility
from .splinemobility import Splinemobility

import src.logWrapper as logWrapper
from shapely.geometry import Point

class Uav():
    _uid = -1
    _mobility = None
    _waypoints = []

    def __init__(self, uid, waypoints: list[Point], speed, polygon_file_path=None, collision_action=None,model_selection=None, removeNode=False):
        if model_selection != 1 and model_selection != 2:
            logWrapper.critical(f'model_selection value can either be 1 or 2 but given {model_selection}. 1 for linear model and 2 for spline model. check uav.py')
            sys.exit()
        startPos = waypoints[0]
        endPos = waypoints[-1]
        self._waypoints = waypoints
        self._uid = uid
        self._angle = self.calculateAngle(startPos, endPos)
        self._waypointInserted = False

        if model_selection == 1:
            self._mobility = Linearmobility(self, uid, self._angle, speed, polygon_file_path, collision_action,removeNode=False)
            self._mobility.updateEndPos()

        elif model_selection == 2:
            waypointX, waypointY, waypointZ = self.splitWaypoints()
            self._mobility = Splinemobility(self, uid, waypointX, waypointY, waypointZ, speed, polygon_file_path,collision_action)

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
            logWrapper.error("Waypoint is not a Point object")
            raise Exception("Waypoint is not a Point object")
        pass    

    def calculateAngle(self, startPos, endPos):
        deltaY = endPos.y-startPos.y
        deltaX = endPos.x-startPos.x

        result = math.atan2(deltaY, deltaX)
       
        if result < 0: 
           result =  360 + result

        return result

    def splitWaypoints(self):
        wpX = []
        wpY = []
        wpZ = []

        for wp in self._waypoints:
            wpX.append(wp.x)
            wpY.append(wp.y)
            wpZ.append(wp.z)

        return wpX, wpY, wpZ

    def setWaypointInsertedFlag(self, flag):
        self._waypointInserted = flag

    def getWaypointInsertedFlag(self):
        return self._waypointInserted
