#!/usr/bin/env python3
import math
import pathlib
import unittest
from unittest.mock import patch, Mock, MagicMock

from shapely.geometry import Point

import src.basemobility
from src.linearmobility import Linearmobility
from src.yamlparser import Yamlparser
from src.splinemobility import Splinemobility
from src.simulationparameter import Simulationparameter

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
        polygon_file = config['files']['polygon']
        homePath = os.environ['AIRMOBISIMHOME']
        polygon_file_path = homePath + '/' + polygon_file
        print(polygon_file_path)

        cls.simTimeLimit = config['simulation']['simTimeLimit']
        cls.stepLength = config['simulation']['stepLength']
        cls.playgroundSizeX = config['simulation']['playgroundSizeX']
        cls.playgroundSizeY = config['simulation']['playgroundSizeY']
        cls.playgroundSizeZ = config['simulation']['playgroundSizeZ']
        cls.uavsSpline = config['uavsp']
        cls.uavsLinear = config['uav']
        cls.kenetic_model = config['kinetic_model']

        # inputs for splinemobility
        cls.speed_sp = []
        cls.waypointX = []
        cls.waypointY = []
        cls.waypointZ = []

        for uavsp in cls.uavsSpline:
            cls.waypointX.append(uavsp['waypointX'])
            cls.waypointY.append(uavsp['waypointY'])
            cls.waypointZ.append(uavsp['waypointZ'])
            cls.speed_sp.append(uavsp['speed'])

        # inputs for linear mobility
        cls.startPos = []
        cls.endPos = []
        cls.speed_lin = []

        for uavlin in cls.uavsLinear:
            # print(uavlin['startPosX'])
            cls.startPos.append(Point(uavlin['startPosX'], uavlin['startPosY'], uavlin['startPosZ']))
            cls.endPos.append(Point(uavlin['endPosX'], uavlin['endPosY'], uavlin['endPosZ']))
            cls.speed_lin.append(uavlin['speed'])

        # print('hello')
        # print(cls.startPos[0])

    @classmethod
    def tearDownClass(cls) -> None:
        # print('after everything')
        pass

    def setUp(self) -> None:
        # print('before running every test')
        step = TestAirmobisim.stepLength
        pass

    def tearDown(self) -> None:
        # print('after every test')
        pass

    def test_waypoints_spline_mob(self):  # all inputs need to be positive and inside the playground

        self.assertTrue(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ),
                        'input waypoint length for x,y and z should be same')

        for i, v in enumerate(TestAirmobisim.waypointX):  # use zip function correct it later on
            # validInputSp=all(0 <= item <=playgroundSizeX for item in v)
            self.assertTrue(len(TestAirmobisim.waypointX[i]) == len(TestAirmobisim.waypointY[i]) == len(
                TestAirmobisim.waypointZ[i]), 'waypoint x,y,z should be same for each uav')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeX for item in TestAirmobisim.waypointX[i]),
                            'waypoint x should be within playgroundX')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeY for item in TestAirmobisim.waypointY[i]),
                            'waypoint y should be within playgroundY')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeZ for item in TestAirmobisim.waypointZ[i]),
                            'waypoint z should be within playgroundZ')

    def test_waypoints_linear_mob(self):  # all inputs need to be positive and inside the playground

        self.assertTrue(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ),
                        'input waypoint length for x,y and z should be same')
        # print(TestAirmobisim.startPos[0])
        # print(TestAirmobisim.endPos[0])
        for startpos, endpos in zip(TestAirmobisim.startPos,
                                    TestAirmobisim.endPos):  # use zip function correct it later on

            self.assertTrue(0 <= (startpos.x and endpos.x) <= TestAirmobisim.playgroundSizeX,
                            'waypoint x should be within playgroundX')
            self.assertTrue(0 <= (startpos.y and endpos.y) <= TestAirmobisim.playgroundSizeY,
                            'waypoint y should be within playgroundY')
            self.assertTrue(0 <= (startpos.z and endpos.z) <= TestAirmobisim.playgroundSizeZ,
                            'waypoint z should be within playgroundZ')

    def test_speed_limit_sp(self):
        for index, uavsp in enumerate(TestAirmobisim.uavsSpline):
            splineObj = Splinemobility(index, TestAirmobisim.waypointX[index],
                                       TestAirmobisim.waypointY[index], TestAirmobisim.waypointZ[index],
                                       TestAirmobisim.speed_lin[index], None)
            print('total flight time')
            print(splineObj._totalFlightTime)
            self.assertTrue(splineObj._totalFlightTime <= TestAirmobisim.simTimeLimit,
                            'this speed will exceed the simTimeLimit consider reducing it')

    def test_all_waypoints_simulated(self):
        self.skipTest("not useful")
        # run simulation sp
        self.run_simulator_sp()
        # get all uav_sp dataframe
        df_simulation_uavs = self.process_result_file()  # result dataframe for each uav
        # TestAirmobisim.waypointX[0].append(0.678822509939085)
        # TestAirmobisim.waypointY[0].append(0.678822509939085)
        # TestAirmobisim.waypointZ[0].append(3.0)
        for index, df_uav in enumerate(df_simulation_uavs):  # loop through each uav dataframe
            for x, y, z in zip(TestAirmobisim.waypointX[index], TestAirmobisim.waypointY[index],
                               TestAirmobisim.waypointZ[index]):  # loop through input waypoints for each uav
                # print(x)
                # print(y)
                # print(z)
                value = 0.1
                df_uav_conditional = df_uav.loc[
                    (abs(df_uav['posX'] - x) <= value) & (abs(df_uav['posY'] - y) <= value) & (
                            abs(df_uav['posZ'] - z) <= value)]  # search for rows with satisfied conditions
                self.assertFalse(df_uav_conditional.empty, 'data frame should not be empty/ no such waypoint is found')
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
        self.assertEqual(len(TestAirmobisim.uavsSpline), 1, 'should be 1 check config')

    def test_simulation_finish_time(self):
        df_simulation_uavs = self.process_result_file()  # result dataframe for each uav

        for df_uav in df_simulation_uavs:
            df_uav_conditional = df_uav.loc[(df_uav['posZ'] == df_uav['posZ'].to_numpy()[-1]) &
                                            (df_uav['posY'] == df_uav['posY'].to_numpy()[-1]) &
                                            (df_uav['posX'] == df_uav['posX'].to_numpy()[
                                                -1])]  # search for rows which are similar as the last entry/ finish line

            self.assertTrue(df_uav_conditional['passedTime'].to_numpy()[0] <= TestAirmobisim.simTimeLimit,
                            'check simulation finish time')

    @patch('src.basemobility.Basemobility.doLog')
    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=True)
    def test_doLog_sp_mob(self, mock_getLinearMobilitySpFlag, mock_doLog):
        sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
                                TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0], None)

        sp_obj.makeMove()
        # print(sp_obj._waypointX)
        # print(sp_obj._waypointY)
        # print(sp_obj._waypointZ)
        # print(sp_obj._speed)
        self.assertTrue(mock_doLog.called, 'The model did not call doLog function. It should!')
        self.assertTrue(mock_getLinearMobilitySpFlag.called_once(),
                        'The model did not call getLinearMobilitySpFlag function. It should!')

    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=True)
    @patch('src.resultcollection.Resultcollection.logCurrentPosition')
    def test_logCurrentPosition_sp_mob(self, mock_logCurrentPosition, mock_getflag):
        sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
                                TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0], None)
        sp_obj.makeMove()
        self.assertTrue(mock_logCurrentPosition.called)

    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=False)
    @patch('src.basemobility.Basemobility.doLog')
    def test_doLog_lin_mob(self, mock_doLog, mock_getLinearMobilitySpFlag):
        # angle = math.atan2(TestAirmobisim.endPos[0].y - TestAirmobisim.startPos[0].y, TestAirmobisim.endPos[0].x -
        # TestAirmobisim.startPos[0].x) * 180 / math.pi
        angle = 0
        polygon_file_path = None
        lin_obj = Linearmobility(0, TestAirmobisim.startPos[0], TestAirmobisim.endPos[0], angle,
                                 TestAirmobisim.speed_lin[0], polygon_file_path)
        # mock_getLinearMobilitySpFlag.retuned_value = True
        lin_obj.makeMove()

        # self.assertTrue(mock_logCurrentPosition.called)
        self.assertTrue(mock_doLog.called)
        self.assertTrue(mock_getLinearMobilitySpFlag.called_once())
        # print(mock_getLinearMobilitySpFlag.call_count)
        # self.assertTrue(mock_getLinearMobilitySpFlag.called)

    # self.assertEqual(validInputSp,True)

    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=False)
    @patch('src.resultcollection.Resultcollection.logCurrentPosition')
    def test_logCurrentPosition_lin_mob(self, mock_logCurrentPosition, mock_getflag):
        angle = 0
        polygon_file_path = None

        lin_obj = Linearmobility(0, TestAirmobisim.startPos[0], TestAirmobisim.endPos[0], angle,
                                 TestAirmobisim.speed_lin[0], polygon_file_path)
        # print(lin_obj._move.getLinearMobilitySpFlag())
        lin_obj.makeMove()

        self.assertTrue(mock_logCurrentPosition.called, 'logCurrentPosition should be called')

    def test_model_selection_input(self):

        self.assertTrue(all((value == 1 or value == 0) for value in TestAirmobisim.kenetic_model.values()),
                        'values can be either 0 or 1')
        self.assertEqual([value for value in TestAirmobisim.kenetic_model.values()].count(1), 1,
                         "Model selection value can contain only one 1 ")

    def test_waypointTime_generated_splinemobility(self):
        for uav in range(len(TestAirmobisim.uavsSpline)):  # check for all uavs
            sp_obj = Splinemobility(uav, TestAirmobisim.waypointX[uav], TestAirmobisim.waypointY[uav],
                                    TestAirmobisim.waypointZ[uav], TestAirmobisim.speed_sp[uav], None)
            print(sp_obj._waypointTime)
            for item in sp_obj._waypointTime:  # test for each entry in waypointTime list
                self.assertEqual([value for value in sp_obj._waypointTime].count(item), 1,
                                 "waypointTime should contain unique timestamp without reperation ")  # test uniqueness of waypointTime entry

    def test_negative_speed(self):
        self.assertTrue(all(speed >= 0 for speed in TestAirmobisim.speed_sp),
                        'Speed can not be negative for splinemobility model')

        self.assertTrue(all(speed >= 0 for speed in TestAirmobisim.speed_lin),
                        'Speed can not be negative for linearmobility model')

    # @patch('src.simulationparameter.Simulationparameter.stepLength',cls.step)
    def test_obstacle_for_spline(self):
        Simulationparameter.stepLength = TestAirmobisim.stepLength
        self._simulationSteps = TestAirmobisim.simTimeLimit / Simulationparameter.stepLength

        sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
                                TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0],
                                '/Users/pritom/Desktop/Paderborn/project/AirMobiSim/examples/simpleSimulation/intersection.add.xml')

        while Simulationparameter.currentSimStep < self._simulationSteps:
            Simulationparameter.incrementCurrentSimStep()
            removeNode = sp_obj.makeMove()  # building ahead
            if removeNode:
                print('removing uav', sp_obj._uid)
                break;
                # self._managedNodes.remove(node)


        # print(Simulationparameter.stepLength)
        # Simulationparameter.incrementCurrentSimStep()
        # print(Simulationparameter.currentSimStep)

        # with patch("src.simulationparameter.Simulationparameter.incrementCurrentSimStep", wraps=self.fake_func) as mock_func:
        #
        #     Simulationparameter.incrementCurrentSimStep()
        #     print(Simulationparameter.currentSimStep)
        #     Simulationparameter.incrementCurrentSimStep()
        #     print(Simulationparameter.currentSimStep)
        # passedTime =(Simulationparameter.currentSimStep * Simulationparameter.stepLength)


    # print(sp_obj.polygon_file_path )


def fake_func(self):
    Simulationparameter.currentSimStep += 2


def getStepLength(self):
    return TestAirmobisim.stepLength


if __name__ == '__main__':
    unittest.main()
