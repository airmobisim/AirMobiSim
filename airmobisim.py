#!/usr/bin/env python3


import sys
import argparse
import pathlib


from src.simulation import Simulation
from src.simpleapp import Simpleapp

from src.yamlparser import Yamlparser

from proto.DroCIBridge import startServer

import os

import errno

import socket
import time

simulation: Simulation

def main():
    global simulation
    parser = argparse.ArgumentParser(description='Importing configuration-file')
    parser.add_argument('--configuration', action='store', type=str, default="examples/simpleSimulation/simulation.config", help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OmNet++ simulator')

    print("""AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""", flush=True)
    args = parser.parse_args()
    homePath = os.environ['AIRMOBISIMHOME']

    p = Yamlparser(homePath + "/" + args.configuration)
    config = p.readConfig()

    directory = pathlib.Path(args.configuration).parent.resolve()
    print(directory, flush=True)
    initializeSimulation(config, directory)

    if args.omnetpp:
        print("Start the AirMobiSim Server...", flush=True)
        #Start the DroCIBridge
        startServer(simulation)
    else:
        #print("Starting the Simulation")
        simulation.startSimulation()



def initializeSimulation(config, directory):
    global simulation
    simulation = Simulation(config['simulation']['stepLength'],
                            config['simulation']['simTimeLimit'],
                            config['simulation']['playgroundSizeX'],
                            config['simulation']['playgroundSizeY'],
                            config['simulation']['playgroundSizeZ'],
                            config['uav'],
                            directory,
                            )


if __name__ == "__main__":    
    main()
