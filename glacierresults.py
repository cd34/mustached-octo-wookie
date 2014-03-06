#!/usr/bin/env python

import ConfigParser
import json
import sys
import os.path

from boto.glacier.layer2 import Layer2
from boto.glacier.exceptions import UnexpectedHTTPResponseError

def printjobs(jobs, header):
    if jobs:
        print header
        for job_detail in jobs:
            print 'Request: {0}\nAction: {1}, Status: {2}\n'.format(
                job_detail.id, job_detail.status_code,
                job_detail.description)

def main(jobid, filename):
    layer2 = Layer2(aws_access_key_id=config.get('glacier',
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))
    vault = layer2.get_vault(config.get('glacier', 'vault'))
 
    if jobid:
        try:
            contents = vault.get_job(jobid)
            if contents.action == u'InventoryRetrieval':
                if contents.completed:
                    list_of_files = {x['ArchiveId']:x for x in \
                        contents.get_output()['ArchiveList']}
                    contents_file = config.get('glacier','contents')
                    if contents_file:
                        file = open(contents_file, 'w+')
                        file.write(json.dumps(list_of_files))
                        file.close()
            else:
                if contents.completed:
                    if filename:
                        contents.download_to_file(filename)
                    else:
                        print 'ERROR', 'must have a filename'
        except UnexpectedHTTPResponseError as e:
            print 'ERROR', json.loads(e.body)['message']
            
    else:
        running_jobs = vault.list_jobs(completed=False)
        printjobs(running_jobs, 'Running Jobs')
        completed_jobs = vault.list_jobs(completed=True)
        printjobs(completed_jobs, 'Completed Jobs')
        

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join('/'.join(sys.argv[0].split('/')[:-1]),
        'glacierputter.cfg')))
    
    try:
        if(len(sys.argv) < 2):
            jobid = None
            filename = None
        else:
            jobid = sys.argv[1]
            filename = sys.argv[2]
        main(jobid, filename)
    except KeyboardInterrupt:
        sys.exit()
