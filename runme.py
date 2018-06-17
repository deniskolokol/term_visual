# -*- coding: utf-8 -*-
import os
import sys
import time
from OSC import OSCServer
from subprocess import Popen, PIPE

import settings


srv_conn = (settings.OSC_LISTEN_ADDRESS, settings.OSC_LISTEN_PORT)
SERVER = OSCServer(srv_conn)
SERVER.timeout = settings.OSC_LISTENER_TIMEOUT
print "\n[>] Instantiated server: {}:{}".format(*srv_conn)

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


def report(path, tags, args, source):
    print("[>] OSC msg: path {}, tags: {}, args: {}, source: {}".format(
        path, tags, args, source))


def quit_callback(path, tags, args, source):
    process_run.kill()
    report(path, tags, args, source)

    global server_run
    server_run = False


def user_callback(path, tags, args, source):
    """
    :path: react only to /run
    :tags: ignored
    :args: OSCMessage with data.
    :source: where the message came from.
    """
    report(path, tags, args, source)

    global process_run
    process_run = Popen('./runtrace.sh', stdout=PIPE, stderr=PIPE, shell=True)


SERVER.addMsgHandler("/run", user_callback)
SERVER.addMsgHandler("/stop", quit_callback)


class KeyboardInterruptError(Exception):
    pass

def f(x):
    try:
        time.sleep(x)
        return x
    except KeyboardInterrupt:
        raise KeyboardInterruptError()

def process_frame():
    SERVER.timed_out = False
    while not SERVER.timed_out:
        SERVER.handle_request()


while server_run:
    try:
        process_frame()
        time.sleep(0.1)
    except KeyboardInterrupt:
        server_run = False

print "\n[>] Stopping processes"
process_stop = Popen(['tmux', 'kill-server'], stdout=PIPE, stderr=PIPE, shell=True)
process_stop.kill()

print "[>] Closing server"
SERVER.close()
