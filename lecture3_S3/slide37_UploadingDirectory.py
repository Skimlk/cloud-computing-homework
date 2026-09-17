from aws_helpers import get_buckets
import os
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		directory = './static/carpictures'
		filelist = os.listdir(directory)
		for file in filelist:
			bucket.upload_file(Filename=f"{directory}/{file}", Key=file)
			print(f"'{directory}/{file}', is uploaded")
		break
