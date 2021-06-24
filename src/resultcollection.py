from .singleton import Singleton

class Resultcollection( metaclass=Singleton):
    _logDelimiter = ';'
    _firstLog = True
    def __init__(self):
        self._firstLog = True
        self._logDelimiter = ';'    
    def logCurrentPosition(self,uid,position):
        if self._firstLog:
            print("creating new log")
            f = open("positionResults.csv", "w")
            f.write("uid" + self._logDelimiter + "posX" + self._logDelimiter + "posY" + self._logDelimiter + "posZ")
            self._firstLog = False
        f = open("positionResults.csv", "a")
#        f.write(str(uid) + self._logDelimiter + str(position.x)+ self._logDelimiter + str(position.y) + self._logDelimiter + str(position.z)+"\n")
        f.close()
       


