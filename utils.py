#! /usr/local/bin/python

import os
import sys
import time
import random
from bisect import bisect
from termcolor import colored
from string import ascii_lowercase, digits, punctuation


CHARS = ascii_lowercase + digits + punctuation


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
    ln = line.lower()
    try:
        line = (line.rstrip() + '\n').encode('utf-8')
    except UnicodeDecodeError as e:
        pass

    if color:
        output.write(colored(line, color))
        return

    if ('error' in ln) or ('exception' in ln):
        output.write(colored(line, 'red'))
    elif 'debug' in ln:
        output.write(colored(line, 'white', attrs=['bold']))
    elif ('warning' in ln) or ('profile' in ln):
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


def spinner():
    while True:
        for cursor in '|/-\\':
            yield cursor

def spinning_cursor(wait=10, output=sys.stdout):
    spinner_ = spinner()
    for _ in range(int(wait/0.1)):
        output.write(spinner_.next())
        output.flush()
        time.sleep(0.1)
        output.write('\b')


def rand_string(size=12):
    """
    Generates quazi-unique sequence from random digits and letters.
    """
    return ''.join(random.choice(CHARS) for x in range(size))
