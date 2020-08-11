import datetime
import json
import os

import boto3

def get_quick_glacier_contents(vault):
    glacier = boto3.client('glacier')
    request_args = {'vaultName':vault}
    uploads_list = []
    more_pages = True
    while more_pages:
        response = glacier.list_multipart_uploads(**request_args)
        uploads_list.extend(response['UploadsList'])
        if 'Marker' not in response:
            more_pages = False
        else:
            request_args['marker'] = response['Marker']
    return uploads_list

def submitjob_glacier_contents(account_id, vault):
    glacier = boto3.resource('glacier')
    vault = glacier.Vault('account_id','name')
    job = vault.initiate_inventory_retrieval()
    return job

def rm_glacier_contents(vault, upload_id):
    glacier = boto3.client('glacier')
    request_args = {'vaultName':vault,
      'archiveId':upload_id}
    response = glacier.delete_archive(**request_args)
    return response['ResponseMetadata']['HTTPStatusCode'] == 204

def get_local_contents(config):
    contents_file = config.get('glacier','contents')
    existing_contents = {}
    if contents_file:
        try:
            file = open(contents_file, 'r+')
            existing_contents = json.loads(file.read())
        except IOError:
            file = open(contents_file, 'w+')
        file.close()
    return existing_contents

def update_local_contents(config, id, file):
    contents_file = config.get('glacier','contents')
    source_dir = config.get("rsync", "source_dir")
    filename = os.path.join(source_dir,file)
    filesize = 0
    try:
        filesize = os.stat(filename).st_size
    except OSError:
        pass

    list_of_files = {id:{'ArchiveId':id,
        'ArchiveDescription':file,
        'CreationDate':datetime.datetime.now(). \
            strftime('%Y-%m-%dT%H:%M:%SZ'),
        'Size':filesize}}
    print(list_of_files)
    """
    if contents_file:
        file = open(contents_file, 'w+')
        list_of_files = dict(list_of_files.items() + \
            existing_contents.items())
        file.seek(0)
        file.write(json.dumps(list_of_files))
        file.close()
    """
