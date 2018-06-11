#!/usr/bin/python

import sys
import time
import datetime
import optparse
import OSC
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

from utils import shoot, spinner


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


def send_osc(client, msg):
    msg.setAddress("/action")
    if 'event' not in msg:
        msg.extend(['event', 1])
    try:
        client.send(msg)
        shoot('\n')
        log_post('DEBUG: sending to the client: %s' % msg)
    except OSC.OSCClientError as err:
        log_post(
            "ERROR: %s OSC.OSCClientError %s\n" % (
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), err
                ),
            output=sys.stderr
            )


def main(opts):
    # connect to SuperCollider
    client = OSC.OSCClient()
    client.connect((opts.ip_addres, int(opts.port)))
    oscmsg = OSC.OSCMessage()
    log_post('INFO: connected to client to %s:%s' % (
        opts.ip_addres, opts.port
        ))

    # setup GPIO
    pin = int(opts.pin_number)
    state = False
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        state = GPIO.input(pin)
    except NameError as err:
        log_post('ERROR: %s' % err)

    log_post('INFO: waiting to state change...')
    spinner_ = spinner()
    while True:
        # read GPIO.
        try:
            read_state = GPIO.input(pin)
        except NameError:
            read_state = False

        if state != read_state:
            state = read_state
            send_osc(client, oscmsg)

        sys.stdout.write(spinner_.next())
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

    try:
        GPIO.cleanup()
    except NameError:
        pass


if __name__ == '__main__':
    cmdparser = optparse.OptionParser(usage="usage: %prog [OPTIONS]")
    cmdparser.add_option(
        "-a", "--addres", action="store", dest="ip_addres", default='127.0.0.1',
        help="IP address of the receiver [default \'%default\']"
        )
    cmdparser.add_option(
        "-p", "--port", action="store", dest="port", default=57120,
        help="IP port of the receiver [default \'%default\']"
        )
    cmdparser.add_option(
        "-n", "--pin", action="store", dest="pin_number", default=18,
        help="GPIO pin number [default \'%default\']"
        )
    opts, args = cmdparser.parse_args()
    main(opts)
