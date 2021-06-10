#!/usr/local/bin/python3
import sys
import argparse

from src import Simulation
from src.utils import Jsonparser

def main():
    parser = argparse.ArgumentParser(description='Nobody needs this right now')
    parser.add_argument('configuration',  action='store', type=str, default="examples/simpleSimulation/simulation.config", help='an integer for the accumulator')
    print("""AirMobiSim Simulation  (C) 2021 Chair of Networked Systems Modelling TU Dresden.\nVersion: 0.0.1\nSee the license for distribution terms and warranty disclaimer""")

    args = parser.parse_args()
    
    p = Jsonparser(args.configuration)
    config = p.readConfig()
    
    initializeSimulation(config)

def initializeSimulation(config):
    simulation = Simulation(config['stepLength'],
            config['simTimeLimit'],
            config['playgroundSizeX'],
            config['playgroundSizeY'],
            config['playgroundSizeZ'],
    )

    

if __name__ == "__main__":
    main()

