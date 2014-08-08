'''
CLMsgr
~~~~~
A Python Core for Command Line Messaging, with extensibility and modularity

Licensed under the MIT License. For Open Source Initiative (OSI)

Contribute to the Project at https://github.com/GochoMugo/CLMsgr
'''

from setuptools import find_packages
from setuptools import setup
import CLMsgr


setup(
    name="CLMsgr",
    version=CLMsgr.__version__,
    author="Gocho Mugo I",
    author_email="gochomugo.developer@gmail.com",
    url="https://github.com/GochoMugo/CLMsgr",
    download_url="https://github.com/GochoMugo/CLMsgr/zipball/master",
    description="A Python Core for Command Line Messaging, with extensibility and modularity",
    keywords=["commands", "messaging", "core", "cli"],
    license="MIT",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
    install_requires=[
        "argparse",
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'CLMsgr = CLMsgr.cli:run',
        ]
    }
)
