
# channel API #

> A Programmer's cheat sheet.

## Channel Definition ##

Required:

* `__Name__`: 'name_of_channel',
* `__short__`: 'short_abbreviation',
* `__description__`: 'short description of channel',
* `__doc__`: 'documentation of the channel',
* An initialization function of the channel named `init`

Optional:

* `__install__`: installation_func_of_channel/None.


## Topics ##

1. **initialization_function(aim, msg, channel)**

    * **aim**s that may be passed include:

        - **fetch**: check for new messages
        - **send**: send new messages
        - **broadcast**: broadcast message to all users
        - **users**: show users user can message

    * **msg**, an object with the following attributes:

        - **to**: List of Users to send message to. e.g. `msg['to']`
        - **content**:  be a String of the message or None if none has been passed. e.g. `msg['content']`

    * **channel** is an object with the following attributes/methods:

        - **username**: string representing the username registered to account. e.g. `myUsername = channel.username`
        - **read(prompt)**: get input from user. e.g. `channel.read('Do I ask for time over there?')`
        - **listing(heading, items)**: items must be iterable. e.g. `channel.listing(AllUsersList)`
        - **msg(sender, content)**: handles showing new messages to user. e.g. `channel.msg('moonServer', message)`
        - **getpass(prompt)**: get password from user. e.g. `key = channel.getpass('I need the key')`
        - **success(msg)**: show a success message to user. e.g. `channel.success('All sent')`
        - **error(msg)**: show an error message to user. e.g. `channel.error('Failed to send')`
        - **read_config(key)**: read configuration e.g. `channel.read_config('isAlien')`
        - **store_config(key, value)**: store a configuration. e.g. `channel.store_config('isAlien', True)`

    A handler should return a tuple: `True/False, 'message to show to user'`

2. **installation_function()**

This function will be run when user is registering a new account for the channel. No parameter is passed to the Function. It should Return `True` for Success. `False` for Errors.


## Notes: ##

1. It is `__Name__` and **NOT** `__name__`
* It is acceptable not to handle an `aim`. It will just be handled as Unsupported.
* Do NOT directly output messages to user. Use the `channel` object to allow consistent user interface.
* We are Consenting Adults.

## Example ##

```python

__Name__ = 'moonServer'
__short__ = 'mS'
__description__ = 'my Server on the Moon'
__doc__ = '''
moonServer
----------
You might wonder how I got a server on the moon? Well, lets just say "am a tourist on planet Earth"

You Ping Ping my Server, my Server Pong Pong you.
'''
__version__ = '0.99.0'
__author__ = '@gochomugo'

def init(aim, msg, channel):
    if aim is 'fetch':
        # call some function here to fetch messages from wherever
        msgs = fetch()
        channel.msgs(msgs) # msgs is iterable
        return True, 'Got ALL new messages'
    elif aim is 'broadcast':
        # broadcast the message content to everyone. here we just know
        # know the moonServer
        status = sendToAllReceipeints(msg['content'])
        if status:
            return True, 'All messages sent successfully'
        else:
            return False, 'Sending failed.'
    elif aim is 'send':
        # sending a message to some one(s). Hurry...
        status = sendToManyReceipeints(msg['to'], msg['content'])
        if status:
            return True, 'All messages sent successfully'
        else:
            return False, 'Sending failed.'
    elif aim is 'users':
        # who do we know about?
        channel.listing(myUsers)
        return True, 'All Users shown'

```
