# -*- coding: utf-8 -*-

import os
import re
import time
import random
import cProfile
from utils import shoot, shoot_file, random, spinning_cursor, relpath

PATT = re.compile('^ds[0-9]+.txt$')
fnames = [fn for fn in os.listdir('.')
          if os.path.isfile(fn) and not PATT.match(fn)]

def shoot_unit():
    os.system('clear')
    fname = relpath(random.choice(fnames))
    shoot(
        "%(div)s\n%(name)s\n%(div)s\n" % {
            'div': "-" * len(fname),
            'name': fname
            },
        color='blue'
        )
    spinning_cursor(random.random()*5)
    with open(fname, 'r') as f:
        shoot_file(fname, 'white')
        shoot("\n")
        spinning_cursor(random.random()*5)
        shoot("\n\n")

        if not fname.endswith(".py"):
            return

        for line in f.readlines():
            shoot("[profile] %s" % line.strip())
            spinning_cursor(random.random()*5)
            try:
                cProfile.run('re.compile("%s")' % line.strip())
            except Exception as e:
                shoot("[exception] %s" % e)
            spinning_cursor(random.random()*5)

while True:
    try:
        shoot_unit()
    except Exception as e:
        shoot("[exception] %s" % e)

    shoot("\n\n")
    time.sleep(random.random()*1.5)
