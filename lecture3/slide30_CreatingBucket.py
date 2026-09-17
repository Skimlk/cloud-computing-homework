from aws_helpers import S3, make_str_unique
import boto3

# Creating a bucket called fdubucket
S3.create_bucket(Bucket=make_str_unique('fdubucket'))

# Creating a bucket constrained to us-east-2 called 'fdubuckettest'
location = {'LocationConstraint': 'us-east-2'}
S3.create_bucket(Bucket=make_str_unique('fdubuckettest'), 
	CreateBucketConfiguration=location)
