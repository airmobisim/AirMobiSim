import math
import geopandas
from shapely.geometry import Point
from .basemobility import Basemobility
from scipy.interpolate import CubicSpline

from .simulationparameter import Simulationparameter
from proto.DroCIBridge import AirMobiSim


class Splinemobility(Basemobility):
    def __init__(self, uid, startPos, endPos, totalFlightTime, waypointTime, waypointX, waypointY, waypointZ):
        super().__init__(uid, startPos, endPos)
        self._move.setStart(startPos, 0)
        self._move.setLastPos(endPos)
        self._move.setTempStartPos(startPos) # holds each intermediate points of linear in each iteration
        self._waypointTime = waypointTime
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ
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

        # for linear mobility with cubic spline
        if move.getLinearMobilitySpFlag():

            if 0.0 <= passedTime < self._totalFlightTime :
                '''
                reduce computation by passing the following lines in constructor
                '''

                spl_x = CubicSpline(self._waypointTime, self._waypointX)
                spl_y = CubicSpline(self._waypointTime, self._waypointY)
                spl_z = CubicSpline(self._waypointTime, self._waypointZ)

                # if move.getWaypointsInsertedFlag() == False:  # if waypoints is not inserted this this add the waypoints if already inserted then it will ignore
                #     move.setWaypointsInsertedFlag(True)
                #     # print(move.getWaypointsInsertedFlag())
                #     spl_x, spl_y = self.updateWaypointsByIndex()  # to insert way points
                #     # print("pritom")

                nextCoordinate= Point(spl_x(passedTime), spl_y(passedTime), spl_z(passedTime))
                move.setNextCoordinate(nextCoordinate)


                pass

            elif passedTime>= self._totalFlightTime :
                move.setFinalFlag(True)
                move.setLinearMobilitySpFlag(False)
                # move.setSpeed(0.0)



            pass
        move.setPassedTime(passedTime)
        super().makeMove()

    def updateWaypointsByIndex(self):
        waypointsIndex = [6, 7]
        waypointsX = [0.23, 0.21]
        waypointsY = [-0.2, -0.35]

        # waypointsIndex, waypointsX, waypointsY = AirMobiSim.getWaypointsByIndex()

        # print('hello hello')
        time = self._waypointTime.copy().tolist()
        x = self._waypointX.copy()
        y = self._waypointY.copy()
        # print(time)
        # print(x)
        # print(y)
        # print(len(time))
        # print(len(x))
        # print(len(y))

        for i, v in enumerate(waypointsIndex):
            print("print")
            if 1 <= v <= len(time) - 2:
                print(v)
                time.insert(v, (time[v] + time[v - 1]) / 2)
                x.insert(v, waypointsX[i])
                y.insert(v, waypointsY[i])
        # print('later')
        # print(len(time))
        # print(len(x))
        # print(len(y))
        # print(time)
        # print(x)
        # print(y)

        spl_x = CubicSpline(time, x)
        spl_y = CubicSpline(time, y)
        self._waypointTime = time
        self._waypointX = x
        self._waypointY = y

        return spl_x, spl_y



