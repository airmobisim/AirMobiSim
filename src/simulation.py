import geopandas
from shapely.geometry import Point
import threading
import time

from .uav import Uav
from .simulationparameter import Simulationparameter
from .repeatedtimer import Repeatedtimer


class Simulation:
    _currentTime = 0
    _isRunnig = False
    _managedNodes = []
    _startUavs = []
    _highestUid = -1

    def __init__(self, stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ, uavs, directory):
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
              "Speed:     simsec/sec=72.8271   ")

    def manageSimulation(self):
        rt = Repeatedtimer(1, self.printStatus, "World")
        while Simulationparameter.currentSimStep < self._simulationSteps:
            self.processNextStep()
        rt.stop()
        self.finishSimulation()

    def initializeNodes(self):
        len(self._startUavs)
        for uav in self._startUavs:
            self._managedNodes.append(
                Uav(self.getNextUid(), Point(uav['startPosX'], uav['startPosY'], uav['startPosZ']),
                    Point(uav['endPosX'], uav['endPosY'], uav['endPosZ'])))

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
