from aws_helpers import EC2_RESOURCE
import boto3

for i in EC2_RESOURCE.instances.all():
	print("Instance Id " + i.id + ", " +
		"Instance AMI " + i.image_id + ", " +
		"Instance type " + i.instance_type + ", " +
		"Instance state " + i.state['Name'])
