#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import time
import random
from utils import shoot, random, weighted_choice, shoot_file


with open('osceleton.tra', 'r+') as f:
    lines = f.readlines()
    f.close()

i = 0
while True:
    freeze = random.random() * 0.05
    try:
        shoot(lines[i])
        i += 1
    except IndexError:
        i = 0

    # occasionally output line breaks
    if weighted_choice([(True, 1), (False, 9)]):
        shoot('\n')

    # occasionally output the whole random file from the current dir
    if weighted_choice([(True, 0.1), (False, 9.9)]):
        shoot_file()
        freeze = random.uniform(0.2, 0.8)

    time.sleep(freeze)
