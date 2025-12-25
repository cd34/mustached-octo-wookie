#!/usr/bin/env python3

import configparser as ConfigParser
import sys
import os
import libs.methods


def main(config):
    existing_contents = libs.methods.get_local_contents(config)
    for item in existing_contents['ArchiveList']:
        print(
            item["ArchiveDescription"],
            item["CreationDate"],
            item["Size"],
            item["ArchiveId"],
        )


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join(os.path.dirname(sys.argv[0]), "glacierputter.cfg"))
    )

    try:
        main(config)
    except KeyboardInterrupt:
        sys.exit()
