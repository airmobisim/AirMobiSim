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
        polygon_file = config['obstacle_detection']['polygon_file']
        cls.collision_action = config['obstacle_detection']['collision_action']
        homePath = os.environ['AIRMOBISIMHOME']
        cls.polygon_file_path = homePath + '/' + polygon_file
        # print('polygon file path: ', cls.polygon_file_path)

        cls.simTimeLimit = config['simulation']['simTimeLimit']
        cls.stepLength = config['simulation']['stepLength']
        cls.playgroundSizeX = config['simulation']['playgroundSizeX']
        cls.playgroundSizeY = config['simulation']['playgroundSizeY']
        cls.playgroundSizeZ = config['simulation']['playgroundSizeZ']
        cls.uavsSpline = config['uavsp']
        cls.uavsLinear = config['uav']
        cls.kenetic_model = config['kinetic_model']

        assert len(cls.uavsSpline) !=0, 'No Spline mobility uav is selected for testing in the config file'
        assert len(cls.uavsLinear) !=0, 'No Linear mobility uav is selected for testing in the config file'


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

    def test_config_waypoints_spline_mob(self):  # all inputs need to be positive and inside the playground

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

    def test_config_waypoints_linear_mob(self):  # all inputs need to be positive and inside the playground

        # self.assertTrue(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ),
        #                 'input waypoint length for x,y and z should be same')
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

    def test_speed_limit_spline(
            self):  # not to use very small values of speed so that the simulation is not completed with in the time limit
        for index, uavsp in enumerate(TestAirmobisim.uavsSpline):
            splineObj = Splinemobility(index, TestAirmobisim.waypointX[index],
                                       TestAirmobisim.waypointY[index], TestAirmobisim.waypointZ[index],
                                       TestAirmobisim.speed_sp[index], None)
            print('total flight time')
            print(splineObj._totalFlightTime)

            self.assertTrue(splineObj._totalFlightTime <= TestAirmobisim.simTimeLimit,
                            f'In spline mobility the {index}th UAV: time required to complete simulation= {splineObj._totalFlightTime}s. The speed={TestAirmobisim.speed_sp[index]}m/s will exceed the simTimeLimit={TestAirmobisim.simTimeLimit}s consider increasing the speed to finish simulation within time simTime')


    def test_speed_limit_linear(
            self):  # not to use very small values of speed so that the simulation is not completed with in the time limit
        angle = 0  # does not matter
        polygon_file_path = None
        for index, uavlin in enumerate(TestAirmobisim.uavsLinear):

            lin_obj = Linearmobility(index, TestAirmobisim.startPos[index], TestAirmobisim.endPos[index], angle,
                                     TestAirmobisim.speed_lin[index], polygon_file_path)
            print('total flight time')
            print(lin_obj._totalFlightTime)

            self.assertTrue(lin_obj._totalFlightTime <= TestAirmobisim.simTimeLimit,
                            f'In linear mobility the {index}th UAV: time required to complete simulation= {lin_obj._totalFlightTime}s. The speed={TestAirmobisim.speed_lin[index]}m/s will exceed the simTimeLimit={TestAirmobisim.simTimeLimit}s consider increasing the speed to finish simulation within time simTime')


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

    def test_model_selection_input(self):  # check the validity for model selection input

        self.assertTrue(all((value == 1 or value == 0) for value in TestAirmobisim.kenetic_model.values()),
                        'values can be either 0 or 1')
        self.assertEqual([value for value in TestAirmobisim.kenetic_model.values()].count(1), 1,
                         "Model selection value can contain only one 1 ")

    def test_collision_action_input(self):  # check the validity of collision action input

        self.assertTrue(TestAirmobisim.collision_action == 1 or TestAirmobisim.collision_action == 2 or TestAirmobisim.collision_action== 3,
                        'collision action value can either be 1, 2 or 3. 1-> warning message. 2-> ignore everything. '
                        '3-> remove uav in case of collision')


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

    def test_obstacle_fileLoaded_spline(self):  # test obstacle file loaded for spline mobility
        sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
                                TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0],
                                TestAirmobisim.polygon_file_path)

        self.assertTrue(sp_obj.polygon_file_path != None, 'poly file is not loaded')
        self.assertTrue(os.path.exists(sp_obj.polygon_file_path),
                        'No such polygon file exists according to the provided '
                        'path')

    def test_obstacle_fileLoaded_linear(self):  # test obstacle file loaded for linear mobility
        angle = 0
        polygon_file_path = TestAirmobisim.polygon_file_path

        lin_obj = Linearmobility(0, TestAirmobisim.startPos[0], TestAirmobisim.endPos[0], angle,
                                 TestAirmobisim.speed_lin[0], polygon_file_path)

        self.assertTrue(lin_obj.polygon_file_path != None, 'poly file is not loaded')
        self.assertTrue(os.path.exists(lin_obj.polygon_file_path),
                        'No such polygon file exists according to the provided '
                        'path')

    # @patch('src.simulationparameter.Simulationparameter.stepLength',cls.step)
    def test_obstacle_for_spline(self):  # todo complete this test case
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
    # todo write test case for collision_action


def fake_func(self):
    Simulationparameter.currentSimStep += 2


def getStepLength(self):
    return TestAirmobisim.stepLength


if __name__ == '__main__':
    unittest.main()
