import geopandas
from shapely.geometry import Point

from .uav import Uav
from .simulationparameter import Simulationparameter

class Simulation:
    _currentTime = 0
    _isRunnig = False
    _managedNodes = []
    _startUavs = []
    _highestUid = -1
    def __init__(self, stepLength,simTimeLimit,playgroundSizeX,playgroundSizeY,playgroundSizeZ,uavs):
        print("Initializing...")
        Simulationparameter.stepLength = stepLength
        self._simTimeLimit = simTimeLimit
        self._playgroundSizeX = playgroundSizeX
        self._playgroundSizeY = playgroundSizeY
        self._playgroundSizeZ = playgroundSizeZ 
        self._simulationSteps = simTimeLimit / Simulationparameter.stepLength
        self._startUavs = uavs
    #@property
    #def currentSimStep(self) -> float:
    #    return self._currentSimStep


    def startSimulation(self):
        if self._isRunnig == True or Simulationparameter.currentSimStep != -1:
            print("Simulation is already running")
            sys.exit()
        
        self._isRunnig = True
        self.initializeNodes()
        self.processNextStep()
    def initializeNodes(self):
        len(self._startUavs) 
        for uav in self._startUavs:
            self._managedNodes.append(Uav(self.getNextUid(), Point(uav['startPosX'], uav['startPosY'], uav['startPosZ']), Point(uav['endPosX'], uav['endPosY'], uav['endPosZ'])))

    def processNextStep(self):
        Simulationparameter.incrementCurrentSimStep()
        #print("Processing step " + str(self._currentSimStep))
        if Simulationparameter.currentSimStep == self._simulationSteps:
            self.finishSimulation()
        else:
            for node in self._managedNodes:
                node._mobility.makeMove()
            self.processNextStep()
    
    def finishSimulation(self):
        print("exiting -- at t=" + str(Simulationparameter.currentSimStep * Simulationparameter.stepLength) + ", event ?")
    def getNextUid(self):
        self._highestUid += 1
        return self._highestUid 
