#!/usr/local/bin/python3
import sys
import argparse

from src import Simulation
from src.jsonparser import Jsonparser
from src.simpleapp import Simpleapp


simulation: Simulation

def main():
    global simulation
    parser = argparse.ArgumentParser(description='Nobody needs this right now')
    parser.add_argument('configuration',  action='store', type=str, default="examples/simpleSimulation/simulation.config", help='an integer for the accumulator')
    print("""AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""")

    args = parser.parse_args()
    
    p = Jsonparser(args.configuration)
    config = p.readConfig()
    initializeSimulation(config)
    simulation.startSimulation()

def initializeSimulation(config):
    global simulation
    simulation = Simulation(config['stepLength'],
            config['simTimeLimit'],
            config['playgroundSizeX'],
            config['playgroundSizeY'],
            config['playgroundSizeZ'],
            config['uavs'],
    )

    

if __name__ == "__main__":
    main()

