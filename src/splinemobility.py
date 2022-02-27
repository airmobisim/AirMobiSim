import math
import geopandas
import numpy as np
from shapely.geometry import Point
from .basemobility import Basemobility
from scipy.interpolate import CubicSpline

from .simulationparameter import Simulationparameter


class Splinemobility(Basemobility):
    def __init__(self, uid, waypointTime, waypointX, waypointY, waypointZ):
        self._startpos=Point(waypointX[0],waypointY[0],waypointZ[0])
        self._endpos=Point(waypointX[-1],waypointY[-1],waypointZ[-1])
        self._totalFlightTime = waypointTime[-1]

        super().__init__(uid, self._startpos, self._endpos)

        self._waypointTime = waypointTime
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ
        self._uid = uid
        self._move.setStart(self._startpos, 0)
        self._move.setLastPos(self._endpos)
        self._move.setTempStartPos(self._startpos) # holds each intermediate points of linear in each iteration
        # since spline so fixing it to true, this flag is used to separate some code from other mobility
        self._move.setLinearMobilitySpFlag(True)
        # self._totalFlightTime= totalFlightTime
        print(waypointTime)
        self._speed= 1.5
        # self._waypointTimeN=Splinemobility.insertWaypointTime()
        # Splinemobility.computeSplineDistance()
        self.insertWaypointTime()
    def makeMove(self):
        #object of Movement
        move = self.getMove()

        # calculate the time elapsed
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        # for linear mobility with cubic spline
        if move.getLinearMobilitySpFlag():

            if 0.0 <= passedTime < self._totalFlightTime :
                '''
                reduce computation by passing the following lines in constructor
                '''

                spl_x = CubicSpline(self._waypointTime, self._waypointX)
                spl_y = CubicSpline(self._waypointTime, self._waypointY)
                spl_z = CubicSpline(self._waypointTime, self._waypointZ)
                nextCoordinate= Point(spl_x(passedTime), spl_y(passedTime), spl_z(passedTime))
                move.setNextCoordinate(nextCoordinate)


                pass

            elif passedTime>= self._totalFlightTime :
                move.setFinalFlag(True)
                # move.setLinearMobilitySpFlag(False)
                # move.setSpeed(0.0)



            pass
        move.setPassedTime(passedTime)
        super().makeMove()


    def insertWaypointTime(self):
        area_of_segments= Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        total_spline_distance=np.sum(area_of_segments)
        total_flight_time= total_spline_distance/self._speed
        print('total flight time')
        print(total_flight_time)




    @staticmethod         # this functions returns area of segments for each waypoint segments
    def computeSplineDistance(waypointX=[0,6,12],waypointY=[0,6,12],waypointZ=[3,3,3]):
        waypointCount=len(waypointX)
        waypointIndex=np.linspace(0,waypointCount-1,num=waypointCount)
        # print('inside computer spline distance')
        # print(waypointIndex)
        spl_x = CubicSpline(waypointIndex, waypointX)
        spl_y = CubicSpline(waypointIndex, waypointY)
        spl_z = CubicSpline(waypointIndex, waypointZ)

        area_of_segments=[]   # 1 less thank number of points
        for i in range(waypointCount-1):
            number_of_small_segment=100

            segments_of_index=np.linspace(waypointIndex[i], waypointIndex[i + 1], number_of_small_segment)
            segments_small_x=spl_x(segments_of_index)
            segments_small_y=spl_y(segments_of_index)
            segments_small_z=spl_z(segments_of_index)
            # print(len(segments_of_x))
            # print(type(segments_of_x))
            segments_distance=0
            for i in range(number_of_small_segment-1):
                segments_distance += math.sqrt((segments_small_x[i+1] - segments_small_x[i])**2 +(segments_small_y[i+1] - segments_small_y[i])**2 + (segments_small_z[i+1] - segments_small_z[i])**2 )

            area_of_segments.append(segments_distance)

        # print(np.sum(area_of_segment))


        return area_of_segments




