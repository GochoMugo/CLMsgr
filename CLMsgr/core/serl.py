'''
The SEnd-Receive-Loop for One-to-One Communication

':end' ends the message and sends it.
Ctrl + D breaks out of the Loop without sending message
'''

from . import channel
from . import io


def loop(ch, receipent, multiline=True):
    ''' Loop (till we told to Die)
    'channel': channel instance.
    '''

    # Loop Now
    stop = False
    while stop is False:
        # Getting input
        if multiline:
            try:
                myInput = io.ask('Message', multiline=True)
            except EOFError:
                break
        else:
            pass
        # Sending Input
        ch['init']('serl',
            {'to': receipent, 'message': myInput},
            channel.channel(ch['name']))
        # Showing Message Received
