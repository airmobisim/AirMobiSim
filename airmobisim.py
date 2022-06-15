#!/usr/bin/env python3

import argparse
import os
import sys
from os.path import exists
import pathlib
import src.logWrapper as logWrapper

from proto.DroCIBridge import startServer
from src.plotting import make_plot
from src.resultcollection import Resultcollection
from src.simulation import Simulation
from src.yamlparser import Yamlparser

simulation: Simulation

def main():


    logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)
    global simulation

    parser = argparse.ArgumentParser(description='Importing configuration-file')
    parser.add_argument('--plot', type=int, required=False, default=0, help='plot vs no plot')
    parser.add_argument('--configuration', action='store', type=str,
                        default="examples/simpleSimulation/simulation.config", help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OmNet++ simulator')
    parser.add_argument('--show', action='store_true', help='Show the Energy as Plot')

    print("""AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""", flush=True)
    args = parser.parse_args()
    try:
        homePath = os.environ['AIRMOBISIMHOME']
    except KeyError:
        print("AIRMOBISIMHOME-Variable missing. Please do run 'export AIRMOBISIMHOME=" + str(pathlib.Path().resolve()) + "' or copy the statement to your .bashrc, .profile, or .zshrc")
        logging.critical("AIRMOBISIMHOME-Variable missing. Please do run 'export AIRMOBISIMHOME=" + str(pathlib.Path().resolve()) + "' or copy the statement to your .bashrc, .profile, or .zshrc")

        sys.exit()



    configPath = homePath + "/" + args.configuration
    if not exists(configPath):
        print("The configuration file " + configPath + " does not exist. Please check the path or run AirMobiSim with the --help option ")
        logging.critical("The configuration file " + configPath + " does not exist. Please check the path or run AirMobiSim with the --help option ")

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
            logging.info("Start the AirMobiSim Server.....")
            startServer(simulation)
        else:
            simulation.startSimulation()
            logging.info('FINISH')
        if args.plot:
            make_plot()

def validateConfiguration(config):
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']
    if linearMobilityFlag == splineMobilityFlag:
        print("Please select either linear or spline mobility")
        logging.critical("Please select either linear or spline mobility")

        sys.exit()
    if config['simulation']['simTimeLimit'] < 0:
        print("Please select a positive simulation time limit")
        logging.critical("Please select a positive simulation time limit")

        sys.exit()
    
    if config['simulation']['stepLength'] < 0:
        print("Please select a positive step length")
        logging.critical("Please select a positive step length")

        sys.exit()
    if config['simulation']['playgroundSizeX'] <0 or config['simulation']['playgroundSizeY'] <0 or config['simulation']['playgroundSizeZ'] < 0:
        print("Please select a positive playground size")
        logging.critical("Please select a positive playground size")
        sys.exit()

def initializeSimulation(config, directory, linearMobilityFlag,splineMobilityFlag):
    global simulation
    if splineMobilityFlag:
        logging.debug("Launch spline mobility")
        simulation = Simulation.from_config_spmob(config, linearMobilityFlag, splineMobilityFlag, directory)

    else:
        logging.debug("Launch linear mobility")
        #simulation = Simulation.from_config_linmob(config, linearMobilityFlag, splineMobilityFlag, directory)
        polygon_file = config['files']['polygon']
        homePath = os.environ['AIRMOBISIMHOME']

        polygon_file_path = homePath + '/' + polygon_file
        
        simulation = Simulation( directory,
                                 config['simulation']['stepLength'],
                                 config['simulation']['simTimeLimit'],
                                 config['simulation']['playgroundSizeX'],
                                 config['simulation']['playgroundSizeY'],
                                 config['simulation']['playgroundSizeZ'],
                                 linearMobilityFlag,
                                 splineMobilityFlag,
                                 config['uav'],
                                 polygon_file_path)



if __name__ == "__main__":    
    main()
