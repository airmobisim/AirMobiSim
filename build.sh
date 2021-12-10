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
echo "AirMobiSim requires pyenv and OMNeT++ 6 Pre 10. Both must be installed before the setup can be started."
echo "It furthermore installes all required Python packages, loads the AirMobiSim extension from Veins, installs native binaries and libs from GRPC (version $GRPC_VERSION) and Protobuf ($PROTOC_VERSION) using conan.io.

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
if ! command -v pyenv &> /dev/null
then
	echo "Installing pyenv..."
	curl https://pyenv.run | bash
#fi
#
################################################################
# ____        _   _                   ____       _               
#|  _ \ _   _| |_| |__   ___  _ __   / ___|  ___| |_ _   _ _ __  
#| |_) | | | | __| '_ \ / _ \| '_ \  \___ \ / _ \ __| | | | '_ \ 
#|  __/| |_| | |_| | | | (_) | | | |  ___) |  __/ |_| |_| | |_) |
#|_|    \__, |\__|_| |_|\___/|_| |_| |____/ \___|\__|\__,_| .__/ 
#       |___/                                             |_|    
################################################################
echo "Installing required Python packages..."

pip3 install --user --upgrade pipenv
if !(pyenv install 3.8.9); then
	echo "Python 3.8.9 will not be installed by this setup. Proceed with the setup.."
fi

pyenv local 3.8.9
PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"
PATH="$PATH:$PYTHON_BIN_PATH"
pip3 install --user --upgrade pipenv

pipenv install
pipenv run python -m grpc_tools.protoc --python_out=. --grpc_python_out=. proto/airmobisim.proto -I .


################################################################
#__     __   _             ____       _               
#\ \   / /__(_)_ __  ___  / ___|  ___| |_ _   _ _ __  
# \ \ / / _ \ | '_ \/ __| \___ \ / _ \ __| | | | '_ \ 
#  \ V /  __/ | | | \__ \  ___) |  __/ |_| |_| | |_) |
#   \_/ \___|_|_| |_|___/ |____/ \___|\__|\__,_| .__/ 
#                                              |_|    
################################################################

cd ..
if ![ -d "airmobisimVeins" ]; then
  git clone https://git.cms-labs.org/git/hardes/airmobisimVeins
fi
cd airmobisimVeins
./configure
make -j$(nproc)

cd subprojects/veins_libairmobisim2/
conan install .
cwd=$(pwd)
cd
cd .conan/data

basePath=$(pwd)

grpc_cpp_plugin=$(find . -type f -name "grpc_cpp_plugin" 2>/dev/null | grep -aE "$GRPC_VERSION.*package")
grpc_cpp_plugin="${grpc_cpp_plugin:1}"
grpc_cpp_plugin=$basePath$grpc_cpp_plugin

echo $grpc_cpp_plugin

protoc=$(find . -name "protoc" | grep  "$PROTOC_VERSION.*package")
protoc="${protoc:1}"
protoc=$basePath$protoc

cd $cwd

$protoc airmobisim.proto --cpp_out=src/veins_libairmobisim/proto

$protoc airmobisim.proto --grpc_out=src/veins_libairmobisim/proto/ --plugin=protoc-gen-grpc=$grpc_cpp_plugin


./configure
make -j$(nproc)


