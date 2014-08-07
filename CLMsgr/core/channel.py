'''
Class for a Channel Object passed to channels.

Dependencies: .accounts
'''

import getpass
from . import accounts
from . import io
from . import messages


class channel:
    ''' `channel` class for file-like objects passed to channels
    '''
    def __init__(self, name):
        self.__name = name  # name of the channel
        self.username = accounts.search_username(name)  # username of user

    def listing(self, heading, content, status=2):
        'Handles listing of iterables'
        io.listing(self.__name, heading, content, status)

    def read(self, prompt):
        'Handles getting input from User'
        return raw_input('? {prompt} ({channel}): '.format(
            prompt=prompt,
            channel=self.__name))

    def msg(self, sender, content):
        'Handles showing message to User'
        messages.save(self.__name, sender, content)
        print('\n{color}>>> {sender}{reset} ({channel}): {content}\n'.format(
            color=colorama.Fore.WHITE,
            reset=colorama.Style.RESET_ALL,
            sender=sender,
            channel=self.__name,
            content=content))

    def getpass(self, prompt):
        'Handles getting password from User'
        return getpass.getpass('?? {prompt} ({channel}): '.format(
            prompt=prompt,
            channel=self.__name))

    def success(self, msg):
        write(self.__name, msg)

    def error(self, msg):
        write(self.__name, msg, 1)

    def read_config(self, key):
        return accounts.read_one(self.__name, key)

    def store_config(self, key, value):
        return accounts.save_one(self.__name, key, value)

    def cache(self, items):
        # Storing Items for a Channel
        pass
