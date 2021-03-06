#!/usr/bin/env python3

import argparse
import configparser as ConfigParser
import sys
import os

import libs.methods


def main(config, args):

    # if args.long:
    job = libs.methods.submitjob_glacier_contents(config)
    print(job)


# else:
#    uploads_list = libs.methods.get_quick_glacier_contents(
#        config.get("glacier", "vault")
#    )
#    print(uploads_list)


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join(os.path.dirname(sys.argv[0]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="List of Vault contents")
    parser.add_argument(
        "--long", action="store_const", const=True, default=False, help="fetch archive"
    )
    args = parser.parse_args()

    try:
        main(config, args)
    except KeyboardInterrupt:
        sys.exit()
