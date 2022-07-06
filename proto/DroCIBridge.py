import grpc
import os

from google.protobuf import struct_pb2

import src.logWrapper as logWrapper

#from src.simulation import Simulation
from concurrent import futures
from src.simulationparameter import Simulationparameter
from shapely.geometry import Point
from src.uav import Uav

import time
import sys
import psutil

from proto import airmobisim_pb2_grpc
from proto import airmobisim_pb2

class AirMobiSim(airmobisim_pb2_grpc.AirMobiSimServicer):
    index=[]
    x=[]
    y=[]            # these list are loaded by omnet   organization needed for multiple waypoint values
    z=[]
    # index = [0, 1]
    # x = [6.5, 6.8]      # harcoded onnet values for testing
    # y = [10, 10]
    # z = [3, 3]

    def __init__(self, simulation_obj):
        self._isRunning = False
        self._isInitialized = True
        self.simulation_obj = simulation_obj
        self._lastUavReport = []
        self.finish = False

    def startSimulation(self):
        self.simulation_obj.initializeNodes()
        self._isRunning = True

    def Start(self, request, context):
        logWrapper.debug("Starting GRPC Server", True)
        return struct_pb2.Value()

    def ExecuteOneTimeStep(self, request, context):
        """
            Execute one timestep - Update the values (positions, velocity,...)
        """
        responseQuery = airmobisim_pb2.ResponseQuery()
        if not self._isRunning:
            self.startSimulation()
            for node in self.simulation_obj._managedNodes:
                startPos = node._mobility._startPos
                uav = airmobisim_pb2.Response(id=node._uid, x=startPos.x, y=startPos.y, z=startPos.z)
                responseQuery.responses.append(uav)

            Simulationparameter.incrementCurrentSimStep()

            return responseQuery
        else:
            # rt = Repeatedtimer(1, self.printStatus, "World")
            if Simulationparameter.currentSimStep < self.simulation_obj._simulationSteps:
                self._lastUavReport = []
                for node in self.simulation_obj._managedNodes:
                    flag = node.getMobility().makeMove()
                    if flag:
                        
                        logWrapper.debug('removing node ' +node._uid,  True)
                        self.simulation_obj._managedNodes.remove(node)

                    self._isInitialized = True
                    currentPos = node.getMobility().getCurrentPos()
                    uav = airmobisim_pb2.Response(id=node._uid, x=currentPos.x, y=currentPos.y, z=currentPos.z, speed=node.getMobility()._move.getSpeed(), angle=node.getMobility()._angle)
                    self._lastUavReport.append(uav)
                    responseQuery.responses.append(uav)

                Simulationparameter.incrementCurrentSimStep()
                return responseQuery

            else:
                logWrapper.debug("Simulation finished", True)
                self.simulation_obj.finishSimulation()

    def Finish(self, request, context):
        ending = True
        return struct_pb2.Value()

    def GetManagedHosts(self, request, context):
        responseQuery = airmobisim_pb2.ResponseQuery()
        if not self._isRunning:
            self.startSimulation() 

        logWrapper.debug("GetManagedHosts gets called -> " + str(len(self.simulation_obj._managedNodes)), True)
        for node in self.simulation_obj._managedNodes:
            if self._isInitialized:
                node._mobility.makeMove()
                self._isInitialized = True
            currentPos = node._mobility.getCurrentPos()
            uav = airmobisim_pb2.Response(id=node._uid, x=currentPos.x, y=currentPos.y, z=currentPos.z,
                                          speed=node.getMobility()._move.getSpeed(), angle=node.getMobility()._angle)  # TODO: Make speed a correct parameter
            responseQuery.responses.append(uav)
        return responseQuery

    def InsertWaypoints(self, request, context):
        for i in range(0, len(request.waypoints)):
            AirMobiSim.index.append(request.waypoints[i].index)
            AirMobiSim.x.append(request.waypoints[i].x)
            AirMobiSim.y.append(request.waypoints[i].y)
            AirMobiSim.z.append(request.waypoints[i].z)
        return struct_pb2.Value()
    
    @staticmethod
    def getWaypointsByIndex():
        if len(AirMobiSim.index)==0:
            return None,None, None,None

        return AirMobiSim.index, AirMobiSim.x, AirMobiSim.y,AirMobiSim.z


    def InsertUAV(self, request, context):
        """
        Method inserts an UAV in simulation
        In the next timestep makeMove()
        """
        print("Insert UAV with ID " + str(request.id), flush=True)
        # TODO: Check if ID already exists
        self.simulation_obj._managedNodes.append(Uav(request.id, Point(request.coordinates[0].x, request.coordinates[0].y, request.coordinates[0].z), Point(request.coordinates[1].x, request.coordinates[1].y, request.coordinates[1].z), angle=request.angle, speed=request.speed))
        
        return struct_pb2.Value()

    def DeleteUAV(self, request, context):
       """
       Delete UAV with the given Id
       """
       logWrapper.debug("DeleteUAV called: UAV to delete" + request.num, True)
       for node in range(len(self.simulation_obj._managedNodes)):
           if self.simulation_obj._managedNodes[node]._uid == request.num:
                self.simulation_obj._managedNodes.pop(node)
                break

       return struct_pb2.Value()

    def getMaxUavId(self, request, context):
        return airmobisim_pb2.Number(num=self.simulation_obj.getNextUid()-1)
         

    def getNumberCurrentUAV(self, request, context):
      """
       Return the number for current UAVs
      """
      currentUav = len(self.simulation_obj._managedNodes) 

      return airmobisim_pb2.Number(num=currentUav)


    def SetDesiredSpeed(self, request, context):
        """
        Set the desired speed for the given uav
        """
        for node in self.simulation_obj._managedNodes:
            if node._uid == request.id:
                node.getMobility()._move.setSpeed(request.speed)
                break

        return struct_pb2.Value()


    def UpdateWaypoints(self, request, context):
        """
        Update waypoints for a given uav
        """
        logWrapper.debug("Update waypoints called")

        return struct_pb2.Value()

    def DeleteWaypoint(self, request, context):
        pass
        return struct_pb2.Value() 

def startServer(simulation_object):
    """
        Start the AirMobiSim Server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    airmobisim_object = AirMobiSim(simulation_object)
    airmobisim_pb2_grpc.add_AirMobiSimServicer_to_server(airmobisim_object, server)
    server.add_insecure_port('localhost:50051')
    server.start()

    logWrapper.info("AirMobiSim Server started", True) 
    ppid = os.getppid()
    omnetpp_pid_valid = False
    grandparent_pid = psutil.Process(os.getppid()).ppid()

    try:
        while True:
            time.sleep(1) 
            #Check whether the OMNeT-process is running
            if psutil.Process(os.getppid()).ppid() != grandparent_pid:
                server.stop(0)
                sys.exit(1)
    except:
        server.stop(0)
        sys.exit(1)
