import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os.path

from .singleton import Singleton
from .simulationparameter import Simulationparameter

class Resultcollection(metaclass=Singleton):

    def __init__(self):
        self._firstLog = True
        self._logDelimiter = '\t'
        self._logDir = str(Simulationparameter.directory) + "/results/"
        if not os.path.exists(self._logDir):
            os.makedirs(self._logDir)

    def logCurrentPosition(self,uid,position):
        """
        Log current position
        """
        logfile = self._logDir + "positionResults.csv"
        if self._firstLog:
            print("creating new log")
            f = open(logfile, "w")
            f.write("uid" + self._logDelimiter + "posX" + self._logDelimiter + "posY" + self._logDelimiter + "posZ"+"\n")
            #self._firstLog = False
        f = open(logfile, "a")
        f.write(str(uid) + self._logDelimiter + str(position.x)+ self._logDelimiter + str(position.y) + self._logDelimiter + str(position.z)+"\n")
        f.close()


    def logCurrentEnergy(self,uid,distance, energy):
        """
        Log current energy
        """
        logfile_2 = self._logDir + "energyResults.csv"
        if self._firstLog:
            fl = open(logfile_2, "w")
            fl.write("uid" + self._logDelimiter + "travelled distance" + self._logDelimiter + "energy"+ "\n")
            self._firstLog = False
        fl = open(logfile_2, "a")
        fl.write(str(uid) + self._logDelimiter + str(distance) + self._logDelimiter + str(energy) + "\n")
        fl.close()

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
            print("There is no such file called 'energyResults.csv'")




        
        

        
       



