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
    logging.basicConfig(filename=filename, encoding=encoding, level=level)


def debug(statement, *args, **kwargs):
    logging.debug(statement, *args, **kwargs)


def info(statement, *args, **kwargs):
    logging.debug(statement, *args, **kwargs)


def warning(statement, *args, **kwargs):
    logging.warning(statement, *args, **kwargs)


def error(statement, *args, **kwargs):
    logging.error(statement, *args, **kwargs)


def critical(statement, *args, **kwargs):
    logging.critical(statement, *args, **kwargs)
    print("CRITICAL: " + statement)
