from aws_helpers import get_buckets
import boto3

# List all objects
for bucket in get_buckets():
	print(f"Bucket '{bucket.name}':")
	for obj in bucket.objects.all():
		print(f"\t{obj.key}")
