#!/usr/bin/env python3
#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
# Copyright (C) 2022 Dalisha Logan <dalisha@mail.uni-paderborn.de>
# Copyright (C) 2022 Touhid Hossain Pritom <pritom@campus.uni-paderborn.de>
#
# Documentation for these modules is at http://veins.car2x.org/
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

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
    parser.add_argument('--configuration', action='store', type=str, default="examples/simpleSimulation/simulation.config", help='configuration')
    parser.add_argument('--omnetpp', action='store_true', help='Start the OMNeT++ simulator')
    parser.add_argument('--show', action='store_true', help='Show the Energy as Plot')
    parser.add_argument('--r', type=int, default=0, help='Specifies the runnumber that is used as the seed')

    print("""AirMobiSim Simulation (C) 2022 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""", flush=True)
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
    


    p = Yamlparser(configPath)
    config = p.readConfig()

    loglevel = config['logging']['loglevel']
    if loglevel == "DEBUG":
        ll = logging.DEBUG
    elif loglevel == "INFO":
        ll = logging.INFO
    elif loglevel == "WARNING":
        ll = logging.WARNING
    elif loglevel ==  "ERROR":
        ll = logging.ERROR
    elif loglevel == "CRITICAL":
        ll = logging.CRITICAL
    else:
        print("CRITICAL: Invalid loglevel set. Please check the value in the config file!")
        sys.exit()

    if (exists(os.path.dirname(args.configuration) + '/logfile.log')): # Remove logfile if it already exists
        os.remove(os.path.dirname(args.configuration) + '/logfile.log')

    logNumber = 0
    freeLogNumberFound = False
    while not freeLogNumberFound:
        if (exists(os.path.dirname(args.configuration) + '/logfile' + str(logNumber) + '.log')):
            logNumber += 1
        else:
            freeLogNumberFound = True

    logWrapper.basicConfig(filename=os.path.dirname(args.configuration) + '/logfile' + str(logNumber) + '.log',
                           encoding='utf-8', level=ll)

    validateConfiguration(config)

    # flags to refer kinetic model selection
    linearMobilityFlag = config['kinetic_model']['linearMobility']
    splineMobilityFlag = config['kinetic_model']['splineMobility']

    directory = pathlib.Path(args.configuration).parent.resolve()
    initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag, args.r)

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


def checkNumeric(fieldValue, fieldName):
    try:
        float(fieldValue)
    except ValueError:
        logWrapper.critical(str(fieldName) + " is not a numeric value!")
        sys.exit()
    return True



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
        sys.exit('Please only use value 0 or 1 for selecting the kinetic model')

    if linearMobilityFlag == splineMobilityFlag:

        logWrapper.critical("Please select either linear or spline mobility")
        sys.exit()

    simTimeLimit = config['simulation']['simTimeLimit']
    checkNumeric(simTimeLimit, "simTimeLimit")
    if simTimeLimit < 0:
        logWrapper.critical("simTimeLimit must be greater than zero. Please select a valid value.")
        sys.exit()


    stepLength = config['simulation']['stepLength']
    checkNumeric(stepLength, "stepLength")
    if stepLength < 0:
        logWrapper.critical("stepLength must be greater than zero. Please select a valid value.")
        sys.exit()

    playgroundSizeX = config['simulation']['playgroundSizeX']
    playgroundSizeY = config['simulation']['playgroundSizeY']
    playgroundSizeZ = config['simulation']['playgroundSizeZ']
    checkNumeric(playgroundSizeX, "playgroundSizeX")
    checkNumeric(playgroundSizeY, "playgroundSizeY")
    checkNumeric(playgroundSizeZ, "playgroundSizeZ")

    if playgroundSizeX < 0 or playgroundSizeY < 0 or playgroundSizeZ < 0:
        logWrapper.critical("playgroundSizeX must be greater than zero. Please select a valid value.")
        sys.exit()

    if not (collision_action == 1 or collision_action == 2 or collision_action == 3):
        logWrapper.critical("The value of collision_action can either be 1, 2 or 3")
        sys.exit()

    if linearMobilityFlag == 1 and linearUavs is None:
        logWrapper.critical("No uav is present in the config file to use linear mobility")
        sys.exit()

    if splineMobilityFlag == 1 and splineUavs is None:
        logWrapper.critical('No uavsp is present in the config file to use spline mobility')
        sys.exit()

    if linearMobilityFlag == 1 and (any(not checkNumeric(uav['speed'], "uavSpeed (linearMobility)") for uav in linearUavs) or \
                                    any(uav['speed'] < 0 for uav in linearUavs)):
        logWrapper.critical('uav speed must not be negative.')
        sys.exit()

    if splineMobilityFlag == 1 and (any(not checkNumeric(uavsp['speed'], "uavSpeed (splineMobility)") for uavsp in splineUavs) or \
                                    any(uavsp['speed'] < 0 for uavsp in splineUavs)):
        logWrapper.critical('uavsp speed must not be negative.')
        sys.exit()

    if splineMobilityFlag:
        if not (len(waypointX) == len(waypointY) == len(waypointZ)):
            logWrapper.critical("Waypoint vectors must be of equal length!")
            sys.exit()

        for i, v in enumerate(waypointX):
            if not (len(waypointX[i]) == len(waypointY[i]) == len(waypointZ[i])):
                logWrapper.critical(f'for uav ' + str(i) + ' waypoint x,y,z needs to be the same for each uav')
                sys.exit()
            if not (all(0 <= item <= config['simulation']['playgroundSizeX'] for item in waypointX[i])):
                logWrapper.critical(f'for uav ' + str(i) + ' waypoint x needs to be within playgroundX. Check playground size in config file')
                sys.exit()
            if not (all(0 <= item <= config['simulation']['playgroundSizeY'] for item in waypointY[i])):
                logWrapper.critical(f'for uav ' + str(i) + ' waypoint y needs to be within playgroundY. Check playground size in config file')
                sys.exit()
            if not (all(0 <= item <= config['simulation']['playgroundSizeZ'] for item in waypointZ[i])):
                logWrapper.critical(f'for uav ' + str(i) + ' waypoint z needs to be within playgroundZ. Check playground size in config file')
                sys.exit()

    if linearMobilityFlag:
        for startpos, endpos in zip(startPos, endPos):
            if not (0 <= (startpos.x and endpos.x) <= config['simulation']['playgroundSizeX']):
                logWrapper.critical('Waypoint x should be within playgroundX. Please check config file.')
                sys.exit()
            if not (0 <= (startpos.y and endpos.y) <= config['simulation']['playgroundSizeY']):
                logWrapper.critical('Waypoint y should be within playgroundY. Please check config file.')
                sys.exit()
            if not (0 <= (startpos.z and endpos.z) <= config['simulation']['playgroundSizeZ']):
                logWrapper.critical('Waypoint z should be within playgroundZ. Please check config file.')
                sys.exit()

    if not(os.path.exists(polygon_file_path)):
        logWrapper.critical('No polygon file was found in the path')
        sys.exit()

def initializeSimulation(config, directory, linearMobilityFlag, splineMobilityFlag, runnumber):
    global simulation
    if splineMobilityFlag:
        logWrapper.debug("Launch spline mobility")
        simulation = Simulation.from_config_spmob(config, linearMobilityFlag, splineMobilityFlag, directory)
    else:
        logWrapper.debug("Launch linear mobility")
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
                                runnumber,
                                polygon_file_path,
                                config['obstacle_detection']['collision_action'])

if __name__ == "__main__":
    main()
