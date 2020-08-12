#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import os
import sys

import libs.methods


def main(args, config):
    for file in args.filename:
        id = libs.methods.upload_file(config, file)
        base_file = os.path.basename(file)
        if id:
            print(f"Uploaded {base_file}")


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join(os.path.dirname(sys.argv[0]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Upload files to glacier.")
    parser.add_argument("filename", help="Files or glob", nargs="+")
    args = parser.parse_args()

    try:
        main(args, config)
    except KeyboardInterrupt:
        sys.exit()
