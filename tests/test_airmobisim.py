import math
import time
import unittest
from unittest.mock import patch, Mock, MagicMock

import pandas as pd
from shapely.geometry import Point
import numpy as np
import shutil

from src.basemobility import Basemobility
from src.linearmobility import Linearmobility
from src.yamlparser import Yamlparser
from src.splinemobility import Splinemobility
from src.simulationparameter import Simulationparameter
from src.resultcollection import Resultcollection
from src.simulation import Simulation
from src.uav import Uav
from src.movement import Movement
from src.singleton import Singleton

import airmobisim
import os



class TestAirmobisim(unittest.TestCase):



    @classmethod
    def setUpClass(cls) -> None:
        homePath = os.environ['AIRMOBISIMHOME']
        p = Yamlparser(homePath +'/examples/simpleSimulation/simulation.config')
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

        # assert len(cls.uavsSpline) != 0, 'No Spline mobility uav is selected for testing in the config file'
        # assert len(cls.uavsLinear) != 0, 'No Linear mobility uav is selected for testing in the config file'

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
        if cls.uavsLinear is not None:
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
        # print('before running every tests')
        # step = TestAirmobisim.stepLength
        pass

    def tearDown(self) -> None:
        # print('after every tests')
        pass





    def test_config_waypoints_spline_mob(self):  # all inputs need to be positive and inside the playground

        self.assertTrue(len(TestAirmobisim.waypointX) == len(TestAirmobisim.waypointY) == len(TestAirmobisim.waypointZ),
                        'input waypoint length for x,y and z should be same')

        for i, v in enumerate(TestAirmobisim.waypointX):
            self.assertTrue(len(TestAirmobisim.waypointX[i]) == len(TestAirmobisim.waypointY[i]) == len(
                TestAirmobisim.waypointZ[i]), 'waypoint x,y,z should be same for each uav')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeX for item in TestAirmobisim.waypointX[i]),
                            'waypoint x should be within playgroundX')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeY for item in TestAirmobisim.waypointY[i]),
                            'waypoint y should be within playgroundY')
            self.assertTrue(all(0 <= item <= TestAirmobisim.playgroundSizeZ for item in TestAirmobisim.waypointZ[i]),
                            'waypoint z should be within playgroundZ')


    def test_config_waypoints_linear_mob(self):  # all inputs need to be positive and inside the playground

        for startpos, endpos in zip(TestAirmobisim.startPos,
                                    TestAirmobisim.endPos):
            self.assertTrue(0 <= (startpos.x and endpos.x) <= TestAirmobisim.playgroundSizeX,
                            'waypoint x should be within playgroundX')
            self.assertTrue(0 <= (startpos.y and endpos.y) <= TestAirmobisim.playgroundSizeY,
                            'waypoint y should be within playgroundY')
            self.assertTrue(0 <= (startpos.z and endpos.z) <= TestAirmobisim.playgroundSizeZ,
                            'waypoint z should be within playgroundZ')


    def test_speed_limit_spline(self):  # check speed to  finish simulation within timelimit
        if TestAirmobisim.uavsSpline is not None:
            for index, uavsp in enumerate(TestAirmobisim.uavsSpline):
                waypoints = [Point(x,y,z) for x,y,z in zip(TestAirmobisim.waypointX[index], TestAirmobisim.waypointY[index], TestAirmobisim.waypointZ[index])]

                uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=TestAirmobisim.speed_sp[index], polygon_file_path=None,collision_action=2,model_selection=2)


                self.assertTrue(uavsp_obj.getMobility()._totalFlightTime <= TestAirmobisim.simTimeLimit,
                                f'In spline mobility the {index}th UAV: time required to complete simulation= {uavsp_obj.getMobility()._totalFlightTime}s. The speed={TestAirmobisim.speed_sp[index]}m/s will exceed the simTimeLimit={TestAirmobisim.simTimeLimit}s consider increasing the speed to finish simulation within time simTime')


    def test_speed_limit_linear(self):  # check speed to  finish simulation within timelimit
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01
        if TestAirmobisim.uavsLinear is not None:
            for index, uavlin in enumerate(TestAirmobisim.uavsLinear):
                waypoints = [TestAirmobisim.startPos[index], TestAirmobisim.endPos[index]]
                uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=TestAirmobisim.speed_lin[index], polygon_file_path=None, collision_action=2,
                                 model_selection=1)

                self.assertTrue(uavlin_obj.getMobility()._totalFlightTime <= TestAirmobisim.simTimeLimit,
                                f'In linear mobility the {index}th UAV: time required to complete simulation= {uavlin_obj.getMobility()._totalFlightTime}s. The speed={TestAirmobisim.speed_lin[index]}m/s will exceed the simTimeLimit={TestAirmobisim.simTimeLimit}s consider increasing the speed to finish simulation within time simTime')


    @patch('src.basemobility.Basemobility.doLog')
    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=True)
    def test_doLog_sp_mob(self, mock_getLinearMobilitySpFlag, mock_doLog):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1

        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None, collision_action=2,
                         model_selection=2)
        uavlin_obj.getMobility().makeMove()

        self.assertTrue(mock_doLog.called, 'The model did not call doLog function. It should!')
        self.assertTrue(mock_getLinearMobilitySpFlag.called_once(),
                        'The model did not call getLinearMobilitySpFlag function. It should!')


    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=True)
    @patch('src.resultcollection.Resultcollection.logCurrentPosition')
    def test_logCurrentPosition_sp_mob(self, mock_logCurrentPosition, mock_getflag):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1

        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None, collision_action=2,
                         model_selection=2)
        uavlin_obj.getMobility().makeMove()

        self.assertTrue(mock_logCurrentPosition.called)


    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=False)
    @patch('src.basemobility.Basemobility.doLog')
    def test_doLog_lin_mob(self, mock_doLog, mock_getLinearMobilitySpFlag):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1

        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None, collision_action=2,
                         model_selection=1)

        uavlin_obj.getMobility().makeMove()

        self.assertTrue(mock_doLog.called)
        self.assertTrue(mock_getLinearMobilitySpFlag.called_once())


    @patch('src.movement.Movement.getLinearMobilitySpFlag', return_value=False)
    @patch('src.resultcollection.Resultcollection.logCurrentPosition')
    def test_logCurrentPosition_lin_mob(self, mock_logCurrentPosition, mock_getflag):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1

        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None, collision_action=2, model_selection=1)

        uavlin_obj.getMobility().makeMove()

        self.assertTrue(mock_logCurrentPosition.called, 'logCurrentPosition should be called')


    def test_model_selection_input(self):  # check the validity for model selection input

        self.assertTrue(all((value == 1 or value == 0) for value in TestAirmobisim.kenetic_model.values()),
                        'values can be either 0 or 1')
        self.assertEqual([value for value in TestAirmobisim.kenetic_model.values()].count(1), 1,
                         "Model selection value can contain only one 1 ")


    def test_collision_action_input(self):  # check the validity of collision action input

        self.assertTrue(
            TestAirmobisim.collision_action == 1 or TestAirmobisim.collision_action == 2 or TestAirmobisim.collision_action == 3,
            'collision action value can either be 1, 2 or 3. 1-> warning message. 2-> ignore everything. '
            '3-> remove uav in case of collision')


    def test_waypointTime_generated_splinemobility(self):
        for uav in range(len(TestAirmobisim.uavsSpline)):  # check for all uavs
            waypoints = [Point(x, y, z) for x, y, z in zip(TestAirmobisim.waypointX[uav], TestAirmobisim.waypointY[uav],
                                    TestAirmobisim.waypointZ[uav])]

            uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=TestAirmobisim.speed_sp[uav], polygon_file_path=TestAirmobisim.polygon_file_path,
                            collision_action=2,
                            model_selection=2)


            for item in uavsp_obj.getMobility()._waypointTime:  # tests for each entry in waypointTime list
                self.assertEqual([value for value in uavsp_obj.getMobility()._waypointTime].count(item), 1,
                                 "waypointTime should contain unique timestamp without reperation ")  # tests uniqueness of waypointTime entry


    def test_negative_speed_configFile(self):
        self.assertTrue(all(speed >= 0 for speed in TestAirmobisim.speed_sp),
                        'Speed can not be negative for splinemobility model')

        self.assertTrue(all(speed >= 0 for speed in TestAirmobisim.speed_lin),
                        'Speed can not be negative for linearmobility model')


    def test_obstacle_fileLoaded_spline(self):  # tests obstacle file loaded for spline mobility
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1
        simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=2,
                         model_selection=2)

        # sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
        #                         TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0],
        #                         TestAirmobisim.polygon_file_path)

        self.assertTrue(uavsp_obj.getMobility().polygon_file_path != None, 'poly file is not loaded')
        self.assertTrue(os.path.exists(uavsp_obj.getMobility().polygon_file_path),
                        'No such polygon file exists according to the provided '
                        'path')


    def test_obstacle_fileLoaded_linear(self):  # tests obstacle file loaded for linear mobility
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1
        simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=1,
                         model_selection=1)


        self.assertTrue(uavlin_obj.getMobility().polygon_file_path != None, 'poly file is not loaded')
        self.assertTrue(os.path.exists(uavlin_obj.getMobility().polygon_file_path),
                        'No such polygon file exists according to the provided '
                        'path')

    @unittest.skip
    # @patch('src.simulationparameter.Simulationparameter.stepLength',cls.step)
    def test_obstacle_for_spline(self):
        Simulationparameter.stepLength = TestAirmobisim.stepLength
        self._simulationSteps = TestAirmobisim.simTimeLimit / Simulationparameter.stepLength

        sp_obj = Splinemobility(0, TestAirmobisim.waypointX[0], TestAirmobisim.waypointY[0],
                                TestAirmobisim.waypointZ[0], TestAirmobisim.speed_sp[0],
                                TestAirmobisim.polygon_file_path)

        while Simulationparameter.currentSimStep < self._simulationSteps:
            Simulationparameter.incrementCurrentSimStep()
            removeNode = sp_obj.makeMove()  # building ahead
            if removeNode:
                print('removing uav', sp_obj._uid)
                break;
                # self._managedNodes.remove(node)

    @unittest.skip   # Todo this test case depends on removeUav flag fix it once removeUav is merged to master
    @patch('src.linearmobility.Linearmobility.manageObstacles')
    def test_manageObstacles_overallTask_linearModel(self, mock_manageObstacle):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 0.4
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=1,
                         model_selection=1)


        removeUav = uavlin_obj.getMobility().makeMove()
        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 1,'collision action as \'warning\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count==1, 'mock_manageObstacle should be called while running the and colllision action value != 2')
        self.assertEqual(removeUav[0],False, 'removeUav value should be false: does not remove uav')

        Simulationparameter.incrementCurrentSimStep()
        uavlin_obj.getMobility()._collisionAction = 2
        removeUav = uavlin_obj.getMobility().makeMove()
        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 2,'collision action as \'do nothing\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count == 1,'mock_manageObstacle should be called once at this point since collision action == 2')
        self.assertEqual(removeUav[0],False, 'removeUav value should be false: does not remove uav')

        Simulationparameter.incrementCurrentSimStep()
        uavlin_obj.getMobility()._collisionAction = 3
        removeUav= uavlin_obj.getMobility().makeMove()

        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 3,'collision action as \'remove node\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count == 2,'mock_manageObstacle should be called while running the and colllision action value != 2')
        self.assertEqual(removeUav[0],False, 'removeUav value should be false: does not remove uav')

    @unittest.skip  # Todo this test case depends on removeUav flag fix it once removeUav is merged to master
    def test_manageObstacles_removeNode_linearModel(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 0.4
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=3,
                         model_selection=1, removeUav=1)

        self.assertFalse(uavlin_obj.getMobility()._obstacleDetector_flag, '_obstacleDetector_flag should be False at this point')


        with patch('src.movement.Movement.getFutureCoordinate') as mock_getFutureCoordinate:
            mock_getFutureCoordinate.return_value = (7.2, 7.2)   # hard-coding point inside the building
            self.assertTrue(uavlin_obj.getMobility()._collisionAction==3, 'collision active should be 3')

            removeUav = uavlin_obj.getMobility().makeMove()
            self.assertTrue(uavlin_obj.getMobility()._obstacleDetector_flag,'_obstacleDetector_flag should be False at this point')
            self.assertTrue(removeUav[0]==True, 'Should return True: flag to remove uav')

        # todo check uav list to ensure the uav is removed


    def test_manageObstacles_general_linearModel(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavlin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path, collision_action=1,
                        model_selection=1)


        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 1, 'collision action as \'warning\' is not selected')
        self.assertTrue(len(uavlin_obj.getMobility()._obstacles) >= 1, 'No building is present as obstacle')
        uavlin_obj.getMobility().getMove().setFutureCoordinate((8,9))

        self.assertFalse(uavlin_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavlin_obj.getMobility().manageObstacles(1,2)
        self.assertTrue(uavlin_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')

        uavlin_obj.getMobility()._collisionAction = 2
        uavlin_obj.getMobility()._obstacleDetector_flag = False
        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 2, 'collision action as \'No action \' is not selected')
        self.assertFalse(uavlin_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavlin_obj.getMobility().manageObstacles(1, 2)
        self.assertTrue(uavlin_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')

        uavlin_obj.getMobility()._collisionAction = 3
        uavlin_obj.getMobility()._obstacleDetector_flag = False
        self.assertTrue(uavlin_obj.getMobility()._collisionAction == 3, 'collision action as \'Remove node \' is not selected')
        self.assertFalse(uavlin_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavlin_obj.getMobility().manageObstacles(1, 2)
        self.assertTrue(uavlin_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')

    @unittest.skip  # Todo this test case depends on removeUav flag fix it once removeUav is merged to master
    def test_manageObstacles_removeNode_splineModel(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 0.4
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=3,
                         model_selection=2, removeUav=1)

        self.assertFalse(uavsp_obj.getMobility()._obstacleDetector_flag, '_obstacleDetector_flag should be False at this point')


        with patch('src.movement.Movement.getFutureCoordinate') as mock_getFutureCoordinate:
            mock_getFutureCoordinate.return_value = (7.2, 7.2)   # hard-coding point inside the building
            self.assertTrue(uavsp_obj.getMobility()._collisionAction==3, 'collision active should be 3')

            removeUav = uavsp_obj.getMobility().makeMove()
            self.assertTrue(uavsp_obj.getMobility()._obstacleDetector_flag,'_obstacleDetector_flag should be False at this point')
            self.assertTrue(removeUav[0]==True, 'Should return True: flag to remove uav')

        # todo chech uav list to ensure the uav is removed

    @unittest.skip #todo fix now
    @patch('src.splinemobility.Splinemobility.manageObstacles')
    def test_manageObstacles_overallTask_splineModel(self, mock_manageObstacle):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 0.4
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path,
                         collision_action=1,
                         model_selection=2)

        removeUav = uavsp_obj.getMobility().makeMove()
        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 1,
                        'collision action as \'warning\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count == 1,
                        'mock_manageObstacle should be called while running the and colllision action value != 2')
        self.assertEqual(removeUav, False, 'removeUav value should be false: does not remove uav')

        Simulationparameter.incrementCurrentSimStep()
        uavsp_obj.getMobility()._collisionAction = 2
        removeUav = uavsp_obj.getMobility().makeMove()
        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 2,
                        'collision action as \'do nothing\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count == 1,
                        'mock_manageObstacle should be called once at this point since collision action == 2')
        self.assertEqual(removeUav, False, 'removeUav value should be false: does not remove uav')

        Simulationparameter.incrementCurrentSimStep()
        uavsp_obj.getMobility()._collisionAction = 3
        removeUav = uavsp_obj.getMobility().makeMove()

        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 3,
                        'collision action as \'remove node\' is not selected')
        self.assertTrue(mock_manageObstacle.call_count == 2,
                        f'mock_manageObstacle should be called while running the and colllision action value != 2 but {mock_manageObstacle.call_count}')
        self.assertEqual(removeUav, False, 'removeUav value should be false: does not remove uav')


    def test_manageObstacles_general_splineModel(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed = 1
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep = 0
        Simulationparameter.stepLength = 0.01

        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=TestAirmobisim.polygon_file_path, collision_action=1,
                        model_selection=2)


        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 1, 'collision action as \'warning\' is not selected')
        self.assertTrue(len(uavsp_obj.getMobility()._obstacles) >= 1, 'No building is present as obstacle')
        uavsp_obj.getMobility().getMove().setFutureCoordinate((8,9))

        self.assertFalse(uavsp_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavsp_obj.getMobility().manageObstacles(1,2)
        self.assertTrue(uavsp_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')

        uavsp_obj.getMobility()._collisionAction = 2
        uavsp_obj.getMobility()._obstacleDetector_flag = False
        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 2, 'collision action as \'No action \' is not selected')
        self.assertFalse(uavsp_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavsp_obj.getMobility().manageObstacles(1, 2)
        self.assertTrue(uavsp_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')

        uavsp_obj.getMobility()._collisionAction = 3
        uavsp_obj.getMobility()._obstacleDetector_flag = False
        self.assertTrue(uavsp_obj.getMobility()._collisionAction == 3, 'collision action as \'Remove node \' is not selected')
        self.assertFalse(uavsp_obj.getMobility()._obstacleDetector_flag, 'Initial value should be false')
        uavsp_obj.getMobility().manageObstacles(1, 2)
        self.assertTrue(uavsp_obj.getMobility()._obstacleDetector_flag, 'Collision is not detected')


    def test_logCurrentPosition(self):

        Singleton.destroy()
        resultCollection_obj = Resultcollection()
        movemoent_obj = Movement()
        movemoent_obj.setPassedTime(50)

        resultCollection_obj.logCurrentPosition(1, Point(100, 200, 300),movemoent_obj)
        self.assertFalse(resultCollection_obj._firstLog, 'firstLog attribute value should be false now')

        movemoent_obj.setPassedTime(500)
        resultCollection_obj.logCurrentPosition(10, Point(1000, 2000, 3000),movemoent_obj)

        # result_file_path = resultCollection_obj._logDir + "/examples/simpleSimulation/results/positionResults.csv"
        result_file_path= os.environ['AIRMOBISIMHOME']+ "/examples/simpleSimulation/results/positionResults_-1.csv"
        df_data = pd.read_csv(result_file_path, sep='\t')

        self.assertTrue(df_data.columns[0] == 'uid', 'first column name is not \'uid\'')
        self.assertTrue(df_data.columns[1] == 'passedTime', 'second column name is not \'passedTime\'')
        self.assertTrue(df_data.columns[2] == 'posX', 'third column name is not \'posX\'')
        self.assertTrue(df_data.columns[3] == 'posY', 'fourth column name is not \'posY\'')
        self.assertTrue(df_data.columns[4] == 'posZ', 'fifth column name is not \'posZ\'')


        self.assertTrue(df_data.iloc[0,0] == 1, 'uid should be recorded as 1')
        self.assertTrue(df_data.iloc[0,1] == 50, 'passedTime should be recorded as 50')
        self.assertTrue(df_data.iloc[0,2] == 100, 'pasX should be recorded as 100')
        self.assertTrue(df_data.iloc[0,3] == 200, 'pasY should be recorded as 200')
        self.assertTrue(df_data.iloc[0,4] == 300, 'pasZ should be recorded as 300')

        self.assertTrue(df_data.iloc[1, 0] == 10, 'uid should be recorded as 10')
        self.assertTrue(df_data.iloc[1, 1] == 500, 'passedTime should be recorded as 500')
        self.assertTrue(df_data.iloc[1, 2] == 1000, 'pasX should be recorded as 1000')
        self.assertTrue(df_data.iloc[1, 3] == 2000, 'pasY should be recorded as 2000')
        self.assertTrue(df_data.iloc[1, 4] == 3000, 'pasZ should be recorded as 3000')


    def test_resultcollection_file_dir_missing(self):
        Singleton.destroy()
        result_dir = '../examples/simpleSimulation/results/'
        if os.path.exists(result_dir):
            shutil.rmtree(result_dir)

        self.assertFalse(os.path.exists(result_dir), 'Result directory should not be present at this point')
        result_obj_1 =  Resultcollection()
        self.assertEqual(result_dir , result_obj_1._logDir, 'Hard coded result path is not similar as used in the simulator ')
        self.assertTrue(os.path.exists(os.path.abspath(result_dir)),'Result directory should have been created at this point' )


    def test_logCurrentEnergy(self):
        Singleton.destroy()
        resultCollection_obj = Resultcollection()

        resultCollection_obj.logCurrentEnergy(1, 10.0, 100.1)
        self.assertFalse(resultCollection_obj._firstLog_energy, 'firstLog_energy attribute value should be false now')

        resultCollection_obj.logCurrentEnergy(10, 100.0, 1001.1)

        result_file_path = resultCollection_obj._logDir + "energyResults_-1.csv"
        df_data = pd.read_csv(result_file_path, sep='\t')

        self.assertTrue(df_data.columns[0] == 'uid', 'first column name is not \'uid\'')
        self.assertTrue(df_data.columns[1] == 'travelled distance', 'second column name is not \'travelled_distance\'')
        self.assertTrue(df_data.columns[2] == 'energy', 'third column name is not \'energy\'')

        self.assertTrue(df_data.iloc[0,0] == 1, 'uid should be recorded as 1')
        self.assertTrue(df_data.iloc[0,1] == 10.0, 'travelled_distance should be recorded as 10.0')
        self.assertTrue(df_data.iloc[0,2] == 100.1, 'energy should be recorded as 100.1')

        self.assertTrue(df_data.iloc[1, 0] == 10, 'uid should be recorded as 10')
        self.assertTrue(df_data.iloc[1, 1] == 100.0, 'travelled_distance should be recorded as 100.0')
        self.assertTrue(df_data.iloc[1, 2] == 1001.1, 'energy should be recorded as 1001.1')


    def test_spline_position_vs_speed(self):
        waypointX = [0, 6, 12]
        waypointY = [0, 6, 12]
        waypointZ = [3, 3, 3]
        speed=1
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep=0
        Simulationparameter.stepLength= 0.01
        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None,collision_action=2, model_selection=2)

        uavsp_obj.getMobility().makeMove()
        currentPos=uavsp_obj.getMobility().getCurrentPos()


        Simulationparameter.incrementCurrentSimStep()
        uavsp_obj.getMobility().makeMove()
        nextPos = uavsp_obj.getMobility().getCurrentPos()

        distance = math.sqrt((nextPos.x - currentPos.x) ** 2 + (nextPos.y - currentPos.y) ** 2 + (
                nextPos.z - currentPos.z) ** 2)
        uav_speed = distance/ Simulationparameter.stepLength

        self.assertTrue(speed-0.1 <= uav_speed <= speed+0.1, 'Spline model: Generated coordinates does not support the provided speed')


        Simulationparameter.incrementCurrentSimStep()
        uavsp_obj.getMobility().makeMove()
        nextNextPos = uavsp_obj.getMobility().getCurrentPos()


        distance = math.sqrt((nextNextPos.x - nextPos.x) ** 2 + (nextNextPos.y - nextPos.y) ** 2 + (
                nextNextPos.z - nextPos.z) ** 2)
        uav_speed = distance / Simulationparameter.stepLength

        self.assertTrue(speed - 0.1 <= uav_speed <= speed + 0.1, 'Spline model: Generated coordinates does not support the provided speed')

    def test_linear_position_vs_speed(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed=1
        Simulationparameter.currentSimStep=0
        Simulationparameter.stepLength= 0.01
        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavLin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None,collision_action=2, model_selection=1)

        uavLin_obj.getMobility().makeMove()
        currentPos=uavLin_obj.getMobility().getCurrentPos()
        # currentPos=uavLin_obj.getMobility().getMove().getTempStartPos()
        print(currentPos)
        print(uavLin_obj.getMobility().getMove().getPassedTime())


        Simulationparameter.incrementCurrentSimStep()
        uavLin_obj.getMobility().makeMove()
        nextPos = uavLin_obj.getMobility().getCurrentPos()
        # nextPos = uavLin_obj.getMobility().getMove().getTempStartPos()
        print(nextPos)
        print(uavLin_obj.getMobility().getMove().getPassedTime())

        distance = math.sqrt((nextPos.x - currentPos.x) ** 2 + (nextPos.y - currentPos.y) ** 2 + (
                nextPos.z - currentPos.z) ** 2)
        uav_speed = distance/ Simulationparameter.stepLength

        self.assertTrue(speed-0.1 <= uav_speed <= speed+0.1, f'linear model: speed: {uav_speed} calculated from generated coordinates does not support the provided speed:{speed}')


        Simulationparameter.incrementCurrentSimStep()
        uavLin_obj.getMobility().makeMove()
        nextNextPos = uavLin_obj.getMobility().getCurrentPos()


        distance = math.sqrt((nextNextPos.x - nextPos.x) ** 2 + (nextNextPos.y - nextPos.y) ** 2 + (
                nextNextPos.z - nextPos.z) ** 2)
        uav_speed = distance / Simulationparameter.stepLength

        self.assertTrue(speed - 0.1 <= uav_speed <= speed + 0.1, f'linear model: speed: {uav_speed} calculated from generated coordinates does not support the provided speed:{speed}')






    def test_computeSplineDistance(self):
        distance=np.sum(Splinemobility.computeSplineDistance([0,3],[0,4],[0,0]))
        self.assertTrue(4.99<=distance<= 5.01, 'Distance computation is not correct')


    def test_linearModel_firstPosition(self):
        waypointX = [0, 12]
        waypointY = [0, 12]
        waypointZ = [3, 3]
        speed=1
        Simulationparameter.currentSimStep=0
        Simulationparameter.stepLength= 0.01
        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavLin_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None,collision_action=2, model_selection=1)

        uavLin_obj.getMobility().makeMove()
        currentPos=uavLin_obj.getMobility().getCurrentPos()

        self.assertEqual(currentPos, Point(0, 0, 3), 'After first iteration getCurrentPos() function should return the Starting position ' )
# TODO CHECH IN A MOMENT
    @unittest.skip
    def test_splineModel_firstPosition(self):
        waypointX = [0, 6, 12]
        waypointY = [0, 6, 12]
        waypointZ = [3, 3, 3]
        speed=1000
        # simulationparameter_obj = Simulationparameter()
        Simulationparameter.currentSimStep=0
        Simulationparameter.stepLength= 0.01
        waypoints = [Point(x, y, z) for x, y, z in zip(waypointX, waypointY, waypointZ)]

        uavsp_obj = Uav(uid=0, waypoints=waypoints, speed=speed, polygon_file_path=None, collision_action=2, model_selection=2)

        uavsp_obj.getMobility().makeMove()
        currentPos = uavsp_obj.getMobility().getCurrentPos()
        print(currentPos.x)
        print(currentPos.y)
        print(currentPos.z)
        self.assertEqual(currentPos, Point(0, 0, 3), 'After first iteration getCurrentPos() function should return the Starting position ')

    @unittest.skip     # todo this implementation depends on removeUav flag. -> not yet merged to master
    def test_removeUavFlag_linear(self):
        uavs = [
            {'startPosX': 500, 'startPosY': 500, 'startPosZ': 500, 'endPosX': 1500, 'endPosY': 1500, 'endPosZ': 1500,
             'speed': 50}]
        simulation_obj_c = Simulation('../examples/simpleSimulation', stepLength=0.01, simTimeLimit=35,
                                      playgroundSizeX=5000, playgroundSizeY=5000, playgroundSizeZ=5000,
                                      linearMobilityFlag=True, splineMobilityFlag=False, uavs=uavs,
                                      polygon_file_path=None,
                                      collision_action=None,
                                      speed=None, waypointX=None, waypointY=None, waypointZ=None)

        simulation_obj_c.initializeNodes()
        Simulationparameter.incrementCurrentSimStep()

        self.assertTrue(len(simulation_obj_c._managedNodes) == 1,
                        'Only one uav should be present in self._managedNodes')

        removeNode = simulation_obj_c._managedNodes[0]._mobility.makeMove()
        self.assertFalse(removeNode[0] or removeNode[1], 'both entry for removeNode should be False')
        self.assertFalse(simulation_obj_c._managedNodes[0]._mobility.getMove().getFinalFlag(),
                         'Initially finalFlag should be False')

        simulation_obj_c._managedNodes[0]._mobility.getMove().setFinalFlag(True)
        removeNode = simulation_obj_c._managedNodes[0]._mobility.makeMove()

        self.assertTrue(removeNode[1], 'finalFlag at position 1 should be True now')
        self.assertTrue(len(simulation_obj_c._managedNodes) == 1,
                        'Only one UAV should be present in self._managedNodes')

        simulation_obj_c.processNextStep()
        self.assertTrue(len(simulation_obj_c._managedNodes) == 0, 'No  UAV should be present in self._managedNodes')





if __name__ == '__main__':

    unittest.main()



