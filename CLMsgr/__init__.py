'''
CLMsgr (Commandline Messenger)
----------------------------------
This is the core of the Messenger. It aims to be a mature and
object oriented framework for writing command line messaging
applications that mainly aim at sending and receiving their
messages.

It is written in python. Well, javascript is the it-lang in internet
applications but this core wants to utilize the Object Orientation
of Python, its maturity and vast capabilities when it comes to
operating on a system.


'''


__version__ = '0.0.0-pre-alpha-build-1'

from .cli import run
from .install import install

__all__ = ['run', 'install', ]
