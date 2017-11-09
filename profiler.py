#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import random
import cProfile
from utils import shoot, random, weighted_choice, shoot_file


fnames = [f for f in os.listdir('.') if os.path.isfile(f)]

with open('osceleton.tra', 'r+') as f:
    lines = f.readlines()
    f.close()

while True:
    freeze = random.random() * 1.5

    fname = random.choice(fnames)
    shoot(
        "%(div)s\n%(name)s\n%(div)s\n" % {
            'div': "-" * len(fname),
            'name': fname
            },
        color='green'
        )
    with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            shoot(line, 'white')

        for line in lines:
            try:
                cProfile.run('re.compile("%s")' % line.strip())
            except Exception as e:
                shoot("[exception] %s" % e)
    shoot('\n')
    time.sleep(freeze)
