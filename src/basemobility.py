from abc import ABC
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
    def __init__(self, uid,  startPos, endPos, polygon_file_path):
        self._uid = uid
        self._move = Movement()
        self._resultcollection =  Resultcollection()
        self._baseenergy = Baseenergy()
        self._startPos = startPos
        self._endPos = endPos
        self._currentPos = Point(0,0,0) 
        self._collisionAction = 1  # 1= warn, 2 = no action 3=remove uav
        self._obstacleDetector_flag = False
        self.polygon_file_path = polygon_file_path
        self._obstacle = self.ParsePolygonFileToObstacles()
        pass

    def getMove(self):
        return self._move

    def getCurrentPos(self):
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        if passedTime==0.0:
            return self._startPos
        else:
            currentDirection = self.getMove().getCurrentDirection()

            previousPos = self.getMove().getTempStartPos()

            if self.getMove().getFinalFlag():
                return previousPos

            x = previousPos.x + (currentDirection.x*self.getMove().getSpeed()*Simulationparameter.stepLength)
            y = previousPos.y + (currentDirection.y*self.getMove().getSpeed()*Simulationparameter.stepLength)
            z = previousPos.z + (currentDirection.z*self.getMove().getSpeed()*Simulationparameter.stepLength)
            currentPos = Point(x,y,z)
            self.getMove().setTempStartPos(currentPos)
        
            return currentPos

    # current position function for spline mobility
    def getCurrentPosSp(self):
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        if passedTime==0:
            return self._startPos
        
        if not self.getMove().getFinalFlag():
            currentPos = self.getMove().getNextCoordinate()
            return currentPos

        elif self.getMove().getFinalFlag():
            currentPos = self.getMove().getNextCoordinate()

        return currentPos

    def makeMove(self):
        self.doLog()

    def doLog(self):
        if self.getMove().getLinearMobilitySpFlag():   # log for spline mobility
            self._resultcollection.logCurrentPosition(self._uid, self.getCurrentPosSp(), self.getMove())

        else:   # log for linear mobility
            self._resultcollection.logCurrentPosition(self._uid, self.getCurrentPos(), self.getMove())
        currentEnergy = self._baseenergy.getcurrentEnergy(self.getMove().getSpeed(), (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime())

        self._resultcollection.logCurrentEnergy(self._uid,currentEnergy[0], currentEnergy[1])
        pass

    def ParsePolygonFileToObstacles(self):
        if self.polygon_file_path == None or not os.path.exists(self.polygon_file_path):
            return None
        logWrapper.debug(("self.polygon_file_path: %s", str(self.polygon_file_path)))
        parsedFile= minidom.parse(self.polygon_file_path)
        polygons = parsedFile.getElementsByTagName('poly')
        buildings=[]
        for polygon in polygons:
            shape_of_polygon = polygon.attributes['shape'].value
            vertex_corordinates= shape_of_polygon.split(' ')       #coordinates are of string type
            list_of_coordinates=[]
            for single_vertex in vertex_corordinates:
                list_of_coordinates.append([float(single_vertex.split(',')[0]),float(single_vertex.split(',')[1])]) # x and y coordinates are seperated and converted to float

            buildings.append(mplPath.Path(np.array(list_of_coordinates)))     # forming shape of polygon by joining the polygon coordinates and appended to building list

        return buildings

    def manageObstacles(self):
        raise NotImplementedError
