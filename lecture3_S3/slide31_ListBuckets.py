from aws_helpers import get_buckets
import boto3
import fnmatch

# List the contents of fdubucket
for bucket in get_buckets():
	print(bucket.name)
