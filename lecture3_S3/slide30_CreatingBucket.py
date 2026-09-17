from aws_helpers import S3_RESOURCE, make_str_unique
import boto3

# Creating a bucket called fdubucket
S3_RESOURCE.create_bucket(Bucket=make_str_unique('fdubucket'))

# Creating a bucket constrained to us-east-2 called 'fdubuckettest'
location = {'LocationConstraint': 'us-east-2'}
S3_RESOURCE.create_bucket(Bucket=make_str_unique('fdubuckettest'), 
	CreateBucketConfiguration=location)
