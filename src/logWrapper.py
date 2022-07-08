#
# Copyright (C) 2022 Tobias Hardes <tobias.hardes@uni-paderborn.de>
# Copyright (C) 2022 Simon Welzel <simon.welzel@uni-paderborn.de>
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
import logging

'''
logWrapper configuration. Valid loglevels are (ordered from most verbose to least verbose):
DEBUG
INFO
WARNING
ERROR
CRITICAL
'''
#class LogWrapper:
 

def basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG):
    print("Writing logs to " + filename + " using level=" + str(logging.getLevelName(level)))
    logging.basicConfig(filename=filename, encoding=encoding, level=level)


def debug(statement, printToConsole=False, *args, **kwargs):
    logging.debug(statement, *args, **kwargs)
    if printToConsole:
       print("DEBUG: " + statement)


def info(statement, printToConsole=False, *args, **kwargs):
    logging.debug(statement, *args, **kwargs)
    if printToConsole:
        print("INFO: " + statement)


def warning(statement, printToConsole=False, *args, **kwargs):
    logging.warning(statement, *args, **kwargs)
    if printToConsole:
        print("INFO: " + statement)


def error(statement, printToConsole=False, *args, **kwargs):
    logging.error(statement, *args, **kwargs)
    if printToConsole:
        print("INFO: " + statement)


def critical(statement, *args, **kwargs):
    logging.critical(statement, *args, **kwargs)
    print("CRITICAL: " + statement)
