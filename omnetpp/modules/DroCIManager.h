#pragma once

#include <map>
#include <memory>

#include <omnetpp.h>
#include <cstdlib>
#include <iostream>
#include <regex>
#include <sstream>

#include <google/protobuf/empty.pb.h>
#include <grpcpp/grpcpp.h>
#include "airmobisim.grpc.pb.h"

class DroCIManager : public omnetpp::cSimpleModule
{
protected:
    void initialize(int stage) override;
    void handleMessage(omnetpp::cMessage *msg);


private:
    void launchSimulator();
    void executeOneTimestep();

private:
    std::shared_ptr<grpc::Channel> channel;
    std::unique_ptr<airmobisim::AirMobiSim::Stub> stub;
    double updateInterval;
    double simTimeLimit;
    double stepLength;
    int count;
    double totalsteps;
    omnetpp::cMessage *initMsg;
    omnetpp::cMessage *executeOneTimestepTrigger;

};






