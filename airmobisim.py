#!/usr/bin/env python3

import argparse
import os
import sys
from os.path import exists
import pathlib

from proto.DroCIBridge import startServer
from src.plotting import make_plot
from src.resultcollection import Resultcollection
from src.simulation import Simulation
from src.yamlparser import Yamlparser

simulation: Simulation


def main():
    global simulation

    parser = argparse.ArgumentParser(description='Importing configuration-file')
    parser.add_argument('--plot', type=int, required=False, default=0, help='plot vs no plot')
    parser.add_argument('--configuration', action='store', type=str,
                        default="examples/simpleSimulation/simulation.config", help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OmNet++ simulator')
    parser.add_argument('--show', action='store_true', help='Show the Energy as Plot')

    print(
        """AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""",
        flush=True)
    args = parser.parse_args()
    try:
        homePath = os.environ['AIRMOBISIMHOME']
    except KeyError:
        print("AIRMOBISIMHOME-Variable missing. Please do run 'export AIRMOBISIMHOME=" + str(
            pathlib.Path().resolve()) + "' or copy the statement to your .bashrc, .profile, or .zshrc")
        sys.exit()

    configPath = homePath + "/" + args.configuration
    if not exists(configPath):
        print(
            "The configuration file " + configPath + " does not exist. Please check the path or run AirMobiSim with the --help option ")
        sys.exit()
    p = Yamlparser(configPath)
    config = p.readConfig()

    validateConfiguration(config)

    # flags to refer kinetic model selection
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']
    # polygon_file= config['files']['polygon']
    # poly_file_path= str(pathlib.Path().resolve())+'/'+polygon_file
    # print(pathlib.Path().resolve().parent)

    directory = pathlib.Path(args.configuration).parent.resolve()
    initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag)

    # Start the DroCI Bridge - Listen to OmNet++ incomes
    if args.show:
        result = Resultcollection()
        result.showEnergy()
    else:
        if args.omnetpp:
            print("Start the AirMobiSim Server.....", flush=True)
            startServer(simulation)
        else:
            simulation.startSimulation()
            print('FINISH')
        if args.plot:
            make_plot()


def validateConfiguration(config):
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']
    collision_action = config['obstacle_detection']['collision_action']

    if not ((linearMobilityFlag == 0 or linearMobilityFlag == 1) and (
            splineMobilityFlag == 0 or splineMobilityFlag == 1)):
        sys.exit('Please only use value 0 or 1 for selecting kinetic model')

    if linearMobilityFlag == splineMobilityFlag:
        sys.exit('Please select either linear or spline mobility')

    if config['simulation']['simTimeLimit'] < 0:
        sys.exit('Please select a positive simulation time limit')

    if config['simulation']['stepLength'] < 0:
        sys.exit('Please select a positive step length')

    if config['simulation']['playgroundSizeX'] < 0 or config['simulation']['playgroundSizeY'] < 0 or \
            config['simulation']['playgroundSizeZ'] < 0:
        sys.exit("Please select a positive playground size")

    if not (collision_action == 1 or collision_action == 2 or collision_action== 3):
        sys.exit('The value of collision_action can either be 1, 2 or 3')


def initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag):
    global simulation
    if splineMobilityFlag:
        print("Launch spline mobility")
        simulation = Simulation.from_config_spmob(config, linearMobilityFlag, splineMobilityFlag, directory)

    else:
        print("Launch linear mobility")
        # simulation = Simulation.from_config_linmob(config, linearMobilityFlag, splineMobilityFlag, directory)
        polygon_file = config['obstacle_detection']['polygon_file']
        homePath = os.environ['AIRMOBISIMHOME']

        polygon_file_path = homePath + '/' + polygon_file

        simulation = Simulation(directory,
                                config['simulation']['stepLength'],
                                config['simulation']['simTimeLimit'],
                                config['simulation']['playgroundSizeX'],
                                config['simulation']['playgroundSizeY'],
                                config['simulation']['playgroundSizeZ'],
                                linearMobilityFlag,
                                splineMobilityFlag,
                                config['uav'],
                                polygon_file_path,
                                config['obstacle_detection']['collision_action'])


if __name__ == "__main__":
    main()
