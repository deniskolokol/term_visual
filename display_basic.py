# -*- coding: utf-8 -*-

from termcolor import colored
import numpy as np
import time


with open('kinect_log.txt', 'r+') as f:
    lines = f.readlines()
    f.close()

i = 0
while True:
    if np.random.choice([True, False], p=[0.1, 0.9]):
        print ''
    try:
        if 'debug' in lines[i]:
            print colored(lines[i].strip(), 'green')
        else:
            print colored(lines[i].strip(), 'white')
        i += 1
    except IndexError:
        i = 0
    time.sleep(np.random.random()*0.1)
