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
from abc import ABC, abstractmethod
import os
from xml.dom import minidom

import numpy as np
from shapely.geometry import Point

from .baseenergy import Baseenergy
from .movement import Movement
from .resultcollection import Resultcollection
from .simulationparameter import Simulationparameter
import matplotlib.path as mplPath
import src.logWrapper as logWrapper


class Basemobility(ABC):
    polygon_file_path = None
    _uav = None
    def __init__(self, uav, uid, speed, polygon_file_path,collision_action):
        self._uav = uav
        self._uid = uid
        self._speed = speed
        self._move = Movement()
        self._resultcollection =  Resultcollection()
        self._baseenergy = Baseenergy()
        self._move.setStart(self._uav._waypoints[0], 0)
        self._move.setTempStartPos(self._uav._waypoints[0])
        self._move.setLastPos(self._uav._waypoints[0])
        self._move.setNextCoordinate(self._uav._waypoints[-1])
        self._move.setEndPos(self._uav._waypoints[-1])
        
        self._currentWaypointIndex = 0

        self._move.setSpeed(self._speed)
        self._move.setTotalDistance(self.computeTotalDistance())
        
        self._collisionAction = collision_action  # 1= warn, 2 = no action 3=remove uav; anything else is wrong
        self._obstacleDetector_flag = False
        self.polygon_file_path = polygon_file_path
        self._obstacles = self.ParsePolygonFileToObstacles()


    def getMove(self):
        return self._move

    def getCurrentPos(self):
        return self._move.getTempStartPos()

    # current position function for spline mobility
    def getCurrentPosSp(self):
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        if passedTime==0:
            return self._uav._waypoints[0]
        
        if not self.getMove().getFinalFlag():
            currentPos = self.getMove().getNextCoordinate()
            return currentPos

        elif self.getMove().getFinalFlag():
            currentPos = self.getMove().getNextCoordinate()

        return currentPos

    @abstractmethod
    def calculateNextPosition(self):
        pass


    def makeMove(self):
        self.doLog()
        self.calculateNextPosition()

    def doLog(self):
        if self.getMove().getLinearMobilitySpFlag():   # log for spline mobility
            self._resultcollection.logCurrentPosition(self._uid, self.getCurrentPosSp(), self.getMove())
        else:   # log for linear mobility
            self._resultcollection.logCurrentPosition(self._uid, self.getCurrentPos(), self.getMove())
        currentEnergy = self._baseenergy.getcurrentEnergy(self.getMove().getSpeed(), (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime())

        self._resultcollection.logCurrentEnergy(self._uid,currentEnergy[0], currentEnergy[1])
        pass

    def ParsePolygonFileToObstacles(self):
        if self.polygon_file_path is None or not os.path.exists(self.polygon_file_path):
            return None

        logWrapper.debug(("self.polygon_file_path: " + str(self.polygon_file_path)))

        parsedFile= minidom.parse(self.polygon_file_path)
        polygons = parsedFile.getElementsByTagName('poly')
        buildings=[]
        for polygon in polygons:
            shape_of_polygon = polygon.attributes['shape'].value
            vertex_coordinates= shape_of_polygon.split(' ')       # coordinates are of string type

            list_of_coordinates=[]
            for single_vertex in vertex_coordinates:       # x and y coordinates are seperated and converted to float
                list_of_coordinates.append([float(single_vertex.split(',')[0]),float(single_vertex.split(',')[1])])

            # forming shape of polygon by joining the polygon coordinates and appended to building list
            buildings.append(mplPath.Path(np.array(list_of_coordinates)))


        return buildings

    def computeTotalFlightTime(self, currentTime, speed, acceleration):
        if speed == 0 and acceleration == 0:
            return 0
        distance = self.getMove().getTotalDistance()
        final_velocity = math.sqrt(speed ** 2 + 2 * acceleration * distance)  # v^2=u^2+2as
        average_velocity = (speed + final_velocity) / 2
        assert average_velocity != 0, 'avarage velocity can not be 0'
        flightTime = distance / average_velocity + currentTime
        return flightTime

    def manageObstacles(self, passedTime,futureTime):
        if self._obstacles == None:
            return
        futureCoordinate = self.getMove().getFutureCoordinate()

        detectObstacle = any(obstacle.intersects_path(mplPath.Path([[self.getCurrentPos().x,self.getCurrentPos().y ],[futureCoordinate[0],futureCoordinate[1]]])) for obstacle in self._obstacles)
        if not self._obstacleDetector_flag and detectObstacle and self._collisionAction == 1:
            logWrapper.warning('Warning ################################ ', True)
            logWrapper.debug(('currentTime: ' + str(passedTime) + ', uav is going to collide at '+ str(futureTime)))

        self._obstacleDetector_flag = True if detectObstacle == True else self._obstacleDetector_flag
