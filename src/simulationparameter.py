from .singleton import Singleton

class Simulationparameter( metaclass=Singleton):
    currentSimStep = -1
    stepLength = -1

    def __init__(self, parStepLength):
        stepLength = parStepLength
    
    def incrementCurrentSimStep():
        Simulationparameter.currentSimStep += 1
