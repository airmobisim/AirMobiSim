
#include "DroCIManager.h"
#include <google/protobuf/empty.pb.h>
#include <grpcpp/grpcpp.h>

#include <string.h>

using namespace omnetpp;


Define_Module(DroCIManager);

void DroCIManager::initialize(int stage)
{
 

    updateInterval = 1.0;
    stepLength = 0.01;
    simTimeLimit = 50;
    totalsteps = simTimeLimit/stepLength;
    count = 0;


    //Create a connection with AirMobiSim Server

    // Do not create children here since OMNeT++ will try to initialize them again
    initMsg = new cMessage("init");

    scheduleAt(simTime(), initMsg);

    executeOneTimestepTrigger = new cMessage("step");

    
}

void DroCIManager::handleMessage(cMessage* msg)
{
    if (msg == initMsg) {

        launchSimulator();
        return;
    }
    if (msg == executeOneTimestepTrigger) {

        executeOneTimestep();
        return;
    }
    throw cRuntimeError("DroCIManager received unknown self-message");

}


void DroCIManager::launchSimulator()
{

    channel = CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    stub = airmobisim::AirMobiSim::NewStub(channel);
    executeOneTimestep();

}

void DroCIManager::executeOneTimestep()
{
    EV_DEBUG << "Triggering AirMobiSim simulator advance to t=" << simTime() << endl;

    airmobisim::ResponseQuery response;
    google::protobuf::Empty empty;
    grpc::ClientContext clientContext;
    grpc::Status status = stub->ExecuteOneTimeStep(&clientContext, empty, &response);


    if(status.ok()){

        for (uint32_t i = 0; i < response.responses_size(); i++) 
        {
        EV << "Getting for " << response.responses(i).id() << " subscription results" << endl;
        EV <<  "Position" << response.responses(i).y() << endl;
        }

    }

    else 
        {
        std::cout << status.error_code() << ": " << status.error_message() << std::endl;
        }    

    
    count = count + 1;

    if(count < totalsteps)
    {
        scheduleAt(simTime() + updateInterval, executeOneTimestepTrigger);
    }
    else
    {
        EV << "End" << endl;
    }
}



