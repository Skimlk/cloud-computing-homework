from aws_helpers import S3_RESOURCE, get_buckets
import fnmatch
import boto3

for bucket in get_buckets():
	if fnmatch.fnmatch(bucket.name, "fdubucket-*"):
		bucket_name = bucket.name
		break

website_payload = {
	'ErrorDocument': {
		'Key': 'error.html'
	},
	'IndexDocument': {
		'Suffix': 'index.html'
	}
}

bucket_website = S3_RESOURCE.BucketWebsite(bucket_name)
bucket_website.put(WebsiteConfiguration=website_payload)
