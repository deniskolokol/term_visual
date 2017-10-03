#! /usr/local/bin/python
import sys
from termcolor import colored


def shoot(line, color=None, output=sys.stdout):
    line = line.rstrip() + '\n'
    if color:
        output.write(colored(line, color))
        return

    ln = line.lower()
    if ('error' in ln) or ('exception' in ln):
        output.write(colored(line, 'red'))
    elif 'debug' in ln:
        output.write(colored(line, 'white', attrs=['bold']))
    elif 'warning' in ln:
        output.write(colored(line, 'green'))
    elif 'info' in ln:
        output.write(colored(line, 'white'))
    else:
        output.write(colored(line, 'blue'))
