'''
Handles the heavy lifting by binding the Commandline runner(argument
parser), utilities(accounts, messages, io etc) and channels(twitter, etc.)

Aims to let utilities and Channels be independent of each other allowing
easier adding and removing channels into the app
'''


from . import chs
from . import install
from . import core

'Importing all the methods here for the External Use of API e.g. api.write()'
from .core.io import ask
from .core.io import write
__app_dir__ = core.__app_dir__
__installation_dir__ = core.__installation_dir__
__chs_dir__ = core.__chs_dir__


def channels():
    ''' Returns a List of Dicts that are channels registered in the
    chs (channels) module '''
    return chs.channels()
# Saving the cost of importing and re-importing modules
channels, faulty_channels = channels()


def channel_lookup(name):
    for channel in channels:
        if channel['name'] == name:
            return channel
    return False


def channel_runner(aim, **kwargs):
    core.channels.run(aim, channels, **kwargs)


def account_mgr(aim, targets=[], username=None):
    # Adding account to DB
    if not core.accounts.manage(aim, targets, username):
        return
    if aim == 'add':
        for target in targets:
            # inject channel instance
            channel = channel_lookup(target)
            if channel['install']: # is None is no install is required
                if channel['install'](core.channel.channel(channel['name'])):
                    # success
                    core.io.write(channel['name'], 'Installation completed well')
                else:
                    # error
                    core.io.write(channel['name'], 'Failed to Install', 1)


def message_mgr(aim, targets=None):
    core.messages.manage(aim, targets)


def serl(target, receipient):
    channel = channel_lookup(target)
    if channel:
        core.serl.loop(channel, receipient)
    else:
        pass


def install_channel(targets):
    install.install_channel(targets, channels)


def uninstall_channel(targets):
    install.uninstall_channel(targets, faulty_channels)


def documentation(targets):
    ''' Show the documentation of channels.
    '''
    for target in targets:
        for channel in channels:
            if channel['name'] == target:
                write(target, channel['doc'], 2)
                break


def view_faulty_channels():
    ''' Show all the faulty channels
    '''
    core.io.listing(
        '',
        'Faulty Channels',
        ['{0}'.format(i['name']) for i in faulty_channels],
        2
    )
