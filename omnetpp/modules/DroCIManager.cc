#include "airmobisim.pb.h"

#//include "DroCIManager.h"

#include <string.h>


#include <cstdlib>
#include <iostream>
#include <regex>
#include <sstream>

#include <boost/process.hpp>
#include <google/protobuf/empty.pb.h>
#include <grpcpp/grpcpp.h>

#include <omnetpp.h>

#include <common/InitStages.h>
#include <common/scenario/ScenarioManager.h>



namespace bp = boost::process;

using namespace omnetpp;


Define_Module(DroCIManager);

void DroCIManager::initialize(int stage)
{
    if (stage == inet::INITSTAGE_LOCAL) {
        moduleType = par("moduleType").stdstringValue();
        moduleName = par("moduleName").stdstringValue();

        updateInterval = par("updateInterval")

        //Create a connection with AirMobiSim Server
        launchSimulator();

        // Do not create children here since OMNeT++ will try to initialize them again
        initMsg = new cMessage("init");

        scheduleAt(simTime(), initMsg);

        executeOneTimestepTrigger = new cMessage("step")

    }
}


void DroCIManager::handleSelfMsg(cMessage* msg)
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

    _simulatorChannel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    if (!_simulatorChannel->WaitForConnected(
            gpr_time_add(gpr_now(GPR_CLOCK_REALTIME), gpr_time_from_seconds(3, GPR_TIMESPAN)))) {
        throw cRuntimeError("Failed to connect to AirMobiSim");
    }

    _simulatorStub = airmobsim::AirMobiSim::NewStub(_simulatorChannel);

    google::protobuf::Empty empty;
    grpc::ClientContext clientContext;
    grpc::Status status = _simulatorStub->Start(&clientContext, empty, &empty);
    if (!status.ok()) {
        throw cRuntimeError("Failed to initialize simulation");
    }

    executeOneTimestamp();

}


void DroCIManager::executeOneTimestep()
{
    EV_DEBUG << "Triggering AirMobiSim simulator advance to t=" << simTime() << endl;

    simtime_t targetTime = simTime();


    airmobisim::Response response;
    google::protobuf::Empty empty;
    grpc::ClientContext clientContext;
    grpc::Status status = _simulatorStub->ExecuteOneTimeStamp(&clientContext, empty, &response);


    if(status.ok()){

        
        //for (uint32_t i = 0; i < count; ++i) 
        //{
        EV_DEBUG << "Getting " << response.message() << " subscription results" << endl;
        //}

    //else {
        //std::cout << status.error_code() << ": " << status.error_message() << std::endl;
        //return -1;
        //}    

    }

    scheduleAt(simtime() + updateInterval, executeOneTimestepTrigger)
    
}



