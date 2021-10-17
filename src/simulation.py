import geopandas
from shapely.geometry import Point
import threading
import time
import sys

from .uav import Uav
from .simulationparameter import Simulationparameter
from .repeatedtimer import Repeatedtimer


class Simulation:
    _currentTime = 0
    _isRunnig = False
    _managedNodes = []
    _startUavs = []
    _highestUid = -1

    def __init__(self, stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ,
                 uavs, uavStartPos, uavEndPos, totalFlightTime, waypointTime, waypointX, waypointY,
                 directory):

        print("Initializing...")
        Simulationparameter.stepLength = stepLength
        Simulationparameter.directory = directory
        Simulationparameter.simStartTime = Simulationparameter.current_milli_time()
        Simulationparameter.simTimeLimit = simTimeLimit
        self._playgroundSizeX = playgroundSizeX
        self._playgroundSizeY = playgroundSizeY
        self._playgroundSizeZ = playgroundSizeZ
        self._simulationSteps = simTimeLimit / Simulationparameter.stepLength
        self._startUavs = uavs
        self._uavStartPos = uavStartPos
        self._uavEndPos = uavEndPos
        self._totalFlightTime = totalFlightTime
        self._waypointTime = waypointTime
        self._waypointX = waypointX
        self._waypointY = waypointY

    def startSimulation(self):
        if self._isRunnig == True or Simulationparameter.currentSimStep != -1:
            print("Simulation is already running")
            sys.exit()

        self._isRunnig = True
        self.initializeNodes()
        self.manageSimulation()

    @staticmethod
    def printStatus():
        t = Simulationparameter.currentSimStep * Simulationparameter.stepLength

        elapsed = (Simulationparameter.current_milli_time() - Simulationparameter.simStartTime) / 1000
        p = 100 / Simulationparameter.simTimeLimit * t
        print("t=" + str(t) + "   Elapsed: " + str(elapsed) + "  " + str(p) + "% completed\n" +
              "Speed: simsec/sec=72.8271")

    def manageSimulation(self):
        rt = Repeatedtimer(1, self.printStatus, "World")
        while Simulationparameter.currentSimStep < self._simulationSteps:
            self.processNextStep()
        rt.stop()
        self.finishSimulation()

    def initializeNodes(self):
        for uav in self._startUavs:
            self._managedNodes.append(
                Uav(self.getNextUid(), self._uavStartPos, self._uavEndPos, self._totalFlightTime, self._waypointTime, self._waypointX, self._waypointY))

    def processNextStep(self):
        Simulationparameter.incrementCurrentSimStep()

        for node in self._managedNodes:
            node._mobility.makeMove()

    def finishSimulation(self):
        print(
            "exiting -- at t=" + str(Simulationparameter.currentSimStep * Simulationparameter.stepLength) + ", event ?")

    def getNextUid(self):
        self._highestUid += 1
        return self._highestUid

    def getManagedNodes(self):
        return self._managedNodes