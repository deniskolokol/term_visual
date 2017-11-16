# -*- coding: utf-8 -*-

import os
import re
import time
import random
from utils import shoot, random, weighted_choice, shoot_file, spinning_cursor


fnames = [f for f in os.listdir('.')
          if os.path.isfile(f) and not re.match('^ds[0-9]+.txt$', f)]

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
        # clear output each time the whole trace file is out
        os.system('clear')
        spinning_cursor(random.random())

    # occasionally output line breaks
    if weighted_choice([(True, 1), (False, 9)]):
        shoot('\n')

    # occasionally output the whole random file from the current dir
    if weighted_choice([(True, 0.1), (False, 9.9)]):
        shoot_file(fname=random.choice(fnames), color='white')
        freeze = random.uniform(0.2, 0.8)

    time.sleep(freeze)
