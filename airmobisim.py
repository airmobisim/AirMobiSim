#!/usr/bin/python3
import sys
import argparse
import pathlib

from src.simulation import Simulation
from src.simpleapp import Simpleapp

from src.yamlparser import Yamlparser

from src.resultcollection import Resultcollection


from proto.DroCIBridge import startServer

simulation: Simulation


def main():
    global simulation
    parser = argparse.ArgumentParser(description='Importing configuration-file')
    parser.add_argument('--configuration', action='store', type=str,
                        default="examples/simpleSimulation/simulation.config", help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OmNet++ simulator')

    parser.add_argument('--show', action='store_true', help='Show the Energy as Plot')



    print(
        """AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""")

    args = parser.parse_args()

    # Start the DroCI Bridge - Listen to OmNet++ incomes

    p = Yamlparser(args.configuration)
    config = p.readConfig()
    directory = pathlib.Path(args.configuration).parent.resolve()
    initializeSimulation(config, directory)

    if args.show:
        hello = Resultcollection()
        hello.showEnergy()
    else:
        if args.omnetpp:
            print("Start the AirMobiSim Server.....")
            startServer(simulation)
        else:
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
