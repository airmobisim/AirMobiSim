import math
import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility
from scipy.interpolate import CubicSpline

from .simulationparameter import Simulationparameter


class Splinemobility(Basemobility):
    def __init__(self, uid, startPos, endPos, totalFlightTime, waypointTime, waypointX, waypointY):
        super().__init__(uid, startPos, endPos)
        self._move.setStart(startPos, 0)
        self._move.setLastPos(endPos)
        self._move.setTempStartPos(startPos) # holds each intermediate points of linear in each iteration
        self._waypointTime=waypointTime
        self._waypointX=waypointX
        self._waypointY=waypointY
        self._uid = uid
        self._totalFlightTime=totalFlightTime
        # only for testing spline mobility fixing to true
        self._move.setLinearMobilitySpFlag(True)
        self._totalFlightTime= totalFlightTime

    def makeMove(self):
        #object of Movement
        move = self.getMove()

        # calculate the time elapsed
        passedTime = (Simulationparameter.currentSimStep * Simulationparameter.stepLength) - self.getMove().getStartTime()
        # print('mike testing ')
        # for linear mobility with cubic spline
        if move.getLinearMobilitySpFlag():
            # print('yooooooooooo')


            if 0.0<= passedTime < self._totalFlightTime :
                spl_x = CubicSpline(self._waypointTime, self._waypointX)
                spl_y = CubicSpline(self._waypointTime, self._waypointY)
                nextCoordinate= Point(spl_x(passedTime), spl_y(passedTime), move.getStartPos().z)
                move.setNextCoordinate(nextCoordinate)

                # print('bara')
                pass

            elif passedTime>= self._totalFlightTime :
                move.setFinalFlag(True)
                move.getLinearMobilitySpFlag()
                # move.setSpeed(0.0)


            # print("jabara goal")
            pass
        move.setPassedTime(passedTime)
        super().makeMove()



