import math
import numpy as np
import geopandas
import numpy as np
from shapely.geometry import Point
from .basemobility import Basemobility
from scipy.interpolate import CubicSpline

from .simulationparameter import Simulationparameter
from proto.DroCIBridge import AirMobiSim


class Splinemobility(Basemobility):
    def __init__(self, uid, speed, waypointX, waypointY, waypointZ):
        self._startpos=Point(waypointX[0],waypointY[0],waypointZ[0])
        self._endpos=Point(waypointX[-1],waypointY[-1],waypointZ[-1])
        # self._totalFlightTime = waypointTime[-1]

        super().__init__(uid, self._startpos, self._endpos)
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ

        self._uid = uid
        self._move.setStart(self._startpos, 0)
        self._move.setLastPos(self._endpos)
        self._move.setTempStartPos(self._startpos) # holds each intermediate points of linear in each iteration

        # since spline so fixing it to true, this flag is used to separate some code from other mobility
        self._move.setLinearMobilitySpFlag(True)


        self._waypointsInsertedFlag=False     # this decides calling of updateWaypointsByIndex()

        self._speed= speed
        self._waypointTime = self.insertWaypointTime()
        self._totalFlightTime = self._waypointTime[-1]


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
                #########
                if self._waypointsInsertedFlag == False:  # if waypoints is not inserted this this add the waypoints if already inserted then it will ignore
                    self._waypointsInsertedFlag=True    #done once at the beginning
                    self.updateWaypointsByIndex()  # to insert way points

                ########

                spl_x = CubicSpline(self._waypointTime, self._waypointX)
                spl_y = CubicSpline(self._waypointTime, self._waypointY)
                spl_z = CubicSpline(self._waypointTime, self._waypointZ)



                nextCoordinate= Point(spl_x(passedTime), spl_y(passedTime), spl_z(passedTime))
                move.setNextCoordinate(nextCoordinate)




            elif passedTime>= self._totalFlightTime :
                move.setFinalFlag(True)
                # move.setLinearMobilitySpFlag(False)
                # move.setSpeed(0.0)


        move.setPassedTime(passedTime)
        super().makeMove()

    def updateWaypointsByIndex(self):

        waypointsIndex, waypointsX, waypointsY, waypointsZ = AirMobiSim.getWaypointsByIndex()


        if waypointsIndex != None:
            # print('hello hello')
            time = self._waypointTime.copy().tolist()
            x = self._waypointX.copy()
            y = self._waypointY.copy()
            z = self._waypointZ.copy()


            for i, v in enumerate(waypointsIndex):
                if 1 <= v <= len(time) - 2:
                    # print('vertex: ',v)
                    time.insert(v, (time[v] + time[v - 1]) / 2)
                    x= np.insert(x,v, waypointsX[i])
                    y=np.insert(y,v, waypointsY[i])
                    z=np.insert(z,v, waypointsZ[i])


            # spl_x = CubicSpline(time, x)
            # spl_y = CubicSpline(time, y)
            # spl_z = CubicSpline(time, z)
            self._waypointTime = time
            self._waypointX = x
            self._waypointY = y
            self._waypointZ = z
            print('waypoint inserted')




    def insertWaypointTime(self):
        distance_of_segments= Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        total_spline_distance=np.sum(distance_of_segments)
        total_flight_time= total_spline_distance/self._speed
        print(' func insertWaypointTime total flight time')
        print(total_flight_time)

        waypointTime=[]
        # now put time stamp for each waypoint
        for i in range(len(self._waypointX)):
            if i==0:
                waypointTime.append(0)
            elif i== len(self._waypointX)-1:
                waypointTime.append(total_flight_time)

            else:
                time_needed_for_this_segment= (distance_of_segments[i-1]/total_spline_distance)*total_flight_time
                waypointTime.append(waypointTime[-1]+time_needed_for_this_segment)

        #print('generated time stamp')
        #print(waypointTime)
        # print(len(self._waypointX))
        return waypointTime




    @staticmethod         # this functions returns area of segments for each waypoint segments
    def computeSplineDistance(waypointX=[0,6,12],waypointY=[0,6,12],waypointZ=[3,3,3]):
        waypointCount=len(waypointX)
        waypointIndex=np.linspace(0,waypointCount-1,num=waypointCount)
        # print('inside computer spline distance')
        # print(waypointIndex)
        spl_x = CubicSpline(waypointIndex, waypointX)
        spl_y = CubicSpline(waypointIndex, waypointY)
        spl_z = CubicSpline(waypointIndex, waypointZ)

        distance_of_segments=[]   # 1 less thank number of points
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

            distance_of_segments.append(segments_distance)

        # print(np.sum(area_of_segment))


        return distance_of_segments




