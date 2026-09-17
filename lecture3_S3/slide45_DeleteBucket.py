from aws_helpers import S3_RESOURCE, get_buckets
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubuckettest-*"):
		bucket.objects.all().delete()
		bucket.delete()
		break
