import math
import unittest
from shapely.geometry import Point
from proto.DroCIBridge import startServer
from src.simulation import  Simulation
from google.protobuf import empty_pb2

import grpc
from proto import airmobisim_pb2_grpc
from proto import airmobisim_pb2

uavs = [{'startPosX': 500, 'startPosY': 500, 'startPosZ': 500, 'endPosX': 1500, 'endPosY': 1500, 'endPosZ': 1500,
         'speed': 50}]
simulation_obj_c = Simulation('../examples/simpleSimulation', stepLength=0.01, simTimeLimit=35, playgroundSizeX=5000, playgroundSizeY=5000, playgroundSizeZ=5000,
                                                     linearMobilityFlag = True, splineMobilityFlag=False, uavs=uavs, polygon_file_path=None,
                                                     collision_action=None,
                                                     speed=None, waypointX=None, waypointY=None,
                                                     waypointZ=None)

class TestDroCIBridge(unittest.TestCase):
    __stub =None
    # simulation_obj_c
    # global simulation_obj_c

    simulation_obj_c: Simulation
    @classmethod
    def setUpClass(cls) -> None:
        # cls.simulation_obj_c = Simulation('../examples/simpleSimulation', 0.01, 30, 5000, 5000, 5000,
        #  True, False, None, polygon_file_path=None, collision_action=None,
        #  speed=None, waypointX=None, waypointY=None,
        #  waypointZ=None)

        channel = grpc.insecure_channel('localhost:5001')
        cls.__stub = airmobisim_pb2_grpc.AirMobiSimStub(channel)
        pass

    def tearDown(self) -> None:
        # print('after every tests')
        number_obj = airmobisim_pb2.Number()
        number_obj.num = 1001

        self.__stub.DeleteUAV(number_obj)
        pass

    def test_Start(self):
        self.__stub.Start(empty_pb2.Empty())



    def test_interface_insertUav(self):
        # num_obj= airmobisim_pb2.Number(num=3)

        startuav_obj= self.build_startUav_obj()

        # cod_obj= airmobisim_pb2.Coordinates(x=1.1, y=2.2, z=3.3)
        # insert_uav= stub.InsertUAV(airmobisim_pb2.StartUav(id=1000, coordinates=startuav_obj, speed=2.2, angle=1.2))
        self.__stub.InsertUAV(startuav_obj)
        # print('aikhane')
        uav_list =self.__stub.GetManagedHosts(empty_pb2.Empty())
        # print('uav list: ', uav_list)
        # print('uav list: ', type(uav_list))
        # print('uav id: ', uav_list.uavs[0].id)
        # print('uav x: ', uav_list.uavs[0].x)
        # print('uav y: ', uav_list.uavs[0].y)
        # print('uav z: ', uav_list.uavs[0].z)
        # print('uav list length : ', len(uav_list.uavs))

        matched_uid_list= [uav for uav in uav_list.uavs if uav.id == 1001]
        self.assertEqual(len(matched_uid_list), 1, 'uid should be unique for each uav')

        self.assertEqual(matched_uid_list[0].id, 1001,'uid does not match for just inserted uav')

    def test_interface_DeleteUAV(self):
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        # print('bal er length: ',len(uav_list.uavs))
        uav_count = len(uav_list.uavs)

        startuav_obj = self.build_startUav_obj()

        self.__stub.InsertUAV(startuav_obj)
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        self.assertEqual(len(uav_list.uavs), uav_count+1, 'After inserting an uav the uav count should increase by 1')

        number_obj = airmobisim_pb2.Number()
        number_obj.num = 1001

        self.__stub.DeleteUAV(number_obj)

        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        self.assertEqual(len(uav_list.uavs), uav_count, 'After deleting an uav the uav count should decrease by 1')

        matched_uid_list = [uav for uav in uav_list.uavs if uav.id == 1001]
        self.assertEqual(len(matched_uid_list), 0, f'No uav with uid={1001} should be present now')



        pass

    def test_interface_getNumberCurrentUAV(self):
        uav_count = self.__stub.getNumberCurrentUAV(empty_pb2.Empty()).num
        print('uav count is ', uav_count)
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        self.assertEqual(len(uav_list.uavs), uav_count, 'Uav count not consistent ')

        startuav_obj = self.build_startUav_obj()

        self.__stub.InsertUAV(startuav_obj)
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        self.assertEqual(len(uav_list.uavs), self.__stub.getNumberCurrentUAV(empty_pb2.Empty()).num, 'After inserting an uav the uav count is not consistent')

        pass


    def test_interface_SetDesiredSpeed(self):
        startuav_obj = self.build_startUav_obj()

        self.__stub.InsertUAV(startuav_obj)
        self.__stub.SetDesiredSpeed( airmobisim_pb2.UavSetSpeed(id=1001,speed=100))
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        matched_uid_list = [uav for uav in uav_list.uavs if uav.id == 1001]
        self.assertEqual(matched_uid_list[0].speed, 100, f'No uav with uid={1001} should be present now')
        # self.assertEqual(len(uav_list.uavs), self.__stub.getNumberCurrentUAV(empty_pb2.Empty()).num,
        #                  'After inserting an uav the uav count is not consistent')


    def test_GetManagedHosts(self):
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        initial_uav_count = len(uav_list.uavs)
        self.assertEqual(initial_uav_count, 1, 'Initial uav count should be 1')

        number_obj = airmobisim_pb2.Number(num=0)
        self.__stub.DeleteUAV(number_obj)

        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        new_uav_count = len(uav_list.uavs)
        self.assertEqual(new_uav_count, 0, 'After deleting 1 uav the count should be 0')

        startuav_obj = self.build_startUav_obj(uid=1000)
        self.__stub.InsertUAV(startuav_obj)

        startuav_obj = self.build_startUav_obj(uid=1001)
        self.__stub.InsertUAV(startuav_obj)

        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        self.assertEqual(len(uav_list.uavs), 2, 'After inserting 2 uavs the count should be 2')

        matched_uid_list = [uav for uav in uav_list.uavs if uav.id == 1001]
        self.assertEqual(len(matched_uid_list), 1, f'One uav with uid={1001} should be present now')

        matched_uid_list = [uav for uav in uav_list.uavs if uav.id == 1000]
        self.assertEqual(len(matched_uid_list), 1, f'One uav with uid={1000} should be present now')


    def test_ExecuteOneTimeStep(self):
        uav_list = self.__stub.GetManagedHosts(empty_pb2.Empty())
        initial_uav_count = len(uav_list.uavs)
        self.assertEqual(initial_uav_count, 1, 'Initial uav count should be 1')
        self.assertEqual(uav_list.uavs[0].id, 0, f'This is not the initial uav with uid=0 but {uav_list.uavs[0].id}')

        responseQuery_obj_dummy = self.__stub.ExecuteOneTimeStep(empty_pb2.Empty())

        self.assertEqual(len(responseQuery_obj_dummy.responses), 1, f'This is not the initial uav with uid=0 but {uav_list.uavs[0].id}')

        responseQuery_obj = self.__stub.ExecuteOneTimeStep(empty_pb2.Empty())
        currentPos = Point(responseQuery_obj.responses[0].x, responseQuery_obj.responses[0].y, responseQuery_obj.responses[0].z)
        print(currentPos)

        responseQuery_obj2 = self.__stub.ExecuteOneTimeStep(empty_pb2.Empty())
        nextPos = Point(responseQuery_obj2.responses[0].x, responseQuery_obj2.responses[0].y,
                        responseQuery_obj2.responses[0].z)
        print(nextPos)

        distance = math.sqrt((nextPos.x - currentPos.x) ** 2 + (nextPos.y - currentPos.y) ** 2 + (
                nextPos.z - currentPos.z) ** 2)

        print('distance1', distance)

        uav_speed_calculated = distance / 0.01     #todo step length might be different fix it
        uav_speed_provided = responseQuery_obj.responses[0].speed

        self.assertTrue(uav_speed_provided - 0.1 <= uav_speed_calculated <= uav_speed_provided + 0.1,
                        f'linear model: speed: {uav_speed_calculated} calculated from generated coordinates does not support the provided speed:{uav_speed_provided}')

        startuav_obj = self.build_startUav_obj()
        self.__stub.InsertUAV(startuav_obj)      # new uav inserted

        responseQuery_obj = self.__stub.ExecuteOneTimeStep(empty_pb2.Empty())
        currentPos_newUav = Point(responseQuery_obj.responses[1].x, responseQuery_obj.responses[1].y,
                           responseQuery_obj.responses[1].z)


        responseQuery_obj = self.__stub.ExecuteOneTimeStep(empty_pb2.Empty())
        newPos_newUav = Point(responseQuery_obj.responses[1].x, responseQuery_obj.responses[1].y,
                           responseQuery_obj.responses[1].z)

        distance = math.sqrt((newPos_newUav.x - currentPos_newUav.x) ** 2 + (newPos_newUav.y - currentPos_newUav.y) ** 2 + (
                newPos_newUav.z - currentPos_newUav.z) ** 2)

        uav_speed_calculated_new = distance / 0.01  # todo step length might be different fix it
        uav_speed_provided_new = responseQuery_obj.responses[1].speed

        self.assertTrue(uav_speed_provided_new - 0.1 <= uav_speed_calculated_new <= uav_speed_provided_new + 0.1,
                        f'linear model: speed: {uav_speed_calculated_new} calculated from generated coordinates does not support the provided speed:{uav_speed_provided_new}')


    def test_getMaxSimulationTime(self):
        maxSimTime_num_obj = self.__stub.GetMaxSimulationTime(empty_pb2.Empty())
        self.assertEqual(maxSimTime_num_obj.num, 35, f'max simulation time should be {35} sec')

    def test_getMaxSimulationSteps(self):
        maxSimStep_num_obj = self.__stub.getMaxSimulationSteps(empty_pb2.Empty())
        self.assertEqual(maxSimStep_num_obj.num, 3500, f'max simulation time should be {3500} sec')







    def build_startUav_obj(self, uid=1001):
        startuav_obj = airmobisim_pb2.StartUav()
        startuav_obj.id = uid
        startuav_obj.speed = 10
        startuav_obj.angle = 2
        startuav_obj.mobilityModel=1
        startuav_obj.removeUav=1
        c1 = startuav_obj.coordinates.add()
        c2 = startuav_obj.coordinates.add()
        c1.x = 0
        c1.y = 0
        c1.z = 0
        c2.x = 10
        c2.y = 10
        c2.z = 10
        return startuav_obj


def startGrpcServer():
    global simulation_obj_c
    startServer(simulation_obj_c)



if __name__ == '__main__':
    unittest.main()

