from aws_helpers import BUCKETS
import boto3
import fnmatch

# List the contents of fdubucket
for bucket in BUCKETS:
	print(bucket.name)
