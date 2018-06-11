# -*- coding: utf-8 -*-
import os
import sys
import time
import OSC
from subprocess import Popen, PIPE


with open('runtrace.sh', 'r') as script:
    commands = [l.split() for l in script.readlines()
                if l.startswith('tmux')]
    script.close()

# processes = []
# for command in commands:
#     process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
#     stdout, stderr = process.communicate()
#     processes.append(process)
#     time.sleep(0.5)

# time.sleep(5)
# for process in processes:
#     process.kill()
#     time.sleep(0.5)


def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


process_run = Popen('./runtrace.sh', stdout=PIPE, stderr=PIPE, shell=True)

while True:
    res = wait_key()
    if res == 'x':
        process_stop = Popen(['tmux', 'kill-server'], stdout=PIPE, stderr=PIPE, shell=True)
        print '...........................exiting!'
        process_run.kill()
        process_stop.kill()
        exit()

