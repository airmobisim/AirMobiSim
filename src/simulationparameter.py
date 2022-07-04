from .singleton import Singleton

import time

class Simulationparameter( metaclass=Singleton):
    currentSimStep = -1
    stepLength = -1
    
    def incrementCurrentSimStep():
        Simulationparameter.currentSimStep += 1

    def current_milli_time():
        return round(time.time() * 1000)