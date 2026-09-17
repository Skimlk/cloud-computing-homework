from aws_helpers import get_buckets
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket.upload_file(Filename=r'./static/index.html',
			Key='index.html',
			ExtraArgs={'ContentType': "text/html", 'ACL': "public-read"})
		
		bucket.upload_file(Filename=r'./static/carpictures/car1.jpg',
			Key='car1.jpg',
			ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"})
		
		break
