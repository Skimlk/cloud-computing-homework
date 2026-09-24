from aws_helpers import EC2_RESOURCE
import boto3

filters = [
	{
		'Name': 'tag:Name',
		'Values': ['debian-1']
	}
]

for i in EC2_RESOURCE.instances.filter(Filters=filters):
	print(i.id)
