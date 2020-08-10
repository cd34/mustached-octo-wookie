#!/usr/bin/env python3

import configparser as ConfigParser
import sys
import os
import json


def main():
    file = open(config.get("glacier", "contents"), "r")
    existing_contents = json.loads(file.read())
    for item in existing_contents.items():
        print(
            item[1]["ArchiveDescription"],
            item[1]["CreationDate"],
            item[1]["Size"],
            item[0],
        )


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
