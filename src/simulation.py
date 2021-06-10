
class Simulation:
    _currentTime = 0
    _currentSimStep = -1
    _isRunnig = False
    def __init__(self, stepLength,simTimeLimit,playgroundSizeX,playgroundSizeY,playgroundSizeZ):
        print("Initializing...")
        self._stepLength = stepLength
        self._simTimeLimit = simTimeLimit
        self._playgroundSizeX = playgroundSizeX
        self._playgroundSizeY = playgroundSizeY
        self._playgroundSizeZ = playgroundSizeZ 
        self._simulationSteps = simTimeLimit / stepLength

    @property
    def currentSimStep(self) -> float:
        return self._currentSimStep


    def startSimulation(self):
        if self._isRunnig == True or self._currentSimStep != -1:
            print("Simulation is already running")
            sys.exit()

        self._isRunnig = True
        self.processNextStep()

    def processNextStep(self):
        self._currentSimStep += 1
        print("Processing " + str(self._currentSimStep))
        if self._currentSimStep == self._simulationSteps:
            self.finishSimulation()
        else:
            self.processNextStep()
    
    def finishSimulation(self):
        print("exiting -- at t=" + str(self._currentSimStep * self._stepLength) + ", event ?")
