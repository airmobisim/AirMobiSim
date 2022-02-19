import math
import geopandas
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
        # since spline so fixing it to true
        self._move.setLinearMobilitySpFlag(True)
        # self._totalFlightTime= totalFlightTime

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



