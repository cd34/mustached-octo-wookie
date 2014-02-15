#!/usr/bin/env python

import ConfigParser
import json
import sys
import os.path

from boto.glacier.layer1 import Layer1
from boto.glacier.exceptions import UnexpectedHTTPResponseError

def printjobs(jobs):
    for job_detail in jobs['JobList']:
        print 'Request: {0}\nAction: {1}, Status: {2}\n'.format(
            job_detail['JobId'], job_detail['StatusCode'],
            job_detail['Action'])

def main(jobid):
    layer1 = Layer1(aws_access_key_id=config.get('glacier',
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    vault = config.get('glacier', 'vault')
 
    if jobid:
        try:
            print layer1.get_job_output(vault, jobid)
        except UnexpectedHTTPResponseError as e:
            print 'ERROR', json.loads(e.body)['message']
            
    else:
        running_jobs = layer1.list_jobs(vault, completed=False)
        print 'Running Jobs'
        printjobs(running_jobs)
        completed_jobs = layer1.list_jobs(vault, completed=True)
        print 'Completed Jobs'
        printjobs(completed_jobs)
        

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
