#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import datetime
import json
import os
import sys

import boto3
import libs.methods


def main(args, config):
    #uploads_list = libs.methods.get_glacier_contents(config.get("glacier", "vault"))

    client = boto3.client('glacier')

    for file in args.filename:
        existing_contents = libs.methods.get_local_contents(config)
        existing_files = [x["ArchiveDescription"] for x in existing_contents.values()]
        if file not in existing_files:
            with open(file, 'rb') as f:
                response = client.upload_archive(vaultName=config.get("glacier", "vault"),
                    archiveDescription=os.path.basename(file),
                    body=f)
                id = response['archiveId']
                libs.methods.update_local_contents(config, id, os.path.basename(file))




    """
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            contents_file = config.get('glacier','contents')
            if contents_file:
                try:
                    file = open(contents_file, 'r+')
                    existing_contents = json.loads(file.read())
                except IOError:
                    file = open(contents_file, 'w+')
                file.close()
            filenames = [x['ArchiveDescription'] for x in \
                existing_contents.values()]
            archive_description = filename.split('/')[-1]
            if os.path.isfile(filename) and archive_description \
                not in filenames:
                #id = uploader.upload(filename, archive_description)
                file = open(filename, 'rb')
                response = glacier.upload_archive(
                    vaultName=config.get('glacier', 'vault'),
                    archiveDescription=archive_description,
                    body=file.read(),
                )
                id = response['archiveId']
                print('Uploaded: {0}, id: {1}'.format(filename, id))
                filesize = 0
                try:
                    filesize = os.stat(filename).st_size
                except OSError:
                    pass
                
                #contents_file = config.get('glacier','contents')
                list_of_files = {id:{'ArchiveId':id, 
                    'ArchiveDescription':archive_description,
                    'CreationDate':datetime.datetime.now(). \
                        strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'Size':filesize}}
                if contents_file:
                    file = open(contents_file, 'w+')
                    list_of_files = dict(list_of_files.items() + \
                        existing_contents.items())
                    file.seek(0)
                    file.write(json.dumps(list_of_files))
                    file.close()
            else:
                if not os.path.isfile(filename):
                    print('Couldn\'t find file: {0}'.format(filename))
                else:
                    print('File {filename} is already in glacier' \
                        .format(filename=filename))
    """


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Upload files to glacier.")
    parser.add_argument("filename", help="Files or glob", nargs="+")
    args = parser.parse_args()

    try:
        main(args, config)
    except KeyboardInterrupt:
        sys.exit()
