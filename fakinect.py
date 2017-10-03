#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Run it as:
$ ./fakinect.py | ./listener.py

In a separate pan run:
$ python display.py

Add 2 pans with htop:
$ htop -d 2 -s PERCENT_MEM
$ htop -d 0.5
"""
import sys
import time
import random


with open('osceleton.trace', 'r+') as f:
    lines = f.readlines()
    f.close()

i = 0
while True:
    try:
        print >> sys.stdout, lines[i].strip()
        i += 1
    except IndexError:
        i = 0
    time.sleep(random.random()*0.001)
