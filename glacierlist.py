#!/usr/bin/env python

import ConfigParser
import sys
import os

from boto.glacier.layer1 import Layer1

def main():
    layer1 = Layer1(aws_access_key_id=config.get('glacier',
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))
 
    job_id = layer1.initiate_job(config.get('glacier','vault'),
        {"Description":"inventory-job", "Type":"inventory-retrieval",
        "Format":"JSON"})
 
    print 'Inventory job id: {0}'.format(job_id)

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join('/'.join(sys.argv[0].split('/')[:-1]),
        'glacierputter.cfg')))
    
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
