import subprocess
import sys
import boto3
import datetime
from shlex import quote

s3 = boto3.client('s3')

def main(argv):
    cmd = argv
    log_file_name = datetime.datetime.now(datetime.timezone.utc).strftime("%m_%d_%Y") + "_logfile"
    kickoff_subprocess(cmd, log_file_name)
    upload_output_to_S3(log_file_name)

def kickoff_subprocess(cmd, log_file_name):
    process = subprocess.call(quote(cmd), shell=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
    output = timestamp + " Command: "+ cmd[0] + " | Return Code: " + str(process) + "\n"
    with open(log_file_name, "a+") as f:
        f.write(output)

def upload_output_to_S3(log_file_name):
    with open(log_file_name, "rb") as f:
        s3.upload_fileobj(f, "<FMI1>", log_file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
