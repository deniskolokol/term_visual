# -*- coding: utf-8 -*-
import os
import time

from utils import shoot, shoot_file, shoot_table, \
                  weighted_choice, random, spinning_cursor
from utils import relpath

fname = relpath('osceleton.trace')
with open(fname, 'r+') as f:
    lines = f.readlines()
    f.close()

i = 0
while True:
    freeze = random.random()*0.3
    try:
        shoot(lines[i])
        i += 1
    except IndexError:
        i = 0
        # clear output each time the whole trace file is out
        os.system('clear')
        spinning_cursor(random.random())

    # occasionally output line breaks
    if weighted_choice([(True, 1), (False, 9)]):
        shoot('\n')

    # occasionally output table
    if weighted_choice([(True, 0.5), (False, 9.5)]):
        shoot('\n')
        shoot_table()
        freeze = random.uniform(0.2, 0.8)

    # occasionally output the whole random file from the current dir
    if weighted_choice([(True, 0.1), (False, 9.9)]):
        shoot_file()
        freeze = random.uniform(0.2, 0.8)

    time.sleep(freeze)
