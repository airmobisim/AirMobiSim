#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
# Copyright (C) 2022 Dalisha Logan <dalisha@mail.uni-paderborn.de>
# Copyright (C) 2022 Touhid Hossain Pritom <pritom@campus.uni-paderborn.de>
#
# Documentation for these modules is at http://veins.car2x.org/
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import grpc
import os

from google.protobuf import struct_pb2

import src.logWrapper as logWrapper

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
       logWrapper.debug("DeleteUAV called: UAV to delete" + str(request.num), True)
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
        logWrapper.debug("UpdateWaypoints() called")
        raise NotImplementedError()
        return struct_pb2.Value()

    def DeleteWaypoint(self, request, context):
        logWrapper.debug("DeleteWapoint() called")
        raise NotImplementedError()
        return struct_pb2.Value() 

    def InsertWaypoints(self, request, context):
        raise NotImplementedError()  
   
    def InsertWaypoint(self, request, context):
        uav = next((x for x in self.simulation_obj._managedNodes if x._uid == request.uid), None)
        if uav is not None:
            if request.index == -1:
                uav.addWaypoint(Point(request.x, request.y, request.z))
            else:
                raise Exception("Not yet implemented")
        else:
            raise Exception("No such UAV")
        return struct_pb2.Value()

    def GetMaxSimulationTime(self, requests, context):
        return airmobisim_pb2.Number(num=self.simulation_obj.getMaxSimulationTime())

    def getMaxSimulationSteps(self, request, context):
        return airmobisim_pb2.DoubleNumber(num=self.simulation_obj.getMaxSimulationSteps())

    @staticmethod
    def getWaypointsByIndex():
        if len(AirMobiSim.index)==0:
            return None,None, None,None

        return AirMobiSim.index, AirMobiSim.x, AirMobiSim.y,AirMobiSim.z

def startServer(simulation_object):
    """
        Start the AirMobiSim Server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    airmobisim_object = AirMobiSim(simulation_object)
    airmobisim_pb2_grpc.add_AirMobiSimServicer_to_server(airmobisim_object, server)
    grpcPort = server.add_insecure_port('localhost:0')
    logWrapper.info("Server starts on port " + str(grpcPort))
    server.start()

    logWrapper.info("AirMobiSim Server started", True)
    ppid = os.getppid()

    filename = str(ppid) + ".tmp"
    f = open(filename, "a")
    f.write(str(grpcPort))
    f.close()
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
