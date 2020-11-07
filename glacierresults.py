#!/usr/bin/env python3

import argparse
import boto3
import configparser
import io
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

    if not args.save_contents and not args.save:
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
            if args.save:
                response = client.get_job_output(
                    vaultName=config.get("glacier", "vault"), jobId=args.jobid,
                )
                with io.FileIO("/tmp/glacier.output", "w") as file:
                    for i in response['body']:
                        file.write(i)
            if args.save_contents:
                response = client.get_job_output(
                    vaultName=config.get("glacier", "vault"), jobId=args.jobid,
                )
                file_listing = {}
                for l in json.loads(response["body"].read())["ArchiveList"]:
                    file_listing[l["ArchiveId"]] = {
                        "ArchiveId": l["ArchiveId"],
                        "ArchiveDescription": l["ArchiveDescription"],
                        "SHA256TreeHash": l["SHA256TreeHash"],
                        "Size": l["Size"],
                        "CreationDate": l["CreationDate"],
                    }

                contents_file = config.get("glacier", "contents")
                file = open(contents_file, "w")
                file.write(json.dumps(file_listing))
                file.close()
        except:
            print("Retrieval not ready")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read_file(
        open(os.path.join(os.path.dirname(sys.argv[0]), "glacierputter.cfg"))
    )

    parser = argparse.ArgumentParser(description="Get glacier results.")
    parser.add_argument("jobid", help="Amazon Job ID", nargs="?")
    parser.add_argument("--save", help="save output", action="store_const", const=True)
    parser.add_argument("--save-contents", help="save directory contents", action="store_const", const=True)
    args = parser.parse_args()

    try:
        main(config, args)
    except KeyboardInterrupt:
        sys.exit()
