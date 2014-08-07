'''
Commandline Interface
----------------------

Dependencies: argparse(amust), .api, .__version__
'''


import argparse
from . import api
from . import __version__


def arg_parser():
    ''' Set the commandline options.
    Returns the arguments/options entered. '''

    parser = argparse.ArgumentParser(
        description='Send and Receive messages from your channels',
    )

    channels = []
    channels_choice = parser.add_argument_group(
        'Channels',
        'Channel to use in the command')
    for channel in api.channels:
        try:
            channels_choice.add_argument(
                '-{0}'.format(channel['short']),
                '--{0}'.format(channel['name']),
                action='store_true',
                help=channel['description'])
            channels.append(channel['name'])
        except KeyError:
            pass

    message_mgt = parser.add_argument_group(
        'Message management',
        'Manage your messages')
    message_mgt.add_argument('-f', '--fetch',
                             action='store_true',
                             help='fetch new messages from the channel(s)')
    message_mgt.add_argument('-s', '--send',
                             metavar='USER',
                             dest='send', nargs='+',
                             help='send message to user(s) in your channel(s)')
    message_mgt.add_argument('-b', '--broadcast',
                             action='store_true',
                             help='broadcast message to your channel(s)')
    message_mgt.add_argument('-v', '--view',
                             action='store_true',
                             help='view recent received messages')
    message_mgt.add_argument('-d', '--delete',
                             action='store_true',
                             help='delete messages in the channel(s)')

    channel_mgt = parser.add_argument_group(
        'Account Management',
        'Manage your accounts connected to the channels')
    channel_mgt.add_argument('-u', '--users',
                             action='store_true',
                             help='see users you can message in the channel')
    channel_mgt.add_argument('-a', '--add',
                             action='store_true',
                             help='add a account to the channel')
    channel_mgt.add_argument('-acc', '--accounts',
                             action='store_true',
                             help='view username of accounts registered to channels')
    channel_mgt.add_argument('-r', '--remove',
                             action='store_true',
                             help='remove a account from the channel')

    more = parser.add_argument_group('More Options')
    more.add_argument('--serl',
                      metavar='receipent',
                      dest='serl', nargs=1,
                      help='Start the Send-Receive-Loop with channel')
    more.add_argument('--doc',
                      action='store_true',
                      help='view the documentation of the channel(s)')
    more.add_argument('--faulty',
                      action='store_true',
                      help='view the faulty channel(s)')
    more.add_argument('--install',
                      metavar='channel.py',
                      dest='install', nargs='+',
                      help='install new channel(s) from a module file')
    more.add_argument('--un-install',
                      metavar='channel',
                      dest='uninstall', nargs='+',
                      help='un-install channel(s)')
    more.add_argument('--version',
                      action='version',
                      version='%(prog)s version {0}'.format(__version__))
#    more.add_argument('--share',
#                        action='store_true',
#                        help='Share the word about %(prog)s')

    args = parser.parse_args()
    args = vars(args)
    return args, channels


def run():
    '''Runs the commandline argument parser and the associated objectives'''

    args, channels = arg_parser()

    # Getting the targeted channels
    targets = []
    for target in channels:
        if args[target]:
            targets.append(target)
    if targets == []:
        targets = None

    def targets_acquired(number=None):
        if targets:
            # Requiring a specific number of targets
            if number:
                if len(targets) == number:
                    return True
                else:
                    api.write('', 'Channels Required: {0}'.format(number), 1)
                    return False
            # No specific number of targets
            else:
                return True
        # No targets found
        api.write('', 'No channel specified', 1)
        return False

    # Fetching messages
    if args['fetch']:
        api.channel_runner('fetch', targets=targets)

    # Sending messages
    if args['send']:
        if targets_acquired():
            words = api.ask('Message', multiline=True)
            if words:
                msg = {
                    'to': args['send'],
                    'content': words
                }
                api.channel_runner('send', targets=targets, message=msg)
            else:
                api.write('', 'Sending terminated...', 1)

    # Broadcast
    if args['broadcast']:
        if targets_acquired():
            msg = api.ask('Message', multiline=True)
            if msg:
                api.channel_runner('broadcast', targets=targets, message=msg)
            else:
                api.write('', 'Broadcast terminated...', 1)

    if args['view']:
        api.message_mgr('view', targets)

    # Deleting messages
    if args['delete']:
        api.message_mgr('delete', targets=targets)

    # Viewing users. Defaults to ALL channels
    if args['users']:
        chs = targets
        if targets is None:
            chs = channels
        api.channel_runner('users', targets=chs)

    # Adding channnels
    if args['add']:
        if targets_acquired():
            username = raw_input('Username: ')
            api.account_mgr('add', targets=targets, username=username)

    # Removing channels
    if args['remove']:
        if targets_acquired():
            api.account_mgr('remove', targets=targets)

    # Listing all the accounts
    if args['accounts']:
        api.account_mgr('view')

    # Send-Receive-Loop
    if args['serl']:
        if targets_acquired(1):
            api.serl(targets[0], args['serl'][0])

    # View documentation of channel(s)
    if args['doc']:
        if targets_acquired():
            api.documentation(targets)

    # View the faulty channel(s)
    if args['faulty']:
        api.view_faulty_channels()

    # Installing new Channel
    if args['install']:
        api.install_channel(args['install'])

    # Unistalling channel(s)
    if args['uninstall']:
        api.uninstall_channel(args['uninstall'])

    # Fall-Back Option
    # Thinking of witty witty messages to user.


if __name__ == '__main__':
    run()
