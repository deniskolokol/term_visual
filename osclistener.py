#!/usr/bin/python

from OSC import OSCServer
import sys
from time import sleep
import subprocess


server = OSCServer(("192.168.1.106", 7110))
server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)


def user_callback(path, tags, args, source):
    action = args[0]
    if action == 'kill':
        subprocess.call(["tmux", "kill-server"])
        # XXX: for Python 3 use
        # subprocess.run(["tmux", "kill-server"])
    print("Now do something:\n{}\n{}\n{}\n{}".format(
        path, tags, args, source))


def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler("/user", user_callback)
server.addMsgHandler( "/quit", quit_callback )


def each_frame():
    """User script that's called by the game engine every frame"""
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()


while run:
    sleep(1)
    each_frame()

server.close()
