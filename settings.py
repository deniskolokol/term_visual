OSC_LISTEN_ADDRESS = "127.0.0.1"
OSC_LISTEN_PORT = 7110
OSC_LISTENER_TIMEOUT = 0

# Load local settings
try:
    from .local_settings import *
except Exception as err:
    print('Error loading local settings:\n%s\n\nUsing base settings.' % err)
