from aws_helpers import S3_CLIENT, get_buckets()
import fnmatch
import boto3

# Enabling Object ACL
for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket_name = bucket.name
		break

S3_CLIENT.put_bucket_ownership_controls(
	Bucket=bucket_name,
	OwnershipControls={
		'Rules': [{'ObjectOwnership' : 'BucketOwnerPreferred'}]
	}
)
