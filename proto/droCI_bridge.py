import airmobisim_pb2
import grpc
from src.simulation import Simulation
from concurrent import futures

import airmobisim_pb2_grpc



from src.repeatedtimer import Repeatedtimer
from src.simulationparameter import Simulationparameter

from proto import airmobisim_pb2_pb2_grpc


class AirMobiSimServicer(airmobisim_pb2_pb2_grpc.AirMobiSimServicer):

    def __init__(self, simulation_obj):
        self.is_running = False
        self.simulation_obj = simulation_obj


    def Start(self, request, context):
        pass    

    def ExecuteOneTimeStep(self, request, context):
        """
            Execute one timestep - Update the values (positions, velocity,...)
        """
        if not self.is_running:

            self.simulation_obj.initializeNodes()
            self.is_running = True  

        else:
            rt = Repeatedtimer(1, self.printStatus, "World")

            if self.simulation_obj.Simulationparameter.currentSimStep < self.simulation_obj._simulationSteps:
                self.simulation_obj.processNextStep()

            else: 
                rt.stop()
                self.simulation_obj.finishSimulation()

        currentNodes = self.simulation_obj.getNodes()

    def Finish(self, request, context):
        pass


def serve():
    """
        Start the AirMobiSim Server
    """

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    airmobisim_pb2_grpc.add_AirMobiSimServicer_to_server(AirMobiSimServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()





if __name__ == '__main__':
    serve()