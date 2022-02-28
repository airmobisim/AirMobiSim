import unittest
from src.yamlparser import Yamlparser
import airmobisim


class TestAirmobisim(unittest.TestCase):

    def test_input(self):
        p = Yamlparser("../examples/simpleSimulation/simulation.config")
        config = p.readConfig()
        print(config)

        simTimeLimit= config['simulation']['simTimeLimit']
        playgroundSizeX=config['simulation']['playgroundSizeX']
        playgroundSizeY=config['simulation']['playgroundSizeY']
        playgroundSizeZ=config['simulation']['playgroundSizeZ']
        uavsSpline=config['uavsp']

        speed = []
        waypointX = []
        waypointY = []
        waypointZ = []

        for uavsp in config['uavsp']:
            waypointX.append(uavsp['waypointX'])
            waypointY.append(uavsp['waypointY'])
            waypointZ.append(uavsp['waypointZ'])
            speed.append(uavsp['speed'])

        # validInputSp=True for equal len of x,y,z list
        validInputSp = len(waypointX) == len(waypointY) == len(waypointZ)

        for i,v in enumerate(waypointX):
            validInputSp=all(0 <= item <=playgroundSizeX for item in v)

        if validInputSp:
            for i, v in enumerate(waypointY):
                validInputSp = all(0 <= item <= playgroundSizeY for item in v)

        if validInputSp:
            for i, v in enumerate(waypointZ):
                validInputSp = all(0 <= item <= playgroundSizeZ for item in v)


        self.assertEqual(validInputSp,True)

