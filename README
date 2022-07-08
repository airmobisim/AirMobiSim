# AirmobiSim Project 

## Pre-Installation 

AirMobiSim requires the following software to be installed 

- OMNeT++ 6
- conan
- curl
- pyenv

### OMNeT 6 installation
Please do follow the instructions from the official [OMNeT documentation](https://doc.omnetpp.org/omnetpp/InstallGuide.pdf)


### Conan installation
Please do follow the instructions from the official [conan documentation](https://docs.conan.io/en/latest/installation.html)



### Curl installation
To install curl please do execute:

Linux/Debian
```sudo apt install curl```


MacOS
```brew install curl```

### Pyenv installation
To install Pyenv please do execute:

Linux / Debian: 
```curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash```


MacOS:
```brew install pyenv```

---

## AirMobiSim-Installation
AirMobiSim requires all installations listed in the section above.
All additional required dependencies will be locally installed using pyenv and poetry by executing the ```build.sh``` script:
```Bash
./build.sh
```

---

## Run AirmobiSim
To run the project use the following command in 'poetry shell':
```Bash
poetry run ./airmobisim.py
```

The above command will run the simulation in command line without any plot.

To run the simulation with plot use :

```Bash
poetry run ./airmobisim.py  --plot 1
```

To get a list of options to use with AirMobiSim, use:

```Bash
poetry run ./airmobisim.py  -h
```

---

## Configure a simulation
The input parameters for the simulations are taken from a file named ```simulation.config```.
An example is located in the ```examples``` directory.

## Logging
A logfile is written to the project directory (e.g., ```AirMobiSim/examples/simpleSimulation```).
The loglevel can be set in the according configuration file.
