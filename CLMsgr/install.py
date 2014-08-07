'''
Handles installing and uninstalling ofapplication
and channel modules onto the user's computer
'''

import ast
import os
import random
import re
import shutil
from.chs import channels as get_channels
from .core import __app_dir__
from .core import __chs_dir__
from .core import channel
from .core import io

# NOTE: we can NOT import `api` here cause this module
# itself is imported in the `api` module


def install():
    ''' Function called first time the Application is being installed on
    the User's machine.
    '''

    io.write('', 'Installing tuma...')

    # Create the App directory
    if not os.path.exists(__app_dir__):
        os.mkdir(__app_dir__)

    # Run Installation Process of Channels
    channels, faulty = get_channels()
    for channel in channels:
        if 'install' in channel:
            io.write(channel['name'], 'Installing...')
            if channel['install']():
                io.write(channel['name'], 'Installed successfully...')
            else:
                io.write(channel['name'], 'Installation failed...', 1)


def verify_module(path, installed_channels):
    ''' Verify that the module is in good condition.
    `path` - path to the module file
    `install_channels` - all the installed channels
    Returns True is good. False if with errors.

    This tries to ensure that a module can be installed/uinstalled.
    def test_channels(self):
        'test the returned channels have all properties'
        chs = api.channels
        points = ['name', 'short', 'info', 'init']
        for ch in chs:
            for point in points:
                self.assertIn(point, ch,
                    'Missing property "{0}" in retrieved channel: {1}'.format(
                        point, ch))
    '''
    channel_names = [i['name'] for i in installed_channels]
    # Read the file looking for Gross Mistakes
    with open(path, 'r') as mod_file:
        content = mod_file.read()

        # Ensure it is syntatically correct SAFELY!!!!! No mischief pls.
        try:
            ast.parse(content)
        except SyntaxError:
            io.write('', 'SyntaxError found: {0}'.format(path), 1)
            return False

        requirements = ['Name', 'short', 'description']
        for requirement in requirements:
            patt = r'.*__{0}__\s*=\s*(\'|")(.*)(\'|").*'.format(requirement)
            name = re.search(patt, content)
            # Ensuring the requirement is given
            if not name:
                io.write('',
                         '__{0}__ missing: {1}'.format(requirement, path),
                         1)
                return False

            # Ensure it is not a blank requirement
            name = name.group(2).strip()
            if name == '':
                io.write('',
                         '__{0}__ is blank: {1}'.format(requirement, path),
                         1)
                return False

            if requirement == 'Name':
                # and that Name is Not already registered
                if name in channel_names:
                    io.write('',
                             '__{0}__ already registered: {1}'.format(
                                 requirement, name),
                             1)
                    return False

        return True
    return False


def install_channel(module_paths, installed_channels):
    ''' Install new channels.
    `module_paths` is an array of paths to the python file
        for channel module '''
    for module_path in module_paths:
        # Ensure it is a Python file
        if module_path[len(module_path) - 3:] != '.py':
            io.write('', 'Not a Python File: {0}'.format(module_path))
            break
        # Ensure it actually exists
        if not os.path.exists(module_path):
            io.write('', 'Not Found: {0}'.format(module_path))
            break
        if verify_module(module_path, installed_channels):
            # Now we copy using a random filename to avoid any
            # possible overwrites
            new_filename = ''.join([
                str(random.randint(1, 9999)),
                module_path])
            new_module = os.path.join(__chs_dir__, new_filename)
            shutil.copy2(module_path, new_module)
            io.write('', 'Installed: {0}'.format(module_path))


def uninstall_channel(channels, all_channels):
    ''' Uninstall channels.
    `channels` is a list of channels we want to delete '''
    for channel in channels:
        # Look for the filename of the module
        found = False
        for one_channel in all_channels:
            if one_channel['name'] == channel:
                # We found the module
                found = True
                # Now removing using the file path.It may be .py or .pyc
                filename = one_channel['file']
                name = re.search(r'(.*)\.py[c]*$', filename).group(1)
                removed = 0
                for ext in ['py', 'pyc']:
                    try:
                        os.unlink('{0}.{1}'.format(name, ext))
                        removed += 1
                    except OSError:
                        pass
                if removed > 0:
                    io.write('', 'Uninstalled: {0}'.format(channel))
                elif removed == 0:
                    io.write('', 'Failed to uninstall: {0}'.format(channel), 1)
                break
        if not found:
            io.write('', 'Channel module not found: {0}'.format(channel), 1)
