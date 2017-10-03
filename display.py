#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import random
from bisect import bisect

import time

from utils import shoot


def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect(cum_weights, x)
    return values[i]


def get_stat(data, labels):
    # statistics
    for row_num in range(random.randint(5, 20)):
        data.append(
            [random.choice(labels)] \
            + [random.randint(0, 2000) for i in range(len(data[0])-2)]
            + [random.random()*random.randint(0, 100)]
            )
    col_width = max(len(str(word)) for row in data for word in row) + 2  # padding
    for rw in data:
        yield "".join(str(word).ljust(col_width) for word in rw)


def shoot_table():
    shoot("=" * 100)
    data = [['#', 'LC', 'CCN', 'Dict', 'Dict#4', '....']]
    labels = ['inf', 'err', 'err cri', 'warn', 'generic']
    ln = 0
    for row in get_stat(data, labels):
        if ln == 0:
            shoot(row, color='green')
        else:
            if 'err cri' in row:
                shoot(row, color='red')
            else:
                shoot(row, color='white')
        ln += 1
        time.sleep(0.1)
    time.sleep(random.random()*2)
    shoot('\n\n')


def shoot_file():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    file_ = random.choice(files)
    color = random.choice(['green', 'blue', 'white'])
    with open(file_, 'r') as f:
        for l in f.readlines():
            shoot(l, color=color)
        shoot('\n')
        f.close()


fname = 'stderr.log'
i = 0
while True:
    try:
        logfile = open(fname, 'r')
        lines = logfile.readlines()
        logfile.close()
    except Exception as err:
        shoot('%(break)s\nERROR: %(err)s\n%(break)s\n' % {
            'err': err, 'break': '='*50
            })
        time.sleep(random.random()*2)
        continue
        
    for line in lines:
        shoot(line)

        # occasionally output line breaks
        if weighted_choice([(True, 1), (False, 9)]):
            shoot('\n')

            # occasionally output line breaks
            if weighted_choice([(True, 2), (False, 8)]):
                shoot_table()

        # occasionally output the whole random file from the current dir
        if weighted_choice([(True, 1), (False, 9)]):
            shoot_file()

        time.sleep(random.random()*0.3)
