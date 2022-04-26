import math

import geopandas
import numpy as np
import warnings
from shapely.geometry import Point
from .basemobility import Basemobility
from scipy.interpolate import CubicSpline
from xml.dom import minidom
import matplotlib.path as mplPath

from .simulationparameter import Simulationparameter
from proto.DroCIBridge import AirMobiSim



class Splinemobility(Basemobility):
    def __init__(self, uid, waypointX, waypointY, waypointZ, speed, polygon_file_path):
        self._startpos=Point(waypointX[0],waypointY[0],waypointZ[0])
        self._endpos=Point(waypointX[-1],waypointY[-1],waypointZ[-1])
        # self._totalFlightTime = waypointTime[-1]

        super().__init__(uid, self._startpos, self._endpos)
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ

        self._uid = uid
        self._move.setStart(self._startpos, 0)
        self._move.setEndPos(self._endpos)
        self._move.setTempStartPos(self._startpos) # holds each intermediate points of linear in each iteration

        # since spline so fixing it to true, this flag is used to separate some code from other mobility
        self._move.setLinearMobilitySpFlag(True)
        # self._waypointsInsertedFlag=True     # this decides calling of updateWaypointsByIndex()
        # self.updateWaypointsByIndex()     # uncomment this line when you want to use insertion of waypoints
        self._speed= speed
        self._waypointTime = self.insertWaypointTime()
        self._totalFlightTime = self._waypointTime[-1]
        self._polygon_file_path = polygon_file_path
        self._obstrackelDetector_flag = False
        self._collisionAction = 2  # 1= warn, 2 = no action 3=remove uav
        self._obstracles= self.ParsePolygonFileToObstracles()



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
                if self._collisionAction != 2:
                    self.manageObstracles(spl_x,spl_y,spl_z, passedTime)




            elif passedTime>= self._totalFlightTime :
                move.setFinalFlag(True)
                # move.setLinearMobilitySpFlag(False)
                # move.setSpeed(0.0)


        move.setPassedTime(passedTime)
        super().makeMove()
        return True if self._obstrackelDetector_flag and self._collisionAction==3 else False

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
            print('waypoint inserted')





    def insertWaypointTime(self):
        distance_of_segments= Splinemobility.computeSplineDistance(self._waypointX, self._waypointY, self._waypointZ)
        total_spline_distance=np.sum(distance_of_segments)
        total_flight_time= total_spline_distance/self._speed
        # print(' func insertWaypointTime total flight time')
        # print(total_flight_time)

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




    @staticmethod         # this functions returns area of segments for each waypoint segments
    def computeSplineDistance(waypointX,waypointY,waypointZ):
        waypointCount=len(waypointX)
        waypointIndex=np.linspace(0,waypointCount-1,num=waypointCount)

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

            segments_distance=0
            for i in range(number_of_small_segment-1):
                segments_distance += math.sqrt((segments_small_x[i+1] - segments_small_x[i])**2 +(segments_small_y[i+1] - segments_small_y[i])**2 + (segments_small_z[i+1] - segments_small_z[i])**2 )

            distance_of_segments.append(segments_distance)

        # print(np.sum(area_of_segment))


        return distance_of_segments


    def ParsePolygonFileToObstracles(self):
        parsedFile= minidom.parse(self._polygon_file_path)
        polygons = parsedFile.getElementsByTagName('poly')
        buildings=[]
        for polygon in polygons:
            shape_of_polygon = polygon.attributes['shape'].value
            vertex_corordinates= shape_of_polygon.split(' ')       #coordinates are of string type
            # print("hello")
            # print(vertex_corordinates)
            list_of_coordinates=[]
            for single_vertex in vertex_corordinates:
                list_of_coordinates.append([float(single_vertex.split(',')[0]),float(single_vertex.split(',')[1])]) # x and y coordinates are seperated and converted to float

            # print(list_of_coordinates)
            buildings.append(mplPath.Path(np.array(list_of_coordinates)))     # forming shape of polyson by joining the polygon coordinates and appended to building list

        return buildings


        # point = (8.9, 8)
        # print(point, " is in polygon: ", building[0].contains_point(point))
        # warnings.filterwarnings('error')
        # print(self.getMove().getPassedTime())
        # warnings.warn('prompt warning')
        # print(len(building))
        '''
        # ex= polys[0].attributes['shape'].value.split(' ')
        # print([float(ex[0].split(',')[0]),float(ex[0].split(',')[1])])
        # vertex_coordinate= [float(ex[0].split(',')[0]),float(ex[0].split(',')[1])]
        # print(type(vertex_coordinate[0]))
        # test_list= [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
        # poly_path = mplPath.Path(np.array(test_list))
        # print(poly_path)
        # point = (9.5, -10)
        # print(point, " is in polygon: ", poly_path.contains_point(point))
        '''


    def manageObstracles(self, spl_x, spl_y, spl_z, passedTime):
        futureTime= passedTime + Simulationparameter.stepLength
        futureCoordinate = (spl_x(futureTime), spl_y(futureTime))
        # self._obstrackelDetector_flag= self._obstracles[0].contains_point(futureCoordinate)
        # warnings.filterwarnings('once')
        detectObstrackel = self._obstracles[0].contains_point(futureCoordinate)
        if not self._obstrackelDetector_flag and detectObstrackel and self._collisionAction==1:
            # warnings.warn('uav is going to collide in collide')
            print('uav is going to collide to collide')
            print(passedTime)
            print(futureTime)

        self._obstrackelDetector_flag= True if detectObstrackel== True else self._obstrackelDetector_flag

        pass









