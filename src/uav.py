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

from .basemobility import Basemobility
from .linearmobility import Linearmobility

import src.logWrapper as logWrapper
from shapely.geometry import Point

class Uav():
    _uid = -1
    _mobility = None
    _waypoints = []
    def __init__(self, uid, startPos, endPos, speed, polygon_file_path=None,collision_action=None,angle=0):
        self._uid = uid
        self._angle = self.calculateAngle(startPos, endPos)
        self.addWaypoint(Point(startPos.x, startPos.y, startPos.z), 0)
        self.addWaypoint(Point(endPos.x, endPos.y, endPos.z), 1)
        self._mobility  =  Linearmobility(self, uid, self._angle, speed, polygon_file_path,collision_action)
        
        self._mobility.updateEndPos()

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
