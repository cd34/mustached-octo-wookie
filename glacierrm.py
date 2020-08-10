#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import os
import json
import sys

import libs.methods


def main(config, args):
    result = libs.methods.rm_glacier_contents(
        config.get("glacier", "vault"), args.upload_id
    )

    contents_file = config.get("glacier", "contents")
    if contents_file:
        file = open(contents_file, "r")
        existing_contents = json.loads(file.read())
        file.close()
        existing_contents.pop(args.upload_id, None)
        file = open(contents_file, "w")
        file.write(json.dumps(existing_contents))
        file.close()


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Remove files from glacier.")
    parser.add_argument("upload_id", help="upload_id")
    args = parser.parse_args()

    try:
        main(config, args)
    except KeyboardInterrupt:
        sys.exit()
