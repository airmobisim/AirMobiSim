#!/bin/bash
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
echo "OMNeT++ 6 Pre 10."
echo "conan.io - version: 1.44.1"

echo "This setup installs all required Python packages (and poetry), loads the AirMobiSim extension from Veins, installs native binaries and libs from GRPC (version $GRPC_VERSION) and Protobuf ($PROTOC_VERSION) using conan.io.

The complete source code is compiled afterwards.
"
read -p "Continue?" 

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
	curl https://pyenv.run | bash
	export PYENV_ROOT="$HOME/.pyenv"
	export PATH="$PYENV_ROOT/bin:$PATH"
	export PATH="$PYENV_ROOT/shims:$PATH"
	eval "$(pyenv virtualenv-init -)"
fi
if !(pyenv install 3.9.0); then
	echo "Python 3.9.0 will not be installed by this setup. Proceed with the setup.."
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
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
	fi
	

	source $HOME/.poetry/env
fi
echo "Switching to python 3.9.0"
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


poetry install
poetry run python -m grpc_tools.protoc --python_out=. --grpc_python_out=. proto/airmobisim.proto -I .
export PATH="$HOME/.poetry/bin:$PATH"

#pip3 install --user conan # We need a lokal installation outside poetry, since conan is required for the OMNeT++ part
AIRMOBISIMDIR=$(pwd)
################################################################
#__     __   _             ____       _               
#\ \   / /__(_)_ __  ___  / ___|  ___| |_ _   _ _ __  
# \ \ / / _ \ | '_ \/ __| \___ \ / _ \ __| | | | '_ \ 
#  \ V /  __/ | | | \__ \  ___) |  __/ |_| |_| | |_) |
#   \_/ \___|_|_| |_|___/ |____/ \___|\__|\__,_| .__/ 
#                                              |_|    
################################################################

cd ..
if [  ! -d "airmobisimVeins" ]; then
  git clone https://git.cms-labs.org/git/hardes/airmobisimVeins
fi
cd airmobisimVeins
AIRMOBISIMVEINS_PATH="$(pwd)/subprojects/veins_libairmobisim2"

./configure
if [[  "$OSTYPE" == "darwin"* ]]; then
	make -j$(sysctl -n hw.ncpu)
else
	make -j$(nproc)
fi

cd $AIRMOBISIMDIR

if [  ! -f "$HOME/.conan/profiles/default" ]; then 
	echo "Create new default conan profile"
	mkdir -p "$HOME/.conan/profiles/"
	poetry run conan profile new default --detect # the quotation marks created an error when running this on Linux
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	echo "This is a Linux"
	poetry run bash -c "conan profile update settings.compiler.libcxx=libstdc++11 default"
else
	echo "This is a Mac"
	poetry run bash -c "conan profile update settings.compiler.version=13.0 default"
	#poetry run bash -c "conan profile update settings.compiler.version=12.0 default"
	#poetry run bash -c "conan profile update settings.compiler.libcxx=libstdc++ default"
fi

echo "Starting installation of conan dependencies"

poetry run bash -c "cd $AIRMOBISIMVEINS_PATH && conan install . --build missing --profile=default"

cd
cd .conan/data

basePath=$(pwd)


### TODO: Start Remove ###
grpc_cpp_plugin=$(find . -type f -name "grpc_cpp_plugin" 2>/dev/null | grep -aE "$GRPC_VERSION.*package")
grpc_cpp_plugin="${grpc_cpp_plugin:1}"
grpc_cpp_plugin=$basePath$grpc_cpp_plugin

echo $grpc_cpp_plugin

protoc=$(find . -name "protoc" | grep  "$PROTOC_VERSION.*package")
protoc="${protoc:1}"
protoc=$basePath$protoc

cd $AIRMOBISIMVEINS_PATH 

$protoc airmobisim.proto --cpp_out=src/veins_libairmobisim/proto

$protoc airmobisim.proto --grpc_out=src/veins_libairmobisim/proto/ --plugin=protoc-gen-grpc=$grpc_cpp_plugin

### TODO: END Remove ###


./configure
if [[  "$OSTYPE" == "darwin"* ]]; then
	make -j$(sysctl -n hw.ncpu)
	#make -j4
else
	make -j$(nproc)
fi


echo "Everything worked"
echo ""
echo "Your PATH does not contain \"\$HOME/.poetry/bin:\$PATH\""
echo "Please run      'export PATH="\$HOME/.poetry/bin:\$PATH"' or add it to your .bashrc/.zshrc/..."
echo "You can run AirMobiSim with the command 'poetry run ./airmobisim.py'"
