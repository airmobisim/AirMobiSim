# AirmobiSim Project 

## Pre-Installation 

AirMobiSim can be used standalone (pure Python kinematic simulation) or coupled with
OMNeT++/veins for wireless communication simulation. The OMNeT++ coupling is optional.

For the standalone simulator, you only need:

- curl
- pyenv
- poetry

If you also want the OMNeT++/veins coupling, you additionally need:

- OMNeT++ 6
- conan

### OMNeT 6 installation (only needed for the OMNeT++ coupling)
Please do follow the instructions from the official [OMNeT documentation](https://doc.omnetpp.org/omnetpp/InstallGuide.pdf)


### Conan installation (only needed for the OMNeT++ coupling)
Please do follow the instructions from the official [conan documentation](https://docs.conan.io/en/latest/installation.html)


### Curl installation
To install curl please do execute:

Linux/Debian
```sudo apt install curl```


MacOS
```brew install curl```

### Poetry installation
Please do follow the instructions from the official [poetry documentation](https://python-poetry.org/docs/#installation), e.g.:
```Bash
curl -sSL https://install.python-poetry.org | python3 -
```
This installs poetry to `~/.local/bin`, which most Linux distributions (Debian/Ubuntu
included) already add to `PATH` automatically for login shells - open a new shell (or
re-source your `.bashrc`/`.zshrc`) after installing so `poetry` is picked up before
running `build.sh`.

---

## AirMobiSim-Installation
All required dependencies are locally installed using pyenv and poetry by executing the ```build.sh``` script:
```Bash
./build.sh
```
This installs the standalone Python simulator only (no OMNeT++/conan required).

To also set up the OMNeT++/veins coupling (clones and compiles veins and
AirMobiSim_libveins; requires OMNeT++ and conan to be installed), run instead:
```Bash
./build.sh --with-omnet
```
Without `-y`/`--non-interactive`, the script will also ask interactively whether to set
up the OMNeT++ coupling. Conan's state (profiles, package cache) is kept scoped to the
project directory (`.conan_home/`) rather than touching your global `~/.conan2`.

**Note:** if you have OMNeT++'s own `setenv` script sourced in your shell (needed to get
`opp_run` etc. on `PATH`), it may also put OMNeT++'s bundled Python distribution ahead in
`PATH` and export `PYTHONHOME`/`PYTHONPATH`. `build.sh` clears these for its own run, but
if you run `poetry install` or `poetry run ./airmobisim.py` manually afterwards in a shell
where OMNeT++'s `setenv` is sourced, unset them first:
```Bash
unset PYTHONHOME PYTHONPATH
```
Otherwise poetry/pyenv may end up targeting OMNeT++'s bundled Python instead of this
project's own environment, which can silently break either one.

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
