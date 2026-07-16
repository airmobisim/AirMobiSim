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

import numpy as np
from scipy.interpolate import CubicSpline
from shapely.geometry import Point
from .basemobility import Basemobility
from .simulationparameter import Simulationparameter

import src.logWrapper as logWrapper

class Splinemobility(Basemobility):
    def __init__(self, uav, uid, waypointX, waypointY, waypointZ, speed, polygon_file_path=None, collision_action=None):

        self._totalDistance = 0.0
        self._acceleration = 2.0
        self._startpos = Point(waypointX[0], waypointY[0], waypointZ[0])
        self._endpos = Point(waypointX[-1], waypointY[-1], waypointZ[-1])
        super().__init__(uav, uid, speed, polygon_file_path, collision_action)
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ
        self._move.setTotalDistance(np.sum(Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)))
        self._uid = uid
        self._move.setLinearMobilitySpFlag(True)    # spline mobility model in use indicator
        # self.updateWaypointsByIndex()     # uncomment this line when you want to use insertion of waypoints
        # self._waypointTime = self.insertWaypointTime()
        # self._totalFlightTime = self._waypointTime[-1]
        self._totalFlightTime = self.computeTotalFlightTime(0.0, speed, self._acceleration)
        self._indexPerUnitDistance = 50
        self._max_index_value = None
        self._waypointIndex = self.insertWaypointIndex()
        self._current_index = 0
        self._distanceTravelledSoFar = 0.0
        self._angle = 0.0
        self._need_to_generate_spline= True
        self._spl_x = None
        self._spl_y = None
        self._spl_z = None
        self._arclength_samples = None
        self._arclength_cumdist = None




        logWrapper.debug(f"speed: {str(speed)}; total flightTime: {str(self._totalFlightTime)}" )
        logWrapper.debug(f"startpos: {self._startpos}" )


    def makeMove(self):
        move = self.getMove()

        if self._uav.getWaypointInsertedFlag():
            self.insertWaypoint()
            self._need_to_generate_spline= True

        # calculate the time elapsed
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        if passedTime >= self._totalFlightTime:
            move.setFinalFlag(True)
            # move.setSpeed(0.0)

        move.setPassedTime(passedTime)
        super().makeMove()
        return True if self._obstacleDetector_flag and self._collisionAction == 3 else False


    def insertWaypoint(self):
        self._uav.setWaypointInsertedFlag(False)

        newWaypointsX, newWaypointsY, newWaypointsZ = self._uav.splitWaypoints()

        self._waypointX, self._waypointY, self._waypointZ = newWaypointsX, newWaypointsY, newWaypointsZ
        self._move.setTotalDistance(np.sum(Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)))
        self._totalFlightTime = self.computeTotalFlightTime(0.0, self._speed, self._acceleration)
        self._waypointIndex = self.insertWaypointIndex()

        logWrapper.debug('waypoint inserted')

    def insertWaypointTime(self):

        distance_of_segments = Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        total_spline_distance = np.sum(distance_of_segments)
        total_flight_time = total_spline_distance / self._speed if self._speed != 0 else -1


        waypointTime = []
        # now put time stamp for each waypoint
        for i in range(len(self._waypointX)):
            if i == 0:
                waypointTime.append(0)
            elif i == len(self._waypointX) - 1:
                waypointTime.append(total_flight_time)

            else:
                time_needed_for_this_segment = (distance_of_segments[i - 1] / total_spline_distance) * total_flight_time
                waypointTime.append(waypointTime[-1] + time_needed_for_this_segment)

        return waypointTime

    @staticmethod  # this function returns area of  waypoint segments
    def computeSplineDistance(waypointX, waypointY, waypointZ):
        waypointCount = len(waypointX)
        waypointIndex = np.linspace(0, waypointCount - 1, num=waypointCount)

        spl_x = CubicSpline(waypointIndex, waypointX)
        spl_y = CubicSpline(waypointIndex, waypointY)
        spl_z = CubicSpline(waypointIndex, waypointZ)

        distance_of_segments = []
        for i in range(waypointCount - 1):
            number_of_small_segment = 10000

            segments_of_index = np.linspace(waypointIndex[i], waypointIndex[i + 1], number_of_small_segment)
            segments_small_x = spl_x(segments_of_index)
            segments_small_y = spl_y(segments_of_index)
            segments_small_z = spl_z(segments_of_index)

            segments_distance = 0
            for i in range(number_of_small_segment - 1):
                segments_distance += math.sqrt((segments_small_x[i + 1] - segments_small_x[i]) ** 2 + (
                        segments_small_y[i + 1] - segments_small_y[i]) ** 2 + (
                                                       segments_small_z[i + 1] - segments_small_z[i]) ** 2)

            distance_of_segments.append(segments_distance)

        return distance_of_segments

    def calculateNextPosition(self):
        move = self.getMove()
        lastpos = move.getNextCoordinate()

        if self._acceleration != 0:
            newVelocity = move.getSpeed() + self._acceleration * Simulationparameter.stepLength
            move.setSpeed(newVelocity)

        distance_to_travel = move.getSpeed() * Simulationparameter.stepLength + 0.5 * self._acceleration * (Simulationparameter.stepLength) ** 2

        self.computeIndexForDistance(distance_to_travel)  # also (re)builds the cached splines/arclength table if needed

        nextCoordinate = Point(self._spl_x(self._current_index), self._spl_y(self._current_index), self._spl_z(self._current_index))
        move.setNextCoordinate(nextCoordinate)

        if self.getMove().getFinalFlag():
            move.setNextCoordinate(lastpos)

        if self._collisionAction != 2:
            future_time = move.getPassedTime() + Simulationparameter.stepLength
            move.setFutureCoordinate((self._spl_x(self._current_index), self._spl_y(self._current_index)))
            self.manageObstacles(move.getPassedTime(), future_time)

    def insertWaypointIndex(self):
        segment_distance = Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        waypointIndex = []
        # max_index_value = 1000
        self._max_index_value = np.sum(segment_distance) * self._indexPerUnitDistance
        for i in range(len(self._waypointX)):
            if i == 0:
                waypointIndex.append(0)
            elif i == len(self._waypointX) - 1:
                waypointIndex.append(self._max_index_value)

            else:
                # indexValue_needed_for_this_segment = (segment_distance[i - 1] / self._totalDistance) * self._max_index_value
                indexValue_needed_for_this_segment = segment_distance[i - 1] * self._indexPerUnitDistance
                waypointIndex.append(waypointIndex[-1] + indexValue_needed_for_this_segment)


        return waypointIndex

    def computeIndexForDistance(self, distance_to_travel):
        if self._need_to_generate_spline:
            self.generateArclengthTable()
            self._need_to_generate_spline = False

        if self._totalDistance - self._distanceTravelledSoFar >= distance_to_travel:
            targetDistance = self._distanceTravelledSoFar + distance_to_travel
            if targetDistance <= self._arclength_cumdist[-1]:
                # invert the (monotonic) arclength-to-index table via interpolation
                # instead of a per-step linear search over the index domain
                self._current_index = float(np.interp(targetDistance, self._arclength_cumdist, self._arclength_samples))
                self._distanceTravelledSoFar = targetDistance
            else:
                self.getMove().setFinalFlag(True)

    def generateArclengthTable(self):
        # lookup table mapping travelled arclength -> spline index, built once per waypoint set
        self._spl_x = CubicSpline(self._waypointIndex, self._waypointX)
        self._spl_y = CubicSpline(self._waypointIndex, self._waypointY)
        self._spl_z = CubicSpline(self._waypointIndex, self._waypointZ)

        num_samples = int(min(200000, max(2000, self._max_index_value * 4)))
        samples = np.linspace(0, self._max_index_value, num_samples)
        sx = self._spl_x(samples)
        sy = self._spl_y(samples)
        sz = self._spl_z(samples)
        segment_lengths = np.sqrt(np.diff(sx) ** 2 + np.diff(sy) ** 2 + np.diff(sz) ** 2)

        self._arclength_samples = samples
        self._arclength_cumdist = np.concatenate(([0.0], np.cumsum(segment_lengths)))