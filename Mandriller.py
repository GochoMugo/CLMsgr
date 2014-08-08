'''

Mandriller
---------
Lets you send transactional emails using the Mandrill API.

Requires you:
 * register a valid API key with Mandrill at https://mandrillapp.com
 * username should be your registered Email Address.
 * install the mandrill module from pip ($ pip install mandrill)

'''

__Name__ = 'mandriller'
__short__ = 'md'
__description__ = 'Send transactional emails with Mandrill'
__version__ = '0.0.0-pre-alpha'
__author__ = '[GochoMugo](https://github.com/GochoMugo)'

import mandrill


# Asks for API key, Stores it.
def install(channel):
    names = channel.read('Names in Email header')
    key = channel.read('API key')
    key_stored = channel.store_config('key', key)
    names_stored = channel.store_config('names', names)
    if key_stored and names_stored:
        return True, 'Installed Successfully'
    else:
        return False, 'Installation failed'


def init(aim, msg, channel):
    key = channel.read_config('key')
    client = mandrill.Mandrill(key)
    message = {
        'subject': channel.read('Subject of Email'),
        'text': msg['content'],
        'from_email': channel.username,
        'from_name': channel.read_config('names'),
        'to': [{'email': i} for i in msg['to']]
    }
    response = client.messages.send(message)
    channel.listing('Sent successfully',
        [i['email'] for i in response if i['status'] == 'sent'])
    channel.listing('Pending',
        [i['email'] for i in response
            if i['status'] == 'queued' or i['status'] == 'scheduled'])
    channel.listing('Rejected',
        [i['email'] for i in response
            if i['status'] == 'rejected' or i['status'] == 'invalid'], 1)
    return True, 'Completed'
