# -*- coding: utf-8 -*-

import os
import time
import random
import psutil
from utils import shoot, random, spinning_cursor, rand_string, weighted_choice

i = 0
curr = 0
while True:
    shoot('{0: <35}|'.format("-" * int(psutil.cpu_percent())), 'red')
    time.sleep(random.random()*0.1)
    i += 1

    # occasionally clear the screen and output rand string
    if i >= 100:
        if weighted_choice([(True, 1), (False, 9)]):
            os.system('clear')
            shoot("\n%s\n" % rand_string(random.randint(200, 800)),
                  color='red')
            spinning_cursor(random.random()*0.5)
        i = 0
