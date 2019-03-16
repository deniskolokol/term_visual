#!/usr/bin/python

from OSC import OSCServer
import sys
import optparse
from time import sleep
import subprocess

from utils import shoot, spinner, log_post


run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

import types


def user_callback(path, tags, args, source):
    action = args[0]
    if action == 'kill':
        # kill existing visuals
        subprocess.call(["tmux", "kill-server"])
        # and start a listener to listen to eventual restart signal
        subprocess.call(["python", "osclistener.py", "--addres", "192.168.1.106", "--port", "7110"])
        # XXX: for Python 3 use
        # subprocess.run(["tmux", "kill-server"])
    elif action == 'restart':
        subprocess.call(["runtrace.sh"])
    log_post("DEBUG: received {} from {}: tags {}; args {}".format(path, source, tags, args))


def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False


def each_frame(server):
    """User script that's called by the game engine every frame"""
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()


def main(opts):
    server = OSCServer((opts.ip_addres, int(opts.port)))
    server.handle_timeout = types.MethodType(handle_timeout, server)
    server.addMsgHandler("/user", user_callback)
    server.addMsgHandler("/quit", quit_callback)
    log_post('INFO: listening on to %s:%s' % (opts.ip_addres, opts.port))
    spinner_ = spinner()
    while run:
        each_frame(server)

        sys.stdout.write(spinner_.next())
        sys.stdout.flush()
        sleep(0.5)
        sys.stdout.write('\b')

    server.close()


if __name__ == '__main__':
    cmdparser = optparse.OptionParser(usage="usage: %prog [OPTIONS]")
    cmdparser.add_option(
        "-a", "--addres", action="store", dest="ip_addres", default='127.0.0.1',
        help="IP address of the receiver [default \'%default\']"
        )
    cmdparser.add_option(
        "-p", "--port", action="store", dest="port", default=57120,
        help="IP port of the receiver [default \'%default\']"
        )
    opts, args = cmdparser.parse_args()
    main(opts)
