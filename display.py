# -*- coding: utf-8 -*-
import os
import time
import json
import pprint
import argparse

from utils import shoot, shoot_file, shoot_table, \
                  weighted_choice, random, spinning_cursor
from utils import relpath


def prettify_json(stuff):
    return json.dumps(stuff, indent=random.randint(2, 4))


def prettify_pprint(stuff):
    return pprint.pformat(stuff, indent=random.randint(2, 4), width=80, depth=None)


def main(*fnames):
    data = []
    for fname in fnames:
        with open(fname, 'r+') as fp:
            data.extend(json.load(fp))
            fp.close()

    i = 0
    stop = len(data)
    while True:
        freeze = random.random() * 0.5
        step = random.randint(1, 3)
        slc = min(i+step, stop-1)

        tmp_ = data[i:slc]
        if tmp_:
            for x in tmp_:
                x.update(
                    status=weighted_choice([
                        ('error', .05),
                        ('debug', .65),
                        ('info', .3)])
                    )
            func = random.choice([prettify_json, prettify_pprint])
            shoot(func(tmp_))
            i += step
        else:
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
            try:
                shoot_file()
            except IndexError:
                pass
            freeze = random.uniform(0.2, 0.8)

        time.sleep(freeze)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='display')
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        required=True,
                        nargs='*',
                        metavar='FILE_JSON',
                        dest='input_files',
                        help='Input file(s) in JSON format')
    args = parser.parse_args()
    main(*args.input_files)
