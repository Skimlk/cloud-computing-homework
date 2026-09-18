import os
import sys
import time
import random
import json
import string
import boto3
import configparser

creds = configparser.ConfigParser()
creds_path = '~/.aws/credentials'
creds_read = creds.read(os.path.expanduser(creds_path))

if not creds_read:
	sys.exit(f"Could not read credentials from {creds_path}.")

# Lecture 3 Slide 29
S3_RESOURCE = boto3.resource(
	's3',
	aws_access_key_id=creds['default']['aws_access_key_id'],
	aws_secret_access_key=creds['default']['aws_secret_access_key']
)

S3_CLIENT = boto3.client(
	's3',
	aws_access_key_id=creds['default']['aws_access_key_id'],
	aws_secret_access_key=creds['default']['aws_secret_access_key']
)

def get_buckets():
	return S3_RESOURCE.buckets.all()

def enable_public_bucket_access(bucket_name):
	S3_CLIENT.put_public_access_block(
		Bucket=bucket_name,
		PublicAccessBlockConfiguration={
			'BlockPublicAcls': False,
			'IgnorePublicAcls': False,
			'BlockPublicPolicy': False,
			'RestrictPublicBuckets': False
		}
	)

	time.sleep(2)

	policy_payload = {
		"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "MakeItPublic",
				"Effect": "Allow",
				"Principal": "*",
				"Action": "s3:GetObject",
				"Resource": "arn:aws:s3:::%s/*" % bucket_name
			}
		]
	}

	S3_CLIENT.put_bucket_policy(Bucket=bucket_name,
		Policy=json.dumps(policy_payload))

def make_str_unique(original_str):
	unique_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
	return f"{original_str}-{unique_str}"

__all__ = ['S3_RESOURCE', 'S3_CLIENT', 'get_buckets', 'make_str_unique']
