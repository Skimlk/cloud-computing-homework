from aws_helpers import S3_CLIENT, get_buckets
import fnmatch
import boto3

# Enabling Public Access
for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket_name = bucket.name
		break

S3_CLIENT.put_public_access_block(
	Bucket=bucket_name,
	PublicAccessBlockConfiguration={
		'BlockPublicAcls': False,
		'IgnorePublicAcls': False,
		'BlockPublicPolicy': False,
		'RestrictPublicBuckets': False
	}
)
