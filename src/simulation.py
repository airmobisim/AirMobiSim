import pathlib

from shapely.geometry import Point

import sys

from .uav import Uav
from .simulationparameter import Simulationparameter
from .repeatedtimer import Repeatedtimer
from .uavsp import UavSp


class Simulation:
    _currentTime = 0
    _isRunnig = False
    _managedNodes = []
    _startUavs = []
    _highestUid = -1

    def __init__(self, directory, stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ,
                 linearMobilityFlag, splineMobilityFlag, uavs, polygon_file_path=None, speed=None, waypointX=None, waypointY=None,
                 waypointZ=None):

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
        self._speed = speed
        self._waypointX = waypointX
        self._waypointY = waypointY
        self._waypointZ = waypointZ
        self._linearMobilityFlag = linearMobilityFlag
        self._splineMobilityFlag = splineMobilityFlag
        self._polygon_file_path= polygon_file_path
        
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
            # print(type(self.getNextUid()))
            nextUid = self.getNextUid()
            # for spline mobility
            if self._splineMobilityFlag:
                self._managedNodes.append(
                    UavSp(nextUid, self._waypointX[nextUid],
                        self._waypointY[nextUid], self._waypointZ[nextUid], self._speed[nextUid], self._polygon_file_path))

            # for linearmobility
            else:
                self._managedNodes.append(Uav(nextUid, Point(uav['startPosX'], uav['startPosY'], uav['startPosZ']),
                                              Point(uav['endPosX'], uav['endPosY'], uav['endPosZ']), self._polygon_file_path))


    def processNextStep(self):
        Simulationparameter.incrementCurrentSimStep()
        if self._splineMobilityFlag:
            for node in self._managedNodes:
                removeNode = node._mobility.makeMove()   # building ahead
                if removeNode:
                    print('removing uav', node._uid)
                    self._managedNodes.remove(node)      # obstacle so remove

        else:
            for node in self._managedNodes:
                removeNode = node._mobility.makeMove()
                if removeNode:
                    print('removing uav', node._uid, flush=True)
                    self._managedNodes.remove(node)

    def finishSimulation(self):
        print(
            "exiting -- at t=" + str(Simulationparameter.currentSimStep * Simulationparameter.stepLength) + ", event ?")

    def getNextUid(self):
        self._highestUid += 1
        return self._highestUid

    def getManagedNodes(self):
        return self._managedNodes

    # alternative constructors:

    @classmethod  # for spline mobility
    def from_config_spmob(cls, config, linearMobilityFlag, splineMobilityFlag, directory):
        speed = []
        waypointX = []
        waypointY = []
        waypointZ = []
        uavs = config['uavsp']

        for uavsp in config['uavsp']:
            waypointX.append(uavsp['waypointX'])
            waypointY.append(uavsp['waypointY'])
            waypointZ.append(uavsp['waypointZ'])
            speed.append(uavsp['speed'])

        polygon_file= config['files']['polygon']
        polygon_file_path= str(pathlib.Path().resolve())+'/'+polygon_file
        # print(poly_file_path)
        # print(pathlib.Path().resolve().parent)

        stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ = Simulation.load_common_parameters_from_config(
            config)

        return cls(directory, stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ,
                   linearMobilityFlag, splineMobilityFlag, uavs, polygon_file_path, speed, waypointX, waypointY, waypointZ)

    @classmethod  # for linear mobility
    def from_config_linmob(cls, config, linearMobilityFlag, splineMobilityFlag, directory):
        polygon_file = config['files']['polygon']
        polygon_file_path = str(pathlib.Path().resolve()) + '/' + polygon_file

        uavs = config['uav']
        stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ = Simulation.load_common_parameters_from_config(
            config)
        return cls(directory, stepLength, simTimeLimit, playgroundSizeX, playgroundSizeY, playgroundSizeZ,
                   linearMobilityFlag, splineMobilityFlag, uavs, polygon_file_path)

    @staticmethod  # load data from config file
    def load_common_parameters_from_config(config):

        return config['simulation']['stepLength'], config['simulation']['simTimeLimit'], \
               config['simulation']['playgroundSizeX'], config['simulation']['playgroundSizeY'], \
               config['simulation']['playgroundSizeZ']
