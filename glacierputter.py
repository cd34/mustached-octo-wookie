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
    uploads_list = libs.methods.get_glacier_contents(config.get("glacier", "vault"))
    pprint.pprint(uploads_list)

    """
    glacier = boto3.client('glacier')
    layer1 = Layer1(aws_access_key_id=config.get('glacier', 
         'aws_access_key_id'), aws_secret_access_key=config.get('glacier',
         'aws_secret_access_key'), region_name=config.get('glacier',
         'region'))

    threads = 1
    try:
        threads = config.getint('glacier', 'threads')
    except ConfigParser.NoOptionError:
        pass
    uploader = ConcurrentUploader(layer1, config.get('glacier', 'vault'),
        part_size=128*1024*1024, num_threads=threads)
    """

    """
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            contents_file = config.get('glacier','contents')
            existing_contents = {}
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
