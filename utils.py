#! /usr/local/bin/python

import os
import sys
import random
from bisect import bisect
from termcolor import colored


def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect(cum_weights, x)
    return values[i]


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


def shoot_file(fname=None, color=None):
    if color is None:
        color = random.choice(['green', 'blue', 'white'])
    if fname is None:
        fname = random.choice(
            [f for f in os.listdir('.') if os.path.isfile(f)]
            )
    with open(fname, 'r') as f:
        for l in f.readlines():
            shoot(l, color=color)
        shoot('\n')
        f.close()
