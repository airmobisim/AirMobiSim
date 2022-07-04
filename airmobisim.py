#!/usr/bin/env python3

import argparse
import os
import sys
from os.path import exists
import pathlib
import src.logWrapper as logWrapper
import logging

from proto.DroCIBridge import startServer
from src.plotting import make_plot
from src.resultcollection import Resultcollection
from src.simulation import Simulation
from src.yamlparser import Yamlparser
from shapely.geometry import Point

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

        print("AIRMOBISIMHOME-Variable missing. Please do run 'export AIRMOBISIMHOME=" + str(pathlib.Path().resolve()) + "' or copy the statement to your .bashrc, .profile, or .zshrc")
        logWrapper.critical("AIRMOBISIMHOME-Variable missing. Please do run 'export AIRMOBISIMHOME=" + str(pathlib.Path().resolve()) + "' or copy the statement to your .bashrc, .profile, or .zshrc")


        sys.exit()

    configPath = homePath + "/" + args.configuration
    if not exists(configPath):

        print("The configuration file " + configPath + " does not exist. Please check the path or run AirMobiSim with the --help option ")
        logWrapper.critical("The configuration file " + configPath + " does not exist. Please check the path or run AirMobiSim with the --help option ")

        sys.exit()    
    
    logWrapper.basicConfig(filename=os.path.dirname(args.configuration) + '/logfile.log', encoding='utf-8', level=logging.DEBUG)

    p = Yamlparser(configPath)
    config = p.readConfig()

    validateConfiguration(config)

    # flags to refer kinetic model selection
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']

    directory = pathlib.Path(args.configuration).parent.resolve()
    initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag)

    # Start the DroCI Bridge - Listen to OmNet++ incomes
    if args.show:
        result = Resultcollection()
        result.showEnergy()
    else:
        if args.omnetpp:
            logWrapper.info("Start the AirMobiSim Server.....", True)
            startServer(simulation)
        else:
            simulation.startSimulation()
            logWrapper.info('FINISH', True)
        if args.plot:
            make_plot()


def validateConfiguration(config):
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']
    collision_action = config['obstacle_detection']['collision_action']
    splineUavs = config['uavsp']
    linearUavs = config['uav']
    polygon_file = config['obstacle_detection']['polygon_file']

    if polygon_file is None:
        logWrapper.critical('polygon file path is not provided')
        sys.exit('polygon file path is not provided')

    homePath = os.environ['AIRMOBISIMHOME']
    polygon_file_path = homePath + '/' + polygon_file

    # inputs for splinemobility
    speed_sp = []
    waypointX = []
    waypointY = []
    waypointZ = []

    if splineUavs is not None:
        for uavsp in splineUavs:
            waypointX.append(uavsp['waypointX'])
            waypointY.append(uavsp['waypointY'])
            waypointZ.append(uavsp['waypointZ'])
            speed_sp.append(uavsp['speed'])

    # inputs for linear mobility
    startPos = []
    endPos = []
    speed_lin = []

    if linearUavs is not None:
        for uavlin in linearUavs:
            startPos.append(Point(uavlin['startPosX'], uavlin['startPosY'], uavlin['startPosZ']))
            endPos.append(Point(uavlin['endPosX'], uavlin['endPosY'], uavlin['endPosZ']))
            speed_lin.append(uavlin['speed'])



    if not ((linearMobilityFlag == 0 or linearMobilityFlag == 1) and (
            splineMobilityFlag == 0 or splineMobilityFlag == 1)):
        sys.exit('Please only use value 0 or 1 for selecting kinetic model')

    if linearMobilityFlag == splineMobilityFlag:

        print("Please select either linear or spline mobility")
        logWrapper.critical("Please select either linear or spline mobility")
        sys.exit()
    if config['simulation']['simTimeLimit'] < 0:
        print("Please select a positive simulation time limit")
        logWrapper.critical("Please select a positive simulation time limit")
        sys.exit()

    if config['simulation']['stepLength'] < 0:
        print("Please select a positive step length")
        logWrapper.critical("Please select a positive step length")
        sys.exit()

    if config['simulation']['playgroundSizeX'] < 0 or config['simulation']['playgroundSizeY'] < 0 or config['simulation'][
        'playgroundSizeZ'] < 0:
        print("Please select a positive playground size")
        logWrapper.critical("Please select a positive playground size")
        sys.exit()

    if not (collision_action == 1 or collision_action == 2 or collision_action == 3):
        logWrapper.critical("The value of collision_action can either be 1, 2 or 3")
        sys.exit('The value of collision_action can either be 1, 2 or 3')

    if linearMobilityFlag == 1 and linearUavs is None:
        logWrapper.critical("No uav is present in the config file to use linear mobility")
        sys.exit('No uav is present in the config file to use linear mobility')

    if splineMobilityFlag == 1 and splineUavs is None:
        logWrapper.critical('No uavsp is present in the config file to use spline mobility')
        sys.exit('No uavsp is present in the config file to use spline mobility')

    if linearMobilityFlag == 1 and any(uav['speed'] < 0 for uav in linearUavs):
        logWrapper.critical('Speed can not be negative for uav. check config file.')
        sys.exit('Speed can not be negative for uav. check config file.')

    if splineMobilityFlag == 1 and any(uavsp['speed'] < 0 for uavsp in splineUavs):
        logWrapper.critical('Speed can not be negative for uavsp. check config file.')
        sys.exit('Speed can not be negative for uavsp. check config file.')


    if splineMobilityFlag:
        if not (len(waypointX) == len(waypointY) == len(waypointZ)):
            logWrapper.critical('input waypoint length for x,y and z should be same for spline uav')
            sys.exit('input waypoint length for x,y and z should be same for spline uav')

        for i, v in enumerate(waypointX):

            if not (len(waypointX[i]) == len(waypointY[i]) == len(waypointZ[i])):
                logWrapper.critical(f'for uav {i} waypoint x,y,z should be same for each uav')
                sys.exit(f'for uav {i} waypoint x,y,z should be same for each uav')
            if not (all(0 <= item <= config['simulation']['playgroundSizeX'] for item in waypointX[i])):
                logWrapper.critical(f'for uav {i} waypoint x should be within playgroundX.check playground size in config file')
                sys.exit(f'for uav {i} waypoint x should be within playgroundX.check playground size in config file')
            if not (all(0 <= item <= config['simulation']['playgroundSizeY'] for item in waypointY[i])):
                logWrapper.critical(f'for uav {i} waypoint y should be within playgroundY.check playground size in config file')
                sys.exit(f'for uav {i} waypoint y should be within playgroundY.check playground size in config file')
            if not (all(0 <= item <= config['simulation']['playgroundSizeZ'] for item in waypointZ[i])):
                logWrapper.critical(f'for uav {i} waypoint z should be within playgroundZ. check playground size in config file')
                sys.exit(f'for uav {i} waypoint z should be within playgroundZ. check playground size in config file')

    if linearMobilityFlag:
        for startpos, endpos in zip(startPos, endPos):

            if not (0 <= (startpos.x and endpos.x) <= config['simulation']['playgroundSizeX']):
                logWrapper.critical('waypoint x should be within playgroundX. Please check config file.')
                sys.exit('waypoint x should be within playgroundX. Please check config file.')
            if not (0 <= (startpos.y and endpos.y) <= config['simulation']['playgroundSizeY']):
                logWrapper.critical('waypoint y should be within playgroundY. Please check config file.')
                sys.exit('waypoint y should be within playgroundY. Please check config file.')
            if not (0 <= (startpos.z and endpos.z) <= config['simulation']['playgroundSizeZ']):
                logWrapper.critical('waypoint z should be within playgroundZ. Please check config file.')
                sys.exit('waypoint z should be within playgroundZ. Please check config file.')

    if not(os.path.exists(polygon_file_path)):
        logWrapper.critical('no polygon file is found in the path')
        sys.exit('no polygon file is found in the path')




def initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag):
    global simulation
    if splineMobilityFlag:
        logWrapper.debug("Launch spline mobility")
        simulation = Simulation.from_config_spmob(config, linearMobilityFlag, splineMobilityFlag, directory)

    else:

        logWrapper.debug("Launch linear mobility")
        #simulation = Simulation.from_config_linmob(config, linearMobilityFlag, splineMobilityFlag, directory)
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
