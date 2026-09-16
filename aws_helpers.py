import os
import sys
import boto3
import configparser

creds = configparser.ConfigParser()
creds_path = '~/.aws/credentials'
creds_read = creds.read(os.path.expanduser(creds_path))

if not creds_read:
	sys.exit(f"Could not read credentials from {creds_path}.")

S3 = boto3.resource(
	's3',
	aws_access_key_id=creds['default']['aws_access_key_id'],
	aws_secret_access_key=creds['default']['aws_secret_access_key']
)

BUCKETS = S3.buckets.all()

__all__ = ['S3', 'BUCKETS']
