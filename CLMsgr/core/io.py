'''
Handles all Input/Output of the Program.

Dependencies: colorama
'''

import sys


try:
    import colorama
    _GREEN = colorama.Fore.GREEN
    _RED = colorama.Fore.RED
    _RESET = colorama.Style.RESET_ALL
    _WHITE = colorama.Fore.WHITE
except ImportError:
    _GREEN = ''
    _RED = ''
    _RESET = ''
    _WHITE = ''


def ask(prompt, multiline=False):
    '''' Asks for Input from the user.
    `prompt`: message to show to the user when asking.
    `multiline`: True/False. Whether input may span several lines.
    Returns content entered.
    Returns None if editing was cancelled by keyboard interrupt
        or no input gotten from user.
    '''
    print('{0}: '.format(prompt))
    if multiline:
        contents = []
        while True:
            try:
                if sys.version_info.major < 3:
                    content = raw_input('> ')
                else:
                    content = input('> ')
            except KeyboardInterrupt:
               return None
            except EOFError:
                return None
            if content == ':end':
                break
            contents.append(content)
        if len(contents) == 0:
            return None
        return '\n'.join(contents)
    else:
        try:
            if sys.version_info.major < 3:
                return raw_input('> ')
            else:
                return input('> ')
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None


def get_color(status):
    ''' Returns the appropriate color for Output.
    `status`:
        0 for success
        1 for errors
        2 for documentation
        * for just plainly boring stuff. (Anything else)
    '''
    if status == 0:
        return _GREEN
    elif status == 1:
        return _RED
    elif status == 2:
        return _WHITE
    else:
        return ''


def write(channel, msg, status=0):
    ''' Writes messages along with the associated channel to the
    stdout.
    `channel`: channel raising the write. e.g. twitter.
        Pass an empty string if no specific channel is targetted.
    `msg`: message to show to user. e.g. Damn! We broken!
    '''
    if channel == '' or not channel:
        channel = '!'
    words = '{color}[ {channel} ] {msg}{reset}'.format(
                color=get_color(status),
                channel=channel,
                msg=msg,
                reset=_RESET)
    print(words)


def listing(channel, heading, content, status=2):
    ''' List items to the User.
    `channel`: channel targetted
    `heading`: heading of the content
    `content`: iterable, dimension list
    `status`: status of the content.
    '''
    if channel == '' or heading is None:
        channel = '!'
    'Handles listing of iterables'
    print('{color}\n{sep}\n{heading} - {channel}\n{sep}\n{content}\n'.format(
                    color=get_color(status),
                    heading=heading,
                    channel=channel,
                    sep="=" * len(heading),
                    content='-> {0}'.format('\n> '.join(content)) if content else ' None'
    ))
