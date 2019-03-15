import os
import sys
import time
import random
import datetime
from bisect import bisect
from termcolor import colored, cprint
from string import ascii_lowercase, digits, punctuation

import settings

CHARS = ascii_lowercase + digits + punctuation


def relpath(*x):
    return os.path.join(settings.BASE_DIR, *x)


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


def shoot(line, color=None, output=sys.stdout, attrs=None):
    ln = line.lower()
    try:
        line = line.rstrip().encode('utf-8')
    except UnicodeDecodeError:
        pass

    if color:
        cprint(line, color, attrs=attrs, file=output)
        return

    if ('error' in ln) or ('exception' in ln) or ('err' in ln):
        cprint(line, 'red', file=output)
    elif 'debug' in ln:
        cprint(line, 'white', attrs=['bold'], file=output)
    elif ('warning' in ln) or ('warn' in ln) or ('profile' in ln):
        cprint(line, 'white', attrs=['bold'], file=output)
    elif ('info' in ln) or ('inf' in ln):
        cprint(line, 'white', attrs=['dark'], file=output)
    else:
        cprint(line, 'white', file=output)


def shoot_file(fname=None, color=None):
    exclude_files = ['osceleton.trace']
    if fname is None:
        fname = random.choice([
            f for f in os.listdir(settings.BASE_DIR)
            if os.path.isfile(f) and f not in exclude_files])

    fname = relpath(fname)
    if color is None:
        # do not allow big files to be displayed in color
        statinfo = os.stat(fname)
        if statinfo.st_size <= 10000:
            color = random.choice(['blue', 'white', 'red'])
        else:
            color = 'white'

    with open(fname, 'r') as f:
        count = 0
        for ln in f.readlines():
            count += 1
            ln = "%-3d    %s" % (count, ln)
            shoot(ln, color=color)
            time.sleep(0.05)
        shoot('\n')
        f.close()


def spinner():
    while True:
        for cursor in '|/-\\':
            yield cursor

def spinning_cursor(wait=10, output=sys.stdout):
    spinner_ = spinner()
    for _ in range(int(wait/0.1)):
        output.write(spinner_.next())
        output.flush()
        time.sleep(0.1)
        output.write('\b')


def table_row(row, width):
    return "".join(str(word).ljust(width) for word in row)


def get_stat(labels, num_col):
    data = []
    for _ in range(random.randint(5, 20)):
        data.append(
            [random.choice(labels)] \
            + [random.randint(0, 2000) for i in range(num_col-2)]
            + [random.random()*random.randint(0, 100)]
            )
    col_width = max(len(str(word)) for row in data for word in row) + 2 # padding
    data = sorted(data, key=lambda x: x[0], reverse=random.choice([True, False]))
    return col_width, [table_row(rw, col_width) for rw in data]


def shoot_table():
    shoot("=" * 80)
    header = ['#', 'LC', 'CCN', 'Dict#4', '-->']
    labels = ['inf', 'err', 'err cri', 'warn', 'generic']
    width, stat = get_stat(labels, num_col=len(header))
    shoot(table_row(header, width), color='white', attrs=['dark'])
    for row in stat:
        shoot(row)
        time.sleep(0.1)
    time.sleep(random.random()*2)
    shoot('\n\n')


def rand_string(size=12):
    """
    Generates quazi-unique sequence from random digits and letters.
    """
    return ''.join(random.choice(CHARS) for x in range(size))


def wait_key():
    """
    Wait for a key press on the console and return it.
    """
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def log_post(msg, output=sys.stdout):
    if msg.lower().startswith('debug'):
        symbol = '>'
    elif msg.lower().startswith('error'):
        symbol = 'x'
    elif msg.lower().startswith('warning'):
        symbol = '!'
    else:
        symbol = '.'
    shoot('[%s] %s: %s' % (
        symbol, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg),
        output=output)
