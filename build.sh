#!/usr/bin/env bash
#
# Copyright (C) 2022-2025 Tobias Hardes <info@thardes.net>
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

usage() {
    echo "Usage: $(basename "$0") [-y|--non-interactive] [--with-omnet] [-h|--help]"
    echo ""
    echo "  -y, --non-interactive   Skip confirmation prompts and proceed automatically"
    echo "                          (implies no OMNeT++ setup unless --with-omnet is also given)"
    echo "  --with-omnet            Also set up the OMNeT++/veins coupling: clones and"
    echo "                          compiles veins and AirMobiSim_libveins, needs OMNeT++"
    echo "                          and conan installed. Without this flag, only the"
    echo "                          standalone Python kinematic simulator is installed."
    echo "  -h, --help              Show this help message and exit"
}

accept_all=false
with_omnet=false
while [ "$1" != "" ]; do
    case $1 in
        -y | --non-interactive )
                                accept_all=true
                                ;;
        --with-omnet )
                                with_omnet=true
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


GRPC_VERSION=1.48.4
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
echo "curl"
echo "pyenv"
echo "(OMNeT++ 6.1 and conan.io - version: 2.12.1 - are only needed if you also want the optional OMNeT++/veins coupling, see --with-omnet)"

echo "This setup installs all required Python packages (and poetry) and generates the gRPC/protobuf Python bindings.

Optionally (only with --with-omnet), it also loads the AirMobiSim extension from Veins and installs native binaries and libs from GRPC (version $GRPC_VERSION) and Protobuf ($PROTOC_VERSION) using conan.io, then compiles that native code."
if ! $accept_all
then
    read -p "Continue?"
fi

if ! $with_omnet && ! $accept_all
then
    read -p "Also set up the OMNeT++/veins coupling? Needs OMNeT++ and conan installed, and clones+compiles veins and AirMobiSim_libveins. [y/N] " omnet_choice
    case "$omnet_choice" in
        [Yy]|[Yy][Ee][Ss]) with_omnet=true ;;
        *) with_omnet=false ;;
    esac
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
    exit 1
fi

if $with_omnet; then
    if ! which conan >/dev/null ; then
        echo ""
        echo "Please install 'conan' to continue, or drop --with-omnet for a standalone install"
        exit 1
    fi

    if ! which opp_run >/dev/null ; then
        echo ""
        echo "Please install 'OMNeT++ ' to continue, or drop --with-omnet for a standalone install"
        exit 1
    fi
fi

if ! which pyenv >/dev/null ; then
    echo ""
    echo "Please install 'pyenv' to continue"
    exit 1
fi

################################################################
# ____        _   _                   ____       _               
#|  _ \ _   _| |_| |__   ___  _ __   / ___|  ___| |_ _   _ _ __  
#| |_) | | | | __| '_ \ / _ \| '_ \  \___ \ / _ \ __| | | | '_ \ 
#|  __/| |_| | |_| | | | (_) | | | |  ___) |  __/ |_| |_| | |_) |
#|_|    \__, |\__|_| |_|\___/|_| |_| |____/ \___|\__|\__,_| .__/ 
#       |___/                                             |_|    
################################################################

echo "Installing required Python packages..."

# needed before the first poetry/pyenv invocation below, not just for later steps
export PATH="$HOME/.local/bin:$PATH"

REQUIRED_PYTHON_VERSION=$(grep -m1 '^python = ' pyproject.toml | sed -E 's/python = "([0-9.]+)".*/\1/')
echo "Ensuring pyenv has Python $REQUIRED_PYTHON_VERSION available..."
pyenv install -s "$REQUIRED_PYTHON_VERSION"
poetry env use "$(pyenv root)/versions/$REQUIRED_PYTHON_VERSION/bin/python3"

poetry install

AIRMOBISIMDIR=$(pwd)

export AIRMOBISIMHOME=$AIRMOBISIMDIR

if $with_omnet; then

# Keep Conan's state (profiles, package cache, config) scoped to this project
# instead of touching the user's global ~/.conan2.
export CONAN_HOME="$AIRMOBISIMDIR/.conan_home"
################################################################
#__     __   _             ____       _
#\ \   / /__(_)_ __  ___  / ___|  ___| |_ _   _ _ __
# \ \ / / _ \ | '_ \/ __| \___ \ / _ \ __| | | | '_ \
#  \ V /  __/ | | | \__ \  ___) |  __/ |_| |_| | |_) |
#   \_/ \___|_|_| |_|___/ |____/ \___|\__|\__,_| .__/
#                                              |_|
################################################################

# number of parallel make jobs, leaving one core free but never going below 1
build_jobs() {
	local ncpu
	if [[ "$OSTYPE" == "darwin"* ]]; then
		ncpu=$(sysctl -n hw.ncpu)
	else
		ncpu=$(nproc)
	fi
	if [ "$ncpu" -gt 1 ]; then
		echo $(( ncpu - 1 ))
	else
		echo 1
	fi
}

cd ..
if [  ! -d "veins" ]; then
  git clone https://github.com/sommer/veins.git
  cd veins
  git checkout tags/veins-5.2
else
  cd veins
fi

./configure
make -j"$(build_jobs)"
cd ..



cd $AIRMOBISIMDIR

if [  ! -f "$CONAN_HOME/profiles/default" ]; then
	echo "Create new default conan profile (scoped to $CONAN_HOME)"
	conan profile detect
fi

profilePath=$(conan profile path default)

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "We need to adapt the conan profile at $profilePath."

	while true; do
		read -p "Should the script overwrite the $profilePath file to apply required changes [Y/n]?" choice


		choice=${choice:-Y}

		case "$choice" in
		    [Yy]|[Yy][Ee][Ss])
			cp "./assets/default" "$profilePath"
			echo "Replaced $profilePath"
			break
			;;
		    [Nn]|[Nn][Oo])
			echo "Skipping action on conan profile"
			break
			;;
		    *)
			echo "Invalid input"
			;;
		esac
	done
else
    echo "This is a Mac. Adapting the conan profile at $profilePath."
	sed -i '' 's/^compiler\.version=.*/compiler.version=13.0/' "$profilePath"
fi

echo "Starting installation of conan dependencies"

cd ..

if [  ! -d "AirMobiSim_libveins" ]; then
  git clone https://github.com/airmobisim/AirMobiSim_libveins
fi
cd AirMobiSim_libveins

./configure
make -j"$(build_jobs)"

cd $AIRMOBISIMDIR

else
    echo "Skipping OMNeT++/veins setup (pass --with-omnet to enable it)."
fi

./buildProto.sh


if $with_omnet; then
    echo "Successfully installed AirMobiSim, including the OMNeT++/veins coupling!"
else
    echo "Successfully installed AirMobiSim (standalone, without the OMNeT++/veins coupling)!"
    echo "Re-run with --with-omnet later if you also want the OMNeT++ coupling."
fi

echo "Please run the following commands or add them to your .bashrc/.zshrc/..."

echo "-"
echo "export PATH="\$HOME/.local/bin:\$PATH""
echo "export AIRMOBISIMHOME=$AIRMOBISIMDIR"
echo "-"

if $with_omnet; then
    echo "If you need to re-run conan or the native build steps manually later, also export:"
    echo "export CONAN_HOME=$CONAN_HOME"
    echo "(this keeps conan's profiles/cache scoped to this project instead of ~/.conan2)"
fi

echo "You can run AirMobiSim with the command 'poetry run ./airmobisim.py'"
