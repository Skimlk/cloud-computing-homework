from aws_helpers import S3_RESOURCE, get_buckets
import os
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		# Create folder
		folder = 'carpictures/'
		bucket.put_object(Key=folder)

		# Upload file to folder
		bucket.upload_file(Filename=f"./static/carpictures/car2.jpg", 
			Key=folder+'car2.jpg')

		# List files in folder
		objects = bucket.objects.filter(Prefix=folder)
		for obj in objects:
			print(obj.key)

		# Delete folder
		for obj in objects:
			obj.delete()		

		break


