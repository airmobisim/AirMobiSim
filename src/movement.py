#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
# Copyright (C) 2022 Dalisha Logan <dalisha@mail.uni-paderborn.de>
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
from shapely.geometry import Point
import numpy as np

from src.simulationparameter import Simulationparameter


class Movement:
    def __init__(self):
        self._startPos = Point(0, 0, 0)
        self._endPos = Point(0, 0, 0)
        self._startTime = 0
        self._orientationX = 0
        self._orientationY = 0
        self._orientationZ = 0
        self._currentDirection = Point(0, 0, 0)
        self._speed = 0
        self._passedTime = 0
        self._futureTime = 0
        self._futureCoordinate = (0.0, 0.0)
        self._tempStartPos = Point(0, 0, 0)
        self._lastPos = Point(0, 0, 0)
        self._nextCoordinate = Point(0, 0, 0)
        self._startPosCircle = Point(0, 0, 0)
        self._finalFlag = False
        self._linear_mobility_sp = False  # spline mobility model in use?
        self._waypointsInsertedFlag = False
        self._totalDistance = 0.0


    def setFinalFlag(self, flag):
        self._finalFlag = flag

    def getFinalFlag(self):
        return self._finalFlag

    def setLinearMobilitySpFlag(self, flag):
        self._linear_mobility_sp = flag

    def getLinearMobilitySpFlag(self):
        return self._linear_mobility_sp

    def setWaypointsInsertedFlag(self, flag):
        self._waypointsInsertedFlag = flag

    def getWaypointsInsertedFlag(self):
        return self._waypointsInsertedFlag

    def setStart(self, startPos, startTime):
        self._startPos = startPos
        self._startTime = startTime

    def getStartTime(self):
        return self._startTime

    def getStartPos(self):
        return self._startPos

    def setStartPos(self, startPos):
        self._startPos = startPos

    def getEndPos(self):
        return self._endPos

    def setEndPos(self, lastPos):
        self._endPos = lastPos

    def getTempStartPos(self):
        return self._tempStartPos

    def setTempStartPos(self, tempStartPos):
        self._tempStartPos = tempStartPos

    def setNextCoordinate(self, nc):
        self._nextCoordinate = nc

    def getNextCoordinate(self):
        return self._nextCoordinate

    def setPassedTime(self, passedTime):
        self._passedTime = passedTime

    def getPassedTime(self):
        return self._passedTime

    def setFutureTime(self, time):
        self._futureTime = time

    def getFutureTime(self):
        return self._futureTime

    def setFutureCoordinate(self, coordinate):
        self._futureCoordinate = coordinate

    def getFutureCoordinate(self):
        return self._futureCoordinate

    def setSpeed(self, speed):
        self._speed = speed

    def getSpeed(self):
        return self._speed

    def setTotalDistance(self, distance):
        self._totalDistance = distance

    def getTotalDistance(self):
        return self._totalDistance

    def getCurrentDirection(self):
        return self._currentDirection

    def setCurrentDirection(self, currentDirection):
        self._currentDirection = currentDirection

    def setDirectionByTarget(self):

        direction = Point(self.getEndPos().x - self.getTempStartPos().x, self.getEndPos().y - self.getTempStartPos().y, self.getEndPos().z - self.getTempStartPos().z)
        distance = math.sqrt((self.getEndPos().x - self.getTempStartPos().x) ** 2 + (self.getEndPos().y - self.getTempStartPos().y) ** 2 + (self.getEndPos().z - self.getTempStartPos().z) ** 2)

        direction = np.array([direction.x, direction.y, direction.z])
        distance = np.array([distance, distance, distance])

        array = np.divide(direction, distance)
        newDirection = Point(round(array[0], 7), round(array[1], 7), round(array[2], 7))

        self.setCurrentDirection(newDirection)

    def getLastPos(self):
        return self._lastPos

    def setLastPos(self, newPos):
        self._lastPos = newPos