#!/usr/bin/env python3
import unittest
from src.yamlparser import Yamlparser
import airmobisim


class TestAirmobisim(unittest.TestCase):

    def test_input(self):
        p = Yamlparser("../examples/simpleSimulation/simulation.config")
        config = p.readConfig()
        # print(config)

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


        self.assertEqual(len(waypointX) == len(waypointY) == len(waypointZ), True)

        for i,v in enumerate(waypointX):
            # validInputSp=all(0 <= item <=playgroundSizeX for item in v)
            self.assertEqual(len(waypointX[i]) == len(waypointY[i]) == len(waypointZ[i]), True)
            self.assertEqual(all(0 <= item <=playgroundSizeX for item in waypointX[i]), True)
            self.assertEqual(all(0 <= item <=playgroundSizeY for item in waypointY[i]), True)
            self.assertEqual(all(0 <= item <=playgroundSizeZ for item in waypointZ[i]), True)




        # self.assertEqual(validInputSp,True)
if __name__=='__main__':
    unittest.main()
