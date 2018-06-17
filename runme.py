# -*- coding: utf-8 -*-
import os
import sys
import time
from OSC import OSCServer
from subprocess import Popen, PIPE

SERVER_ADDRESS = "localhost"
SERVER_PORT = 7110
SERVER_TIMEOUT = 0
SERVER = OSCServer((SERVER_ADDRESS, SERVER_PORT))
SERVER.timeout = SERVER_TIMEOUT
server_run = True


# Add a method `handle_timeout` to an instance of OSCServer.
#
# tThis method of reporting timeouts only works by convention
# that before calling handle_request() the field .timed_out is
# set to False.
import types

def handle_timeout(self):
    self.timed_out = True

SERVER.handle_timeout = types.MethodType(handle_timeout, SERVER)


def quit_callback(path, tags, args, source):
    process_run.kill()
    # time.sleep(0.1)

    global server_run
    server_run = False

    process_stop = Popen(['tmux', 'kill-server'], stdout=PIPE, stderr=PIPE, shell=True)
    print '...........................exiting!'
    process_stop.kill()


def user_callback(path, tags, args, source):
    """
    :path: react only to /run
    :tags: ignored
    :args: OSCMessage with data.
    :source: where the message came from.
    """
    print("RUN: path: {}, tags: {}, args: {}, source: {}".format(
        path, tags, args, source))
    global process_run
    process_run = Popen('./runtrace.sh', stdout=PIPE, stderr=PIPE, shell=True)


SERVER.addMsgHandler("/run", user_callback)
SERVER.addMsgHandler("/stop", quit_callback)


def process_frame():
    SERVER.timed_out = False
    while not SERVER.timed_out:
        SERVER.handle_request()


while server_run:
    process_frame()
    time.sleep(0.1)

SERVER.close()
