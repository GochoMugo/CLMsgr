'''
Updates the README with new channels
'''

import importlib
import json
import os
import re


def generateTable():
    tags = ['Name', 'version', 'author', 'description', 'file', ]
    content = []
    # Look for the names in the upper folder
    files = os.listdir('.')
    files = [f for f in files if f[len(f) - 3:] == '.py']
    files.sort()
    for pyFile in files:
        with open(pyFile, 'r') as module:
            module = module.read()
            found = []
            for tag in tags:
                pattern = '__{0}__\s*=\s*[\'\"]+(.*)[\'\"]'.format(tag)
                hit = re.search(pattern, module)
                if hit:
                    found.append(hit.group(1))
            # Adding the filename
            found.append(pyFile)
        if len(found) == len(tags):
            content.append(''.join(['|', '|'.join(found), '|']))
    body =  '\n'.join(content)
    head = ''.join(['|', '|'.join(tags), '|'])
    sep = ''.join(['|', '|'.join(['-----' for i in tags]), '|'])
    return '\n'.join([head, sep, body])


def README():
    with open('utils/README.md', 'r+') as readme:
        content = readme.read()
        content = content.format(table=generateTable())
        with open('./README.md', 'w') as newReadme:
            newReadme.write(content)


if __name__ == '__main__':
    README()
    print('README updated')
