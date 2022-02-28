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

        validInputSp=True

        for i,v in enumerate(waypointX):
            # print(waypointX)
            # print(item)
            for item in v:
                if item<0 or item>playgroundSizeX:
                    validInputSp=False

        # print('hello')

        #if validInputSp:
           # validInputSp= all((0 <= element <= playgroundSizeX)  for element in waypointX)

        if validInputSp:
            for i, v in enumerate(waypointY):
                # print(waypointX)
                # print(item)
                for item in v:
                    if item < 0 or item > playgroundSizeY:
                        validInputSp = False

        if validInputSp:
            for i, v in enumerate(waypointZ):
                # print(waypointZ)
                # print(item)
                for item in v:
                    if item < 0 or item > playgroundSizeZ:
                        validInputSp = False

        self.assertEqual(validInputSp,True)

    pass