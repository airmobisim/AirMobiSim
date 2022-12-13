#!/usr/bin/env python3
#
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

from tests.test_DroCIBridge import startGrpcServer
from subprocess import Popen, PIPE
import time
import threading
import os
import signal

subprocess_server:Popen

# def startServer():
#     global subprocess_server
#     subprocess_server = Popen(['python3 startServer.py'], shell=True, stdout=PIPE)
    # out, err = subprocess_server.communicate()


def runAllTest():
    test = Popen(['python -m unittest discover -v '], shell=True, stdout=PIPE)
    out, err = test.communicate()


# t1 = threading.Thread(target=startServer)
t1 = threading.Thread(target=startGrpcServer)
t2 = threading.Thread(target=runAllTest)

t1.start()
time.sleep(5)
t2.start()
t2.join()

print('Finished running all tests!!!!!!!!!!')
# os.killpg(os.getpgid(subprocess_server.pid), signal.SIGTERM)
os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

