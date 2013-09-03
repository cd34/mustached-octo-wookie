#!/usr/bin/env python

"""
M4ofpKwzspYNJrJqgHUdONtlqr9IDFPDl5TWp7pTFG8HCTQjd2w37PAIPy2IOcAq0tTmD3MdgA-lBuPFaQfgpiDncKEQ
"""

import ConfigParser
import sys
import os.path

from boto.glacier.layer1 import Layer1

def main(jobid):
    layer1 = Layer1(aws_access_key_id=config.get('glacier',
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    vault = config.get('glacier', 'vault')
 
    if jobid:
        print layer1.get_job_output(vault, jobid)
    else:
        print layer1.list_jobs(vault, completed=False)

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join('/'.join(sys.argv[0].split('/')[:-1]),
        'glacierputter.cfg')))
    
    try:
        if(len(sys.argv) < 2):
            jobid = None
        else:
            jobid = sys.argv[1]
        main(jobid)
    except KeyboardInterrupt:
        sys.exit()
