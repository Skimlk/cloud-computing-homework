from aws_helpers import get_buckets
import boto3
import fnmatch

# List the contents of fdubucket
for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		for obj in bucket.objects.all():
			print(obj.key)
