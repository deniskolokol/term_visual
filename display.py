#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import time

from utils import shoot, shoot_file, weighted_choice, random, spinning_cursor


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
    shoot("=" * 80)
    data = [['#', 'LC', 'CCN', 'Dict#4', '....']]
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


with open('osceleton.tra', 'r+') as f:
    lines = f.readlines()
    f.close()

fname = 'osceleton.tra'
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
