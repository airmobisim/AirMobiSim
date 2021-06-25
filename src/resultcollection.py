import os

from .singleton import Singleton
from .simulationparameter import Simulationparameter

class Resultcollection( metaclass=Singleton):

    def __init__(self):
        self._firstLog = True
        self._logDelimiter = '\t'
        self._logDir = str(Simulationparameter.directory) + "/results/"
        if not os.path.exists(self._logDir):
            os.makedirs(self._logDir)
    def logCurrentPosition(self,uid,position):
        logfile = self._logDir + "positionResults.csv"
        if self._firstLog:
            print("creating new log")
            f = open(logfile, "w")
            f.write("uid" + self._logDelimiter + "posX" + self._logDelimiter + "posY" + self._logDelimiter + "posZ"+"\n")
            self._firstLog = False
        f = open(logfile, "a")
        f.write(str(uid) + self._logDelimiter + str(position.x)+ self._logDelimiter + str(position.y) + self._logDelimiter + str(position.z)+"\n")
        f.close()
       


