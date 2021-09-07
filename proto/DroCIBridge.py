import grpc
from src.simulation import Simulation
from concurrent import futures
from src.simulationparameter import Simulationparameter

import time
#from src.repeatedtimer import Repeatedtimer
from proto import airmobisim_pb2_grpc
from proto import airmobisim_pb2


class AirMobiSim(airmobisim_pb2_grpc.AirMobiSimServicer):

    def __init__(self, simulation_obj):
        self._isRunning = False
        self.simulation_obj = simulation_obj

    def Start(self, request, context):
        pass    

    def ExecuteOneTimeStep(self, request, context):
        """
            Execute one timestep - Update the values (positions, velocity,...)
        """
        responseQuery = airmobisim_pb2.ResponseQuery()

        if not self._isRunning:

            self.simulation_obj.initializeNodes()
            self._isRunning = True 

            for node in self.simulation_obj._managedNodes:
                startPos = node._mobility._startPos

                uav = airmobisim_pb2.Response(id=node._uid,x=startPos.x, y=startPos.y, z=startPos.z)
                responseQuery.responses.append(uav)

            Simulationparameter.incrementCurrentSimStep()

            return responseQuery
        else:
            #rt = Repeatedtimer(1, self.printStatus, "World")

            if Simulationparameter.currentSimStep < self.simulation_obj._simulationSteps:
                for node in self.simulation_obj._managedNodes:
                    node._mobility.makeMove()
                    currentPos = node._mobility.getCurrentPos()

                    uav = airmobisim_pb2.Response(id=node._uid,x=currentPos.x, y=currentPos.y, z=currentPos.z)
                    responseQuery.responses.append(uav)

                Simulationparameter.incrementCurrentSimStep()    
                return responseQuery

            else: 
                #rt.stop()
                self.simulation_obj.finishSimulation()

        currentNodes = self.simulation_obj.getNodes()

    def Finish(self, request, context):
        pass


def startServer(simulation_object):
    """
        Start the AirMobiSim Server
    """

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    airmobisim_pb2_grpc.add_AirMobiSimServicer_to_server(AirMobiSim(simulation_object), server)
    server.add_insecure_port('localhost:50051')
    server.start()

    print("AirMobiSim Server has started....")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
        print("Server has been stopped")

