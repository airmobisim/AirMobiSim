#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from src.yamlparser import Yamlparser
from src.splinemobility import Splinemobility
import airmobisim
import os
from pathlib import Path
import pandas as pd


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

    def test_input_sp(self):   # all inputs need to be positive and inside the playground

        self.assertTrue(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ), 'input waypoint length for x,y and z should be same')

        for i,v in enumerate(TestAirmobisim.waypointX):      # use zip function correct it later on
            # validInputSp=all(0 <= item <=playgroundSizeX for item in v)
            self.assertTrue(len(TestAirmobisim.waypointX[i]) == len(TestAirmobisim.waypointY[i]) == len(TestAirmobisim.waypointZ[i]), 'waypoint x,y,z should be same for each uav')
            self.assertTrue(all(0 <= item <=TestAirmobisim.playgroundSizeX for item in TestAirmobisim.waypointX[i]), 'waypoint x should be within playgroundX')
            self.assertTrue(all(0 <= item <=TestAirmobisim.playgroundSizeY for item in TestAirmobisim.waypointY[i]), 'waypoint y should be within playgroundY')
            self.assertTrue(all(0 <= item <=TestAirmobisim.playgroundSizeZ for item in TestAirmobisim.waypointZ[i]), 'waypoint z should be within playgroundZ')

    def test_speed_limit_sp(self):
        for index,uavsp in enumerate(TestAirmobisim.uavsSpline):

            splineObj= Splinemobility(index,TestAirmobisim.speed[index],TestAirmobisim.waypointX[index],TestAirmobisim.waypointY[index],TestAirmobisim.waypointZ[index])
            print('total flight time')
            print(splineObj._totalFlightTime)
            self.assertTrue(splineObj._totalFlightTime<=TestAirmobisim.simTimeLimit, 'this speed will exceed the simTimeLimit consider reducing it')

    def test_all_waypoints_simulated(self):


        # run simulation sp
        self.run_simulator_sp()
        # get all uav_sp dataframe
        df_simulation_uavs = self.process_result_file()     # result dataframe for each uav
        # TestAirmobisim.waypointX[0].append(0.678822509939085)
        # TestAirmobisim.waypointY[0].append(0.678822509939085)
        # TestAirmobisim.waypointZ[0].append(3.0)
        for index, df_uav in enumerate(df_simulation_uavs):     # loop through each uav dataframe
            for x,y,z in zip(TestAirmobisim.waypointX[index],TestAirmobisim.waypointY[index],TestAirmobisim.waypointZ[index]): # loop through input waypoints for each uav
                # print(x)
                # print(y)
                # print(z)
                value= 0.1
                df_uav_conditional= df_uav.loc[(abs(df_uav['posX'] -x) <= value) & (abs(df_uav['posY']-y) <= value)  & (abs(df_uav['posZ']-z) <= value)] # search for rows with satisfied conditions
                self.assertFalse( df_uav_conditional.empty, 'data frame should not be empty/ no such waypoint is found')
                # print('testing')
                # print(df_uav_conditional)
                # print('end testing')

    def run_simulator_sp(self):
        config_path_abs = str(Path("../examples/simpleSimulation/simulation.config").resolve())

        os.system('../airmobisim.py --configuration ' + config_path_abs + ' --plot 0')

    def process_result_file(self):
        '''
        after running the simulation create seperate dataframe for each uid from resultant .csv file
        '''
        current_file = os.path.abspath(os.path.dirname(__file__))
        csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults.csv')

        df_simulation = pd.read_csv(csv_filename, sep=r'\t', skipinitialspace=True, engine='python')

        max_uav_index = max(df_simulation['uid'])

        df_simulation_uavs = []


        for index in range(max_uav_index + 1):

            df_simulation_uavs.append(df_simulation.loc[df_simulation['uid'] == index])

        return df_simulation_uavs

    def test_active_uav_count_sp(self):

        self.skipTest("not useful")


        '''
        number of spline uav active
        '''
        self.assertEqual(len(TestAirmobisim.uavsSpline),1, 'should be 1 check config')

    def test_simulation_finish_time(self):
        df_simulation_uavs = self.process_result_file()  # result dataframe for each uav

        for df_uav in df_simulation_uavs:

            df_uav_conditional = df_uav.loc[(df_uav['posZ'] == df_uav['posZ'].to_numpy()[-1]) &
                                             (df_uav['posY'] == df_uav['posY'].to_numpy()[-1]) &
                                             (df_uav['posX'] == df_uav['posX'].to_numpy()[-1]) ]  # search for rows which are similar as the last entry/ finish line


            self.assertTrue(df_uav_conditional['passedTime'].to_numpy()[0] <= TestAirmobisim.simTimeLimit, 'check simulation finish time')

    @patch('src.basemobility.Basemobility.doLog')
    def test_doLog_sp(self, mock_doLog):

        sp_obj = Splinemobility(0,TestAirmobisim.speed[0],TestAirmobisim.waypointX[0],TestAirmobisim.waypointY[0],TestAirmobisim.waypointZ[0])

        # ht.foo("some string")
        sp_obj.makeMove()
        # print(sp_obj.passedtime)
        self.assertTrue(mock_doLog.called)

    # self.assertEqual(validInputSp,True)
if __name__=='__main__':
    unittest.main()
