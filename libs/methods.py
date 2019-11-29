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
