#!/usr/bin/env python3

import argparse
import boto3
import botocore
import configparser
import json
import sys
import os.path


def printjobs(jobs, header):
    if jobs["JobList"]:
        print(header)
        for job_detail in list(jobs["JobList"]):
            print(
                "Request: {0}\nAction: {1}, Status: {2}\n".format(
                    job_detail["JobId"], job_detail["StatusCode"], job_detail["Action"],
                )
            )


def main(config, args):
    client = boto3.client("glacier")

    if not args.save:
        if args.jobid:
            response = client.describe_job(
                accountId=config.get("glacier", "account_id"),
                jobId=args.jobid,
                vaultName=config.get("glacier", "vault"),
            )
            print(response)
        else:
            running_jobs = client.list_jobs(
                completed="false", vaultName=config.get("glacier", "vault")
            )
            printjobs(running_jobs, "Running Jobs")
            completed_jobs = client.list_jobs(
                completed="true", vaultName=config.get("glacier", "vault")
            )
            printjobs(completed_jobs, "Completed Jobs")
    else:
        try:
            response = client.get_job_output(
                vaultName=config.get("glacier", "vault"), jobId=args.jobid,
            )
            print(response)
        except:
            print("Retrieval not ready")

    """


    if jobid:
        try:
            contents = vault.get_job(jobid)
            if contents.action == u"InventoryRetrieval":
                if contents.completed:
                    list_of_files = {
                        x["ArchiveId"]: x for x in contents.get_output()["ArchiveList"]
                    }
                    contents_file = config.get("glacier", "contents")
                    if contents_file:
                        file = open(contents_file, "w+")
                        file.write(json.dumps(list_of_files))
                        file.close()
            else:
                if contents.completed:
                    if filename:
                        contents.download_to_file(filename)
                    else:
                        print("ERROR", "must have a filename")
        except UnexpectedHTTPResponseError as e:
            print("ERROR", json.loads(e.body)["message"])

    """


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read_file(
        open(os.path.join("/".join(sys.argv[0].split("/")[:-1]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Get glacier results.")
    parser.add_argument("jobid", help="Amazon Job ID", nargs="?")
    parser.add_argument("--save", help="save output", action="store_const", const=True)
    args = parser.parse_args()

    try:
        main(config, args)
    except KeyboardInterrupt:
        sys.exit()
