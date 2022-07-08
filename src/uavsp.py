#
# Copyright (C) 2022 Touhid Hossain Pritom <pritom@campus.uni-paderborn.de>
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
