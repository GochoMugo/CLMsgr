'''
Channels Definition
-------------------
Required:
    __Name__: 'name_of_channel',
    __short__: 'short_name',
    __description__: 'short description of channel',
    __init__: initialization_func_of_channel,
    __doc__: 'documentation of the channel'
Optional:
    __install__: installation_func_of_channel/None.
            This function will be run when user is registering
            a new account for the channel.
            No parameter is passed to the Function.
            Should Return True for Success. False for Errors.

Topics
------

initialization_function(aim, msg, channel)
    - 'aim's that may be passed include:
            - fetch - check for new messages
            - send - send new messages
            - broadcast - broadcast message to users
            - users - show users user can message
            - serl - user running a SEnd-Receive-Loop
    - 'msg':
        - to: Array of Users to send message to.
        - content:  be a String of the message or None if none has been passed.
    - 'channel' is an object with the following attributes/methods:
            - username: string representing the username registered to account
            - read(prompt): get input from user
            - listing(heading, items): items must be iterable
            - msg(sender, content): handles showing new messages to user
            - getpass(prompt): get password from user
            - success(msg)
            - error(msg)
            - read_config(key)
            - store_config(key, value)
    A handler should return a tuple:
        True/False, 'message to show to user'

    Notes:
    ------
    1. It is acceptable not to handle an 'aim'. It will just be handled as
       Unsupported.
    2. Do NOT directly output messages to user. Use the 'io' to allow
       consistent user interface.
    3. We are Consenting Adults.

'''

import importlib
import os
import re


# This function should NEVER be automatically run when importing this
# module. Circular Dependency may occur.
def channels():
    ''' Get the Available channels.
    Returns a Tuple.
    tuple[0]: List with dictionaries in this form:
    {
        'name': 'name_of_channel',
        'short': 'short_name',
        'description': 'short description of channel',
        'install': installation_func_of_channel/None,
        'init': initialization_func_of_channel,
        'doc': 'documentation of the channel',
        'file': 'path/to/the/module'
    }
    tuple[1]: List with dictionaries in this form:
    {
        'name': 'name_of_channel',
        'short': 'short_name',
        'file': 'path/to/the/module'
    }
    '''
    chs = []
    faulty = []
    # Get the .py files in the current directory
    mod_dir = os.path.dirname(__file__)
    mod_dir = os.listdir(mod_dir)
    modules = [f[:len(f) - 3] for f in mod_dir if f[len(f) - 3:] == '.py']
    # Remove this file itself
    filename = os.path.basename(__file__)
    try:
        filename = re.sub(r'(.+).py[c]*', r'\1', filename)
        modules.remove(filename)
    except:
        pass
    # Dynamic Import (Relative)
    for mod in modules:
        try:
            module = importlib.import_module(
                '.{0}'.format(mod),
                package=__name__)
            # installing dependencies.
            try:
                dependencies = module.__dependencies__
            except AttributeError:
                # No dependencies defined.
                pass
            # look for an install function.
            try:
                installer = module.install
            except AttributeError:
                installer = None
            chs.append({
                'name': module.__Name__.strip(),
                'short': module.__short__.strip(),
                'description': module.__description__,
                'install': installer,
                'init': module.init,
                'doc': module.__doc__,
                'file': module.__file__
            })
        except AttributeError as err:
            # module loaded fine but some attribute is missing
            try:
                faulty.append({
                    'name': module.__Name__,
                    'short': module.__short__,
                    'file': module.__file__
                })
            except AttributeError:
                pass
        except ImportError as err:
            # module could not be loaded at all.
            # I suggest we delete it immediately
            pass
    return chs, faulty
