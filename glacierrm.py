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

    libs.methods.delete_local_contents(config, args.upload_id)


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
