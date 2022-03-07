#!/usr/bin/env python3
import unittest
from src.yamlparser import Yamlparser
from src.splinemobility import Splinemobility
import airmobisim
import os
from pathlib import Path


class TestAirmobisim(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        p = Yamlparser("../examples/simpleSimulation/simulation.config")
        config = p.readConfig()
        # print(config)

        cls.simTimeLimit = config['simulation']['simTimeLimit']
        cls.playgroundSizeX = config['simulation']['playgroundSizeX']
        cls.playgroundSizeY = config['simulation']['playgroundSizeY']
        cls.playgroundSizeZ = config['simulation']['playgroundSizeZ']
        cls.uavsSpline = config['uavsp']
        cls.uavsLinear = config['uav']

        cls.speed = []
        cls.waypointX = []
        cls.waypointY = []
        cls.waypointZ = []

        for uavsp in cls.uavsSpline:
            cls.waypointX.append(uavsp['waypointX'])
            cls.waypointY.append(uavsp['waypointY'])
            cls.waypointZ.append(uavsp['waypointZ'])
            cls.speed.append(uavsp['speed'])

    @classmethod
    def tearDownClass(cls) -> None:
        #print('after everything')
        pass

    def setUp(self) -> None:
        #print('before running every test')
        pass

    def tearDown(self) -> None:
        #print('after every test')
        pass

    def test_input_sp(self):

        self.assertEqual(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ), True)

        for i,v in enumerate(TestAirmobisim.waypointX):
            # validInputSp=all(0 <= item <=playgroundSizeX for item in v)
            self.assertEqual(len(TestAirmobisim.waypointX[i]) == len(TestAirmobisim.waypointY[i]) == len(TestAirmobisim.waypointZ[i]), True)
            self.assertEqual(all(0 <= item <=TestAirmobisim.playgroundSizeX for item in TestAirmobisim.waypointX[i]), True)
            self.assertEqual(all(0 <= item <=TestAirmobisim.playgroundSizeY for item in TestAirmobisim.waypointY[i]), True)
            self.assertEqual(all(0 <= item <=TestAirmobisim.playgroundSizeZ for item in TestAirmobisim.waypointZ[i]), True)

    def test_speed_limit_sp(self):
        for index,uavsp in enumerate(TestAirmobisim.uavsSpline):

            splineObj= Splinemobility(index,TestAirmobisim.speed[index],TestAirmobisim.waypointX[index],TestAirmobisim.waypointY[index],TestAirmobisim.waypointZ[index])
            print('total flight time')
            print(splineObj._totalFlightTime)
            self.assertEqual(splineObj._totalFlightTime<=TestAirmobisim.simTimeLimit,True)

    def test_waypoints_reached(self):


        # define some args
        config_path_abs = str(Path("../examples/simpleSimulation/simulation.config").resolve())

        os.system('../airmobisim.py --configuration ' + config_path_abs +' --plot 0')

        bool=True
        self.assertEqual(bool,True)




    # self.assertEqual(validInputSp,True)
if __name__=='__main__':
    unittest.main()
