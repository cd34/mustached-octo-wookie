#!/usr/bin/env python

import configparser as ConfigParser
import datetime
import glob
import json
import os
import sys

"""
[rsync]
source_dir = /var/www/cd34.com/testmovies
destination_host = li.daviesinc.com
destination_dir = /var/www/cd34.com/movies
bw_limit = 24
"""


def main():
    source_dir = config.get("rsync", "source_dir")
    for filename in glob.glob(os.path.join(source_dir, "*.mp4")):
        contents_file = config.get("glacier", "contents")
        existing_contents = {}
        if contents_file:
            try:
                file = open(contents_file, "r+")
                existing_contents = json.loads(file.read())
            except IOError:
                file = open(contents_file, "w+")
            file.close()
        filenames = [x["ArchiveDescription"] for x in existing_contents.values()]
        archive_description = filename.split("/")[-1]
        if os.path.isfile(filename) and archive_description not in filenames:
            print("rsync: {filename}".format(filename=filename))
            print("Uploaded: {0}, id: {1}".format(filename, id))
            filesize = 0
            try:
                filesize = os.stat(filename).st_size
            except OSError:
                pass

            # contents_file = config.get('glacier','contents')
            """
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
            """
        else:
            if not os.path.isfile(filename):
                print("Couldn't find file: {0}".format(filename))
            else:
                print("File {filename} is already in glacier".format(filename=filename))


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
