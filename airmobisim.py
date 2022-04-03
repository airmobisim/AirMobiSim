#!/usr/bin/env python3
import sys
import argparse
import pathlib
import os

from shapely.geometry import Point
from src.simulation import Simulation
from src.simpleapp import Simpleapp

from src.yamlparser import Yamlparser

from src.resultcollection import Resultcollection
from src.plotting import  make_plot
from pathlib import Path

from proto.DroCIBridge import startServer

simulation: Simulation


def main():
    global simulation

    parser = argparse.ArgumentParser(description='Importing configuration-file')
    parser.add_argument('--plot', type=int, required=False, default=1, help='plot vs no plot')
    parser.add_argument('--configuration', action='store', type=str,
                        default=Path("examples/simpleSimulation/simulation.config").resolve(), help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OmNet++ simulator')

    parser.add_argument('--show', action='store_true', help='Show the Energy as Plot')


    print("""AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""")

    args = parser.parse_args()

    p = Yamlparser(args.configuration)
    config = p.readConfig()

    # flags to refer kinetic model selection
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']

    '''
    ####################################
    
    the code within this ###s are only for the input of spline mobility it is a redundant code which should be removed during final merge.
    

    speed = []
    waypointX = []
    waypointY = []
    waypointZ = []


    if splineMobilityFlag:
        # uavStartPos.clear(), uavEndPos.clear(), totalFlightTime.clear(), waypointTime.clear(), waypointX.clear(), waypointY.clear(), waypointZ.clear()

        for uavsp in config['uavsp']:
            waypointX.append(uavsp['waypointX'])
            waypointY.append(uavsp['waypointY'])
            waypointZ.append(uavsp['waypointZ'])
            speed.append(uavsp['speed'])


    #####################################
    '''
    directory = pathlib.Path(args.configuration).parent.resolve()
    initializeSimulation(config, directory, linearMobilityFlag,splineMobilityFlag)

    # Start the DroCI Bridge - Listen to OmNet++ incomes
    if args.show:
        result = Resultcollection()
        result.showEnergy()
    else:
        if args.omnetpp:
            print("Start the AirMobiSim Server.....")
            startServer(simulation)
        else:
            simulation.startSimulation()
            print('FINISH')
        if args.plot:
            make_plot()

def initializeSimulation(config, directory, linearMobilityFlag,splineMobilityFlag):
    global simulation
    if splineMobilityFlag:
        print("Launch spline mobility")
        simulation = Simulation.from_config_spmob(config, linearMobilityFlag, splineMobilityFlag, directory)
        # simulation = Simulation(config['simulation']['stepLength'],
        #                         config['simulation']['simTimeLimit'],
        #                         config['simulation']['playgroundSizeX'],
        #                         config['simulation']['playgroundSizeY'],
        #                         config['simulation']['playgroundSizeZ'],
        #                         config['uavsp'],
        #                         speed,
        #                         waypointX,
        #                         waypointY,
        #                         waypointZ,
        #                         linearMobilityFlag,
        #                         splineMobilityFlag,
        #                         directory,
        #                         )

    else:
        print("Launch linear mobility")
        simulation = Simulation.from_config_linmob(config, linearMobilityFlag, splineMobilityFlag, directory)
        # simulation = Simulation(config['simulation']['stepLength'],
        #                         config['simulation']['simTimeLimit'],
        #                         config['simulation']['playgroundSizeX'],
        #                         config['simulation']['playgroundSizeY'],
        #                         config['simulation']['playgroundSizeZ'],
        #                         config['uav'],
        #                         speed,
        #                         waypointX,
        #                         waypointY,
        #                         waypointZ,
        #                         linearMobilityFlag,
        #                         splineMobilityFlag,
        #                         directory,
        #                         )



if __name__ == "__main__":
    main()
