#!/usr/bin/env python

import ConfigParser
import os
import sys

from boto.glacier.layer1 import Layer1
from boto.glacier.concurrent import ConcurrentUploader

def main():
    layer1 = Layer1(aws_access_key_id=config.get('glacier', 
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    uploader = ConcurrentUploader(layer1, config.get('glacier', 'vault'),
        part_size=128*1024*1024, num_threads=4)

    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                id = uploader.upload(filename, filename)
                print 'Uploaded: {0}, id: {1}'.format(filename, id) 
            else:
                print 'Couldn\'t find file: {0}'.format(filename) 
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
        main()
    except KeyboardInterrupt:
        sys.exit()
