#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import os
import sys

import boto3
import libs.methods


def main(args, config):
    client = boto3.client("glacier")

    for file in args.filename:
        existing_contents = libs.methods.get_local_contents(config)
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
                libs.methods.update_local_contents(config, id, os.path.basename(file))
        else:
            if not os.path.isfile(file):
                print(f"Couldn't find file: {file}")
            else:
                print(f"File {file} is already in glacier")


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
