from .singleton import Singleton

import threading
import time

class Simulationparameter( metaclass=Singleton):
    currentSimStep = -1
    stepLength = -1
    directory = "../examples/simpleSimulation"
    
    def incrementCurrentSimStep():
        Simulationparameter.currentSimStep += 1

    def current_milli_time():
        return round(time.time() * 1000)