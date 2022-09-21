#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
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
from .simulationparameter import Simulationparameter

import src.logWrapper as logWrapper

class Linearmobility(Basemobility):

    def __init__(self, uav, uid, angle, speed=0, polygon_file_path=None,collision_action=None):
        super().__init__(uav, uid, speed, polygon_file_path,collision_action)
        self._uid = uid
        self._angle = angle
        self._acceleration = 0  # acceleration not considered yet
        self._totalFlightTime = self.computeTotalFlightTime(0.0,speed,self._acceleration)

    def updateEndPos(self):
        self._move.setEndPos(self._uav._waypoints[-1])

    def makeMove(self):
        move = self.getMove()
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        move.setTempStartPos(move.getLastPos())

        distancePerstep = self.getMove().getSpeed()*Simulationparameter.stepLength
        distance = self.getCurrentPos().distance(self._uav._waypoints[self._currentWaypointIndex+1])
        if self.getCurrentPos().distance(self._uav._waypoints[self._currentWaypointIndex+1])<distancePerstep:
            logWrapper.info("UAV " + self._uid.__str__() + " reached waypoint " + self._currentWaypointIndex.__str__() + " waypoint position: " + self._uav._waypoints[self._currentWaypointIndex+1].__str__() + " current position: " + self.getCurrentPos().__str__())
            self._currentWaypointIndex = self._currentWaypointIndex  + 1
            if self._currentWaypointIndex == len(self._uav._waypoints)-1: #there are no further waypoints
                logWrapper.info("UAV " + self._uid.__str__() + " reached all configured waypoints")
                self.getMove().setFinalFlag(True)
            else:
                logWrapper.info("UAV " + self._uid.__str__() + " starts to move towards the next waypoint " + self._uav._waypoints[self._currentWaypointIndex+1].__str__())
                self.getMove().setTempStartPos(self.getCurrentPos())
                self.getMove().setEndPos(self._uav._waypoints[self._currentWaypointIndex+1])
              

        move.setDirectionByTarget()
        newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength

       # if passedTime >= self._totalFlightTime:
           # newSpeed = 0.0
           # self._acceleration = 0.0
           # print("passedTime >= self._totalFlightTime")
           # self.getMove().setFinalFlag(True)

        move.setSpeed(newSpeed)
        move.setPassedTime(passedTime)
        super().makeMove()

        #if passedTime < self._totalFlightTime:
        #    if self._collisionAction != 2:
        #        future_time = passedTime + Simulationparameter.stepLength
        #        self.setFutureCoordinate()
        #        self.manageObstacles(passedTime, future_time)

        return True if (self._obstacleDetector_flag and self._collisionAction == 3) or self.getMove().getFinalFlag() else False  # obstacle->remove/not remove node indicator

    def computeTotalDistance(self):
            return math.sqrt((self._uav._waypoints[-1].x - self._uav._waypoints[self._currentWaypointIndex].x) ** 2 + (self._uav._waypoints[-1].y - self._uav._waypoints[self._currentWaypointIndex].y) ** 2 + (
                self._uav._waypoints[-1].z - self._uav._waypoints[self._currentWaypointIndex].z) ** 2)

    # set future x,y coordinate for building detection
    def setFutureCoordinate(self):
        currentDirection = self.getMove().getCurrentDirection()
        previousPos = self.getMove().getTempStartPos()
        x = previousPos.x + (currentDirection.x * self.getMove().getSpeed() * Simulationparameter.stepLength)
        y = previousPos.y + (currentDirection.y * self.getMove().getSpeed() * Simulationparameter.stepLength)

        futureCoordinate = (x, y)

        # self._obstacleDetector_flag = self._obstacles[0].contains_point(futureCoordinate)
        # warnings.filterwarnings('once')
        detectObstacle = self._obstacle[0].contains_point(futureCoordinate)
        if not self._obstacleDetector_flag and detectObstacle and self._collisionAction==1:
            # warnings.warn('uav is going to collide in collide')
            print('WARNING!!!!')
            print('currentTime:',passedTime,'uav is going to collide at ', futureTime)

        self._obstacleDetector_flag = True if detectObstacle == True else self._obstacleDetector_flag
