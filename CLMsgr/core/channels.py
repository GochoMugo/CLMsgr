'''
Handles running activities and needs of channels.
- Handles returns of channel runs

Dependencies: .accounts, .channel, .io

Not Implemented:
    - Handling Connection Errors Better
'''

import threading
from . import accounts
from . import channel
from . import io


def execute_aim(name, init, aim, msg, channel=channel.channel):
    '''Handles Calling channels init functions and return values.
        `name` - name of the channel
        `init` - initialization function of channel
        `aim` - aim the channels should achieve
        `msg` - msg that the channel will process
        `channel` - the channel class
    '''
    try:
        status, result = init(aim, msg, channel(name))
        if status:
            io.write(name, result)
        else:
            io.write(name, result, 1)
    except TypeError as err:
        io.write(name, '{0} Unsupported'.format(aim), 1)
    except Exception as err:
        io.write(name, '{0} Errored due to {1}'.format(aim, err), 1)
#        io.write(name, '{0} Errored'.format(aim), 1)


def run(aim, predefined, **kwargs):
    ''' Allows Running of Activities by channels.
            `aim` - aim to be passed to channels.
            `predefined` - all the channels that exist.
            `targets=targets` - the targetted channels.
            `message=message` - message to pass to channel.
     - Checks if username is registered for the channel.
     - Creates a new thread for activity for each channel.
    '''
    msg = kwargs.get('message', None)
    targets = kwargs.get('targets', None)

    # defaulting to all channels, if None is passed
    if not targets:
        targets = [i['name'] for i in predefined]

    # Looping through each channel being targetted
    for target_channel in targets:
        # Looking for the channel's init function
        for ch in predefined:
            if ch['init'] and ch['name'] == target_channel:
                # Ensure a username is registered for channel
                if accounts.search_username(ch['name']):
                    # Executing aim in a new thread
                    threading.Thread(
                        target=execute_aim,
                        args=(
                            ch['name'], ch['init'],
                            aim, msg,)
                    ).start()
                else:
                    io.write(ch['name'], 'No account registered', 1)
                # Break out of Loop
                break
