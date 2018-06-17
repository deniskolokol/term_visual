# -*- coding: utf-8 -*-
import os
import sys
import time
from OSC import OSCServer
from subprocess import Popen, PIPE

import settings


def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clean_screen()

srv_conn = (settings.OSC_LISTEN_ADDRESS, settings.OSC_LISTEN_PORT)
SERVER = OSCServer(srv_conn)
SERVER.timeout = settings.OSC_LISTENER_TIMEOUT
print "\n[>] Instantiated server: {}:{}".format(*srv_conn)

oscserver_run = True

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
    global oscserver_run
    oscserver_run = False


def user_callback(path, tags, args, source):
    """
    :path: react only to /run
    :tags: ignored
    :args: OSCMessage with data.
    :source: where the message came from.
    """
    global process_run
    process_run = Popen('./runtrace.sh', stdout=PIPE, stderr=PIPE, shell=True)


SERVER.addMsgHandler("/run", user_callback)
SERVER.addMsgHandler("/stop", quit_callback)


class KeyboardInterruptError(Exception):
    pass

def process_frame():
    SERVER.timed_out = False
    while not SERVER.timed_out:
        SERVER.handle_request()


while oscserver_run:
    try:
        process_frame()
        time.sleep(0.1)
    except KeyboardInterrupt:
        oscserver_run = False


process_stop = Popen(['tmux', 'kill-server'], stdout=PIPE, stderr=PIPE, shell=True)
SERVER.close()
clean_screen()
