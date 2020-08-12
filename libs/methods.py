import datetime
import json
import os

import boto3


def get_quick_glacier_contents(vault):
    glacier = boto3.client("glacier")
    request_args = {"vaultName": vault}
    uploads_list = []
    more_pages = True
    while more_pages:
        response = glacier.list_multipart_uploads(**request_args)
        uploads_list.extend(response["UploadsList"])
        if "Marker" not in response:
            more_pages = False
        else:
            request_args["marker"] = response["Marker"]
    return uploads_list


def submitjob_glacier_contents(config):
    glacier = boto3.resource("glacier")
    vault = glacier.Vault(
        config.get("glacier", "account_id"), config.get("glacier", "vault")
    )
    job = vault.initiate_inventory_retrieval()
    return job


def rm_glacier_contents(vault, upload_id):
    glacier = boto3.client("glacier")
    request_args = {"vaultName": vault, "archiveId": upload_id}
    response = glacier.delete_archive(**request_args)
    return response["ResponseMetadata"]["HTTPStatusCode"] == 204


def upload_file(config, file):

    id = None
    client = boto3.client("glacier")

    existing_contents = get_local_contents(config)
    existing_files = [x["ArchiveDescription"] for x in existing_contents.values()]
    base_file = os.path.basename(file)
    if base_file not in existing_files and os.path.isfile(file):
        with open(file, "rb") as f:
            print(f"Uploading {base_file}")
            response = client.upload_archive(
                vaultName=config.get("glacier", "vault"),
                archiveDescription=base_file,
                body=f,
            )
            id = response["archiveId"]
            update_local_contents(config, id, file)
    else:
        if not os.path.isfile(file):
            print(f"Couldn't find file: {file}")
        else:
            print(f"File {file} is already in glacier")

    return id


def get_local_contents(config):
    contents_file = config.get("glacier", "contents")
    existing_contents = {}
    if contents_file:
        try:
            file = open(contents_file, "r+")
            try:
                existing_contents = json.loads(file.read())
            except json.JSONDecodeError:
                existing_contents = {}
        except IOError:
            file = open(contents_file, "w+")
        file.close()
    return existing_contents


def update_local_contents(config, id, filename):
    contents_file = config.get("glacier", "contents")
    source_dir = config.get("rsync", "source_dir")
    filesize = 0
    try:
        filesize = os.stat(filename).st_size
    except OSError:
        pass

    list_of_files = {
        id: {
            "ArchiveId": id,
            "ArchiveDescription": os.path.basename(filename),
            "CreationDate": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "Size": filesize,
        }
    }
    if contents_file:
        existing_contents = get_local_contents(config)
        file = open(contents_file, "w+")
        json_dict = {**list_of_files, **existing_contents}
        file.seek(0)
        file.write(json.dumps(json_dict))
        file.close()
