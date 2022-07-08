#!/usr/bin/env bash
#
# Copyright (C) 2021 Tobias Hardes <tobias.hardes@uni-paderborn.de>
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

accept_all=false
while [ "$1" != "" ]; do
    case $1 in
        -y | --non-interactive )          shift
                                accept_all=true
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

set -e 


GRPC_VERSION=1.38.1
PROTOC_VERSION=3.17.1




base64 -d <<< "ICAgIF8gICAgXyAgICAgIF9fICBfXyAgICAgICBfICAgICBfIF9fX18gIF8KICAgLyBcICAoXylf
IF9ffCAgXC8gIHwgX19fIHwgfF9fIChfKSBfX198KF8pXyBfXyBfX18KICAvIF8gXCB8IHwgJ19f
fCB8XC98IHwvIF8gXHwgJ18gXHwgXF9fXyBcfCB8ICdfIGAgXyBcCiAvIF9fXyBcfCB8IHwgIHwg
fCAgfCB8IChfKSB8IHxfKSB8IHxfX18pIHwgfCB8IHwgfCB8IHwKL18vICAgXF9cX3xffCAgfF98
ICB8X3xcX19fL3xfLl9fL3xffF9fX18vfF98X3wgfF98IHxffA=="
echo -e "\n=====================================================================
The open-source unmanned aerial vehicle simulation framework
====================================================================="
echo "AirMobiSim requires the following software to be installed:"
echo "OMNeT++ 6"
echo "conan.io - version: 1.44.1"
echo "curl"
echo "pyenv"

echo "This setup installs all required Python packages (and poetry), loads the AirMobiSim extension from Veins, installs native binaries and libs from GRPC (version $GRPC_VERSION) and Protobuf ($PROTOC_VERSION) using conan.io.

The complete source code is compiled afterwards."
if ! $accept_all
then
    read -p "Continue?" 
fi


###################################
#                           
# ____  ____  _____       ____ _               _        
#|  _ \|  _ \| ____|     / ___| |__   ___  ___| | _____ 
#| |_) | |_) |  _| _____| |   | '_ \ / _ \/ __| |/ / __|
#|  __/|  _ <| |__|_____| |___| | | |  __/ (__|   <\__ \
#|_|   |_| \_\_____|     \____|_| |_|\___|\___|_|\_\___/
#                                                       
#
##################################


if ! which curl >/dev/null ; then
    echo ""
    echo "Please install 'curl' to continue"
    exit -1 
fi

if ! which conan >/dev/null ; then
    echo ""
    echo "Please install 'conan' to continue"
    exit -1 
fi


if ! which opp_run >/dev/null ; then
    echo ""
    echo "Please install 'OMNeT++ ' to continue"
    exit -1 
fi

###################################
#                           
# _ __  _   _  ___ _ ____   __
#| '_ \| | | |/ _ \ '_ \ \ / /
#| |_) | |_| |  __/ | | \ V / 
#| .__/ \__, |\___|_| |_|\_/  
#|_|    |___/                 
#
##################################
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$PYENV_ROOT/shims:$PATH"
if ! command -v pyenv &> /dev/null
then
	echo "Installing pyenv..."
	if [[  "$OSTYPE" == "darwin"* ]]; then
		brew install pyenv
	else
		git clone --branch v2.3.2 https://github.com/pyenv/pyenv.git ~/.pyenv
	fi
	export PYENV_ROOT="$HOME/.pyenv"
	export PATH="$PYENV_ROOT/bin:$PATH"
	export PATH="$PYENV_ROOT/shims:$PATH"
	eval "$(pyenv virtualenv-init -)"
fi

if $accept_all
then
    pyenv install 3.9.0 -f
fi

if ! $accept_all
then
    if !(pyenv install 3.9.0); then
        echo "Python 3.9.0 will not be installed by this setup. Proceed with the setup.."
    fi
fi
eval "$(pyenv init -)"
pyenv global 3.9.0
##################################
#                  _              
# _ __   ___   ___| |_ _ __ _   _ 
#| '_ \ / _ \ / _ \ __| '__| | | |
#| |_) | (_) |  __/ |_| |  | |_| |
#| .__/ \___/ \___|\__|_|   \__, |
#|_|                        |___/ 
##################################
if ! command -v poetry &> /dev/null
then
    echo "Installing poetry"
	if [[  "$OSTYPE" == "darwin"* ]]; then
		brew install poetry
	else
		pip install --user poetry
	fi
	mkdir -p $HOME/.poetry/env
	source $HOME/.poetry/env
fi
echo "Switching to python 3.9.0"

mkdir -p $HOME/.cache/pypoetry/virtualenvs
poetry env use 3.9.0

################################################################
# ____        _   _                   ____       _               
#|  _ \ _   _| |_| |__   ___  _ __   / ___|  ___| |_ _   _ _ __  
#| |_) | | | | __| '_ \ / _ \| '_ \  \___ \ / _ \ __| | | | '_ \ 
#|  __/| |_| | |_| | | | (_) | | | |  ___) |  __/ |_| |_| | |_) |
#|_|    \__, |\__|_| |_|\___/|_| |_| |____/ \___|\__|\__,_| .__/ 
#       |___/                                             |_|    
################################################################

echo "Installing required Python packages..."
poetry run python --version

poetry install
export PATH="$HOME/.poetry/bin:$PATH"

pip3 install conan # We need a local installation outside poetry, since conan is required for the OMNeT++ part
AIRMOBISIMDIR=$(pwd)

export AIRMOBISIMHOME=$AIRMOBISIMDIR
################################################################
#__     __   _             ____       _               
#\ \   / /__(_)_ __  ___  / ___|  ___| |_ _   _ _ __  
# \ \ / / _ \ | '_ \/ __| \___ \ / _ \ __| | | | '_ \ 
#  \ V /  __/ | | | \__ \  ___) |  __/ |_| |_| | |_) |
#   \_/ \___|_|_| |_|___/ |____/ \___|\__|\__,_| .__/ 
#                                              |_|    
################################################################

cd ..
if [  ! -d "veins" ]; then
  git clone https://github.com/sommer/veins.git
  cd veins
  git checkout tags/veins-5.2
else
  cd veins
fi

./configure
if [[  "$OSTYPE" == "darwin"* ]]; then
	make -j$(( $(sysctl -n hw.ncpu) - 1 ))
else
	make -j$(( $(nproc) - 1 ))
fi
cd ..



cd $AIRMOBISIMDIR

if [  ! -f "$HOME/.conan/profiles/default" ]; then 
	echo "Create new default conan profile"
	mkdir -p "$HOME/.conan/profiles/"
	poetry run conan profile new default --detect 
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "This is a Linux"
	poetry run bash -c "conan profile update settings.compiler.libcxx=libstdc++11 default"
else
    echo "This is a Mac"
	poetry run bash -c "conan profile update settings.compiler.version=13.0 default"
fi

echo "Starting installation of conan dependencies"

cd ..

if [  ! -d "AirMobiSim_libveins" ]; then
  git clone https://git.cms-labs.org/git/hardes/AirMobiSim_libveins
fi
cd AirMobiSim_libveins

./configure
if [[  "$OSTYPE" == "darwin"* ]]; then
	make -j$(( $(sysctl -n hw.ncpu) - 1 ))
else
	make -j$(( $(nproc) - 1 ))
fi

cd $AIRMOBISIMDIR
./buildProto.sh


echo "Successfully installed AirMobiSim!"

echo "Please run the following commands or add them to your .bashrc/.zshrc/..."

echo "-"
echo "'export PATH="\$HOME/.poetry/bin:\$PATH"'"
echo "'export AIRMOBISIMHOME=$AIRMOBISIMDIR'"
echo "-"

echo "You can run AirMobiSim with the command 'poetry run ./airmobisim.py'"
