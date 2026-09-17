import os
import sys
import random
import string
import boto3
import configparser

creds = configparser.ConfigParser()
creds_path = '~/.aws/credentials'
creds_read = creds.read(os.path.expanduser(creds_path))

if not creds_read:
	sys.exit(f"Could not read credentials from {creds_path}.")

# Lecture 3 Slide 29
S3 = boto3.resource(
	's3',
	aws_access_key_id=creds['default']['aws_access_key_id'],
	aws_secret_access_key=creds['default']['aws_secret_access_key']
)

BUCKETS = S3.buckets.all()

def make_str_unique(original_str):
	unique_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
	return f"{original_str}-{unique_str}"

__all__ = ['S3', 'BUCKETS', 'make_str_unique']
