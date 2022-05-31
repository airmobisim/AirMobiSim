import math

import numpy as np
from proto.DroCIBridge import AirMobiSim
from scipy.interpolate import CubicSpline
from shapely.geometry import Point

from .basemobility import Basemobility
from .simulationparameter import Simulationparameter

import logging

class Splinemobility(Basemobility):
    def __init__(self, uid, waypointX, waypointY, waypointZ, speed, polygon_file_path=None):
        self._startpos=Point(waypointX[0],waypointY[0],waypointZ[0])
        self._endpos=Point(waypointX[-1],waypointY[-1],waypointZ[-1])
        # self._totalFlightTime = waypointTime[-1]

        super().__init__(uid, self._startpos, self._endpos, polygon_file_path)
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ

        self._uid = uid
        self._move.setStart(self._startpos, 0)
        self._move.setEndPos(self._endpos)
        # self._move.setTempStartPos(self._startpos) # holds each intermediate points of linear in each iteration
        self._move.setNextCoordinate(self._startpos) # holds each intermediate points of linear in each iteration

        # since spline so fixing it to true, this flag is used to separate some code from other mobility
        self._move.setLinearMobilitySpFlag(True)
        # self._waypointsInsertedFlag=True     # this decides calling of updateWaypointsByIndex()
        # self.updateWaypointsByIndex()     # uncomment this line when you want to use insertion of waypoints
        self._speed= speed
        self._waypointTime = self.insertWaypointTime()
        # self._totalFlightTime = self._waypointTime[-1]
        self._totalFlightTime = self.computeTotalFlightTime(0.0, speed, 0)
        logging.debug("speed: %s; total flightTime: %s", str(speed), str(self._totalFlightTime))
        logging.debug("startpos: %s", self._startpos)

    def makeMove(self):
        #object of Movement
        move = self.getMove()

        # calculate the time elapsed
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        # for linear mobility with cubic spline
        # if move.getLinearMobilitySpFlag():

        if 0.0 <= passedTime < self._totalFlightTime :
        # if passedTime !=0 and passedTime < self._totalFlightTime :
            '''
            reduce computation by passing the following lines in constructor
            '''
            if passedTime !=0.0:
                spl_x = CubicSpline(self._waypointTime, self._waypointX)
                spl_y = CubicSpline(self._waypointTime, self._waypointY)
                spl_z = CubicSpline(self._waypointTime, self._waypointZ)

                nextCoordinate= Point(spl_x(passedTime), spl_y(passedTime), spl_z(passedTime))
                move.setNextCoordinate(nextCoordinate)
                if self._collisionAction != 2:
                    self.manageObstacles(spl_x,spl_y,spl_z, passedTime)

        elif passedTime>= self._totalFlightTime :
            move.setFinalFlag(True)
            # move.setLinearMobilitySpFlag(False)
            # move.setSpeed(0.0)


        move.setPassedTime(passedTime)
        super().makeMove()
        return True if self._obstacleDetector_flag and self._collisionAction==3 else False

    def updateWaypointsByIndex(self):

        waypointsIndex, waypointsX, waypointsY, waypointsZ = AirMobiSim.getWaypointsByIndex()

        if waypointsIndex != None:
            # print('hello hello')
            # time = list(self._waypointTime.copy())
            x = self._waypointX.copy()
            y = self._waypointY.copy()
            z = self._waypointZ.copy()
            x=[float(i) for i in x]   # type cast to float required by np.insert()
            y=[float(i) for i in y]
            z=[float(i) for i in z]

            for idx_new,x_new,y_new,z_new in zip(waypointsIndex,waypointsX,waypointsY,waypointsZ) :

                # print('vertex: ',v)
                # time.insert(v, (time[v] + time[v - 1]) / 2)
                x= np.insert(x,idx_new, x_new)
                y=np.insert(y,idx_new,y_new)
                z=np.insert(z,idx_new, z_new)


            self._waypointX = x
            self._waypointY = y
            self._waypointZ = z
            logging.debug('waypoint inserted')

    def insertWaypointTime(self):
        distance_of_segments= Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        total_spline_distance=np.sum(distance_of_segments)
        total_flight_time= total_spline_distance/self._speed

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

        return waypointTime

    @staticmethod         # this functions returns an area of segments for each waypoint segments
    def computeSplineDistance(waypointX,waypointY,waypointZ):
        waypointCount=len(waypointX)
        waypointIndex=np.linspace(0,waypointCount-1,num=waypointCount)

        spl_x = CubicSpline(waypointIndex, waypointX)
        spl_y = CubicSpline(waypointIndex, waypointY)
        spl_z = CubicSpline(waypointIndex, waypointZ)

        distance_of_segments=[]
        for i in range(waypointCount-1):
            number_of_small_segment=100

            segments_of_index=np.linspace(waypointIndex[i], waypointIndex[i + 1], number_of_small_segment)
            segments_small_x=spl_x(segments_of_index)
            segments_small_y=spl_y(segments_of_index)
            segments_small_z=spl_z(segments_of_index)

            segments_distance=0
            for i in range(number_of_small_segment-1):
                segments_distance += math.sqrt((segments_small_x[i+1] - segments_small_x[i])**2 +(segments_small_y[i+1] - segments_small_y[i])**2 + (segments_small_z[i+1] - segments_small_z[i])**2 )

            distance_of_segments.append(segments_distance)

        # print(np.sum(area_of_segment))

        return distance_of_segments

    def manageObstacles(self, spl_x, spl_y, spl_z, passedTime):
        if self._obstacle == None:
            return
        futureTime= passedTime + Simulationparameter.stepLength
        futureCoordinate = (spl_x(futureTime), spl_y(futureTime))
        # self._obstackelDetector_flag= self._obstacles[0].contains_point(futureCoordinate)
        # warnings.filterwarnings('once')
        detectObstacle = self._obstacle[0].contains_point(futureCoordinate)
        if not self._obstacleDetector_flag and detectObstacle and self._collisionAction==1:
            # warnings.warn('uav is going to collide in collide')
            logging.debug('WARNING!!!!')
            logging.debug("currentTime: %s; uav is going to collide at %s", str(passedTime), str(futureTime))


        self._obstacleDetector_flag= True if detectObstacle == True else self._obstacleDetector_flag



    def computeTotalFlightTime(self, currentTime, speed, acceleration):
        if speed==0 and acceleration==0:
            return 0
        distance = np.sum(Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ))
        final_velocity = math.sqrt(speed ** 2 + 2 * acceleration * distance)  # v^2=u^2+2as
        average_velocity = (speed + final_velocity) / 2
        assert average_velocity != 0, 'avarage velocity can not be 0'
        flightTime = distance / average_velocity + currentTime
        return flightTime
