from aws_helpers import get_buckets
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket.download_file('car1.jpg', './static/carpictures/car1-downloaded.jpg')
		break
