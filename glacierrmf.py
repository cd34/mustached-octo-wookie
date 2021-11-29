#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import os
import sys

import libs.methods


def main(config, args):
    files = libs.methods.get_local_contents(config)
    file_to_key = {files[x]["ArchiveDescription"]: x for x in files.keys()}

    if args.file in file_to_key:
        upload_id = file_to_key[args.file]
        try:
            libs.methods.rm_glacier_contents(config.get("glacier", "vault"), upload_id)
            libs.methods.delete_local_contents(config, upload_id)
        except:
            print(f"{upload_id} not found")
    else:
        print(f"{args.file} not found")


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join(os.path.dirname(sys.argv[0]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Remove files from glacier.")
    parser.add_argument("file", help="filename")
    args = parser.parse_args()

    try:
        main(config, args)
    except KeyboardInterrupt:
        sys.exit()
