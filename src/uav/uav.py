from src.uav.app.simpleapp import Simpleapp
from src.uav.missioncontrol.simplemissioncontrol import Simplemissioncontrol 
from src.uav.mobility.simplemobility import Simplemobility
from src.uav.mobility.linearmobility import Linearmobility
class Uav:
    def __init__(self):
        self.mobility = Linearmobility
        pass

    def getMobility():
        return self.mobility

    def logPosition():
        pass 

