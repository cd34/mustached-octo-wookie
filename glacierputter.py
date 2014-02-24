#!/usr/bin/env python

import ConfigParser
import datetime
import json
import os
import sys

from boto.glacier.layer1 import Layer1
from boto.glacier.concurrent import ConcurrentUploader

def main():
    layer1 = Layer1(aws_access_key_id=config.get('glacier', 
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    threads = 1
    try:
        threads = config.get('glacier', 'threads')
    except ConfigParser.NoOptionError:
        pass
    uploader = ConcurrentUploader(layer1, config.get('glacier', 'vault'),
        part_size=128*1024*1024, num_threads=threads)

    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                archive_description = filename.split('/')[-1]
                id = uploader.upload(filename, archive_description)
                print 'Uploaded: {0}, id: {1}'.format(filename, id) 
                filesize = 0
                try:
                    filesize = os.stat(filename).st_size
                except OSError:
                    pass
                
                contents_file = config.get('glacier','contents')
                list_of_files = {id:{'ArchiveId':id, 
                    'ArchiveDescription':archive_description,
                    'CreationDate':datetime.datetime.now(). \
                        strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'Size':filesize}}
                if contents_file:
                    existing_contents = {}
                    try:
                        file = open(contents_file, 'r+')
                        existing_contents = json.loads(file.read())
                    except IOError:
                        file = open(contents_file, 'w+')
                    list_of_files = dict(list_of_files.items() + \
                        existing_contents.items())
                    file.seek(0)
                    file.write(json.dumps(list_of_files))
                    file.close()
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
