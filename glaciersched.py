#!/usr/bin/env python

import argparse
import configparser as ConfigParser
import datetime
import os
import sys
import time

import libs.methods


def main(args, config):
    time_average = 0
    time_count = 0
    time_start = datetime.datetime.now()
    time_end = time_start + datetime.timedelta(hours=args.hours)
    print(time_start, time_end)
    for file in args.filename:
        if (
            datetime.datetime.now() + datetime.timedelta(seconds=time_average)
            < time_end
        ):
            call_start = time.time()
            libs.methods.upload_file(config, file)
            call_end = time.time()
            time_count += 1
            time_average = (time_average + (call_start - call_end)) / time_count


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Script to upload files to glacier.")
    parser.add_argument("hours", help="Number of hours to schedule", type=int)
    parser.add_argument("filename", help="Files or glob", nargs="+")
    args = parser.parse_args()

    try:
        main(args, config)
    except KeyboardInterrupt:
        sys.exit()
