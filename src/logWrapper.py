#!/usr/bin/env python3

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
    print("Writing logs to " + filename)
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


def critical(statement, printToConsole=False, *args, **kwargs):
    logging.critical(statement, *args, **kwargs)
    print("CRITICAL: " + statement)
