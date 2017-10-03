#! /usr/local/bin/python
import sys
from termcolor import colored

from utils import shoot


lines = []
for line in sys.stdin:
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
