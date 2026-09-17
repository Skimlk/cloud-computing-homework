from aws_helpers import S3_CLIENT, get_buckets
import fnmatch
import boto3
import json

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket_name = bucket.name
		break

policy_payload = {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "MakeItPublic",
			"Effect": "Allow",
			"Principal": "*",
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::%s/*" % bucket_name
		}
	]
}

S3_CLIENT.put_bucket_policy(Bucket=bucket_name,
	Policy=json.dumps(policy_payload))
