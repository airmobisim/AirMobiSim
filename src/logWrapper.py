#!/usr/bin/env python3

import logging

'''
Logging configuration. Valid loglevels are (ordered from most verbose to least verbose):
DEBUG
INFO
WARNING
ERROR
CRITICAL
'''
#class LogWrapper:


def basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG):
    logging.basicConfig(filename, encoding, level)


def debug(statement):
    logging.debug(statement)


def info(statement):
    logging.debug(statement)


def warning(statement):
    logging.warning(statement)


def error(statement):
    logging.error(statement)


def critical( statement):
    logging.critical(statement)
    print("CRITICAL: " + statement)
