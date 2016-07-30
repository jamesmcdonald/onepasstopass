#!/usr/bin/env python3

"""Import 1Password export file into pass"""

from __future__ import print_function

import sys
import json
from subprocess import Popen, PIPE

class Importer(object):
    """Import 1Password export file into pass"""
    entries = []

    def __init__(self, inputfile):
        self.parse(inputfile)

    def __iter__(self):
        for item in self.entries:
            yield item

    def __len__(self):
        return len(self.entries)

    def parse(self, inputfile):
        """Parse an input file into internal data structure"""
        for line in inputfile.readlines():
            # Skip the separator lines
            if line.startswith('*'):
                continue
            data = json.loads(line)
            entry = {}
            if data['typeName'] != 'webforms.WebForm':
                print("Warning: entry {} of type {} not imported".format(
                    data['title'], data['typeName']), file=sys.stderr)
                continue
            entry['title'] = data['title']
            if 'locationKey' in data and data['locationKey'] != '':
                entry['location'] = data['locationKey']
            if 'notesPlain' in data['secureContents']:
                entry['notes'] = data['secureContents']['notesPlain']
            for field in data['secureContents']['fields']:
                if 'designation' in field:
                    if field['designation'] == 'username' and field['value'] != '':
                        entry['username'] = field['value']
                    if field['designation'] == 'password':
                        entry['password'] = field['value']
            path = []
            if 'location' in entry:
                path.append('website')
                path.append(entry['location'])
            else:
                path.append('misc')
                path.append(entry['title'])
            entry['path'] = '/'.join(path)

            content = []
            content.append(entry['password'])
            if 'username' in entry:
                content.append("Username: " + entry['username'])
            if 'notes' in entry:
                content.append(entry['notes'])
            entry['content'] = '\n'.join(content)

            self.entries.append(entry)

    def dump(self, dumpcontent=False):
        """Dump imported entries to stdout"""
        for entry in self:
            print('--- ' + entry['path'])
            if dumpcontent:
                print(entry['content'])

    def sendtopass(self):
        """Send entries to pass"""
        for entry in self:
            print("Adding {}...".format(entry['path']))
            sub = Popen(["pass", "insert", "-m", entry['path']], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            sub.communicate((entry['content'] + '\n').encode())

with open(sys.argv[1]) as pf:
    i = Importer(pf)
    i.sendtopass()
