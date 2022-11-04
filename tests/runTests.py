#!/usr/bin/env python3
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

