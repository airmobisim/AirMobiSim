import math
from xml.dom import minidom
import matplotlib.path as mplPath
import numpy as np

import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility

from .simulationparameter import Simulationparameter

class Linearmobility(Basemobility):
    def __init__(self, uid, angle, startPos, endPos, polygon_file_path):
        super().__init__(uid, startPos, endPos)
        self._angle = angle
        self._acceleration = 0
        self._move.setStart(startPos, 0)
        self._move.setEndPos(endPos)
        self._move.setTempStartPos(startPos)

        self._move.setSpeed(0.8)
        self._uid = uid
        self._stepTarget = ""
        self._totalFlightTime= self.computeTotalFlightTime()
        # for pilygon detection
        self._polygon_file_path = polygon_file_path
        self._obstrackelDetector_flag = False
        self._collisionAction = 1  # 1= warn, 2 = no action 3=remove uav
        self._obstracles = self.ParsePolygonFileToObstracles()

    def makeMove(self):
        move = self.getMove()
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()

        if 0.0 <= passedTime < self._totalFlightTime:
            move.setDirectionByTarget()
            newSpeed = move.getSpeed() + self._acceleration * Simulationparameter.stepLength



        elif passedTime>= self._totalFlightTime:
            newSpeed=0.0
            self._acceleration=0.0
            self.getMove().setFinalFlag(True)
         
        move.setSpeed(newSpeed)
        move.setPassedTime(passedTime)
        super().makeMove()

        if passedTime < self._totalFlightTime:
            if self._collisionAction != 2:
                self.manageObstracles( passedTime)

        return True if self._obstrackelDetector_flag and self._collisionAction == 3 else False   # obstacle->remove/not remove node indicator


    def computeTotalFlightTime(self):
        distance = math.sqrt((self._endPos.x - self._startPos.x) ** 2 + (self._endPos.y - self._startPos.y) ** 2 + (
                    self._endPos.z - self._startPos.z) ** 2)
        final_velocity = math.sqrt(self.getMove().getSpeed()**2 + 2*self._acceleration*distance) # v^2=u^2+2as
        average_velocity= (self.getMove().getSpeed()+final_velocity)/2
        assert average_velocity !=0, 'avarage velocity can not be 0'
        return distance/average_velocity

    # form buildings  list from polygon life
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


    def manageObstracles(self, passedTime):
        futureTime= passedTime + Simulationparameter.stepLength

        currentDirection = self.getMove().getCurrentDirection()
        previousPos = self.getMove().getTempStartPos()
        x = previousPos.x + (currentDirection.x * self.getMove().getSpeed() * Simulationparameter.stepLength)
        y = previousPos.y + (currentDirection.y * self.getMove().getSpeed() * Simulationparameter.stepLength)
        # z = previousPos.z + (currentDirection.z * self.getMove().getSpeed() * Simulationparameter.stepLength) # no need since building height not given

        futureCoordinate = (x, y)


        # self._obstrackelDetector_flag= self._obstracles[0].contains_point(futureCoordinate)
        # warnings.filterwarnings('once')
        detectObstrackel = self._obstracles[0].contains_point(futureCoordinate)
        if not self._obstrackelDetector_flag and detectObstrackel and self._collisionAction==1:
            # warnings.warn('uav is going to collide in collide')
            print('WARNING!!!!')
            print('currentTime:',passedTime,'uav is going to collide at ', futureTime)

        self._obstrackelDetector_flag= True if detectObstrackel== True else self._obstrackelDetector_flag

