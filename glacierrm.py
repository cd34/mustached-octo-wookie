#!/usr/bin/env python

import ConfigParser
import os
import json
import sys

from boto.glacier.layer1 import Layer1

def main(archive_id):
    layer1 = Layer1(aws_access_key_id=config.get('glacier', 
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    if len(sys.argv) > 1:
        vault = config.get('glacier', 'vault')
        layer1.delete_archive(vault, archive_id) 
        contents_file = config.get('glacier','contents')
        if contents_file:
            file = open(contents_file, 'r')
            existing_contents = json.loads(file.read())
            file.close()
            existing_contents.pop(archive_id, None)
            file = open(contents_file, 'w')
            file.write(json.dumps(existing_contents))
            file.close()
    else:
        print """\
Need at least one filename on the command line, can accept globs.

Example:

{0} *.py""".format(sys.argv[0])


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join('/'.join(sys.argv[0].split('/')[:-1]),
        'glacierputter.cfg')))

    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        sys.exit()
