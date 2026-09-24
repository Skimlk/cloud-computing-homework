from aws_helpers import EC2_RESOURCE
import boto3

filters = [
	{
		'Name': 'instance-state-name',
		'Values': ['running']
	}
]

for i in EC2_RESOURCE.instances.filter(Filters=filters):
	print(i.id)
