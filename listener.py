#! /usr/local/bin/python
import sys
from termcolor import colored

from utils import shoot, weighted_choice, random


lines = []
for line in sys.stdin:
    # colorize line
    if weighted_choice([(True, 1), (False, 9)]):
        word = 'debug' if 'debug' in line else 'info'
        line = line.replace(word, random.choice(['warning', 'error']))

    lines.append(line)
    if len(lines) >= 1000:
        with open('stderr.log', 'w+') as log:
            log.seek(0)
            log.writelines(lines)
            log.truncate()
            log.close()
        lines = []

    shoot(line)

log.close()
