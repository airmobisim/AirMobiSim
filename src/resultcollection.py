import os
import matplotlib.pyplot as plt
import pandas as pd

import os.path

from .singleton import Singleton
from .simulationparameter import Simulationparameter

import src.logWrapper as logWrapper

class Resultcollection(metaclass=Singleton):

    def __init__(self):
        self._firstLog = True
        self._logDelimiter = '\t'
        self._logDir = str(Simulationparameter.directory) + "/results/"
        if not os.path.exists(self._logDir):
            os.makedirs(self._logDir)

    def logCurrentPosition(self,uid,position, movement):
        """
        Log current position
        """
        logfile = self._logDir + "positionResults.csv"
        if self._firstLog:
            logWrapper.info("creating new log")
            with open(logfile, "w") as f:
                f.write("uid" + self._logDelimiter + "passedTime" + self._logDelimiter + "posX" + self._logDelimiter + "posY" + self._logDelimiter + "posZ"+"\n")
            # f.close()
            #self._firstLog = False

        with open(logfile, "a") as f:
            f.write(str(uid) + self._logDelimiter + str(movement.getPassedTime()) + self._logDelimiter + str(
                position.x) + self._logDelimiter + str(position.y) + self._logDelimiter + str(position.z) + "\n")
            # f.close()


    def logCurrentEnergy(self,uid,distance, energy):
        """
        Log current energy
        """
        logfile_2 = self._logDir + "energyResults.csv"
        if self._firstLog:
            with open(logfile_2, "w") as fl:
                fl.write("uid" + self._logDelimiter + "travelled distance" + self._logDelimiter + "energy"+ "\n")
            self._firstLog = False

        with open(logfile_2, "a") as fl:
            fl.write(str(uid) + self._logDelimiter + str(distance) + self._logDelimiter + str(energy) + "\n")
            # fl.close()

    def showEnergy(self):
        """
            Show the data of the energy as a plot
        """
        if os.path.isfile(self._logDir + "energyResults.csv"):
            energyData = pd.read_csv(self._logDir + "energyResults.csv", sep=self._logDelimiter)
            energyData.set_index("travelled distance", inplace=True)
            energyData.groupby("uid")["energy"].plot(legend=True, xlabel="Distance (m)", ylabel= "Energy (Joules)")
            plt.show()
        else:
            logWrapper.error("There is no such file called 'energyResults.csv'")
