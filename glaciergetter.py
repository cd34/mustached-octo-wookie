#!/usr/bin/env python

import configparser as ConfigParser
import sys
import os

from boto.glacier.layer2 import Layer2


def main(id):
    layer2 = Layer2(
        aws_access_key_id=config.get("glacier", "aws_access_key_id"),
        aws_secret_access_key=config.get("glacier", "aws_secret_access_key"),
        region_name=config.get("glacier", "region"),
    )
    vault = layer2.get_vault(config.get("glacier", "vault"))

    job_id = vault.retrieve_archive(id)

    print("Inventory job id: {0}".format(job_id))


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        sys.exit()
