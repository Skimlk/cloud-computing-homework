from aws_helpers import EC2_RESOURCE
import boto3
import time

# Creating New Key Pair
outfile = open('../.env/ec2keypair.pem','w')
key_pair = EC2_RESOURCE.create_key_pair(KeyName='ec2keypair')
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
outfile.close()

# Creating New Security Group
print("Creating New Security Group...")
mysg = EC2_RESOURCE.create_security_group(
	GroupName='http&ssh',
	Description='security group allowing http, ssh and ping')
mysg.authorize_ingress(
	IpPermissions=[
		{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
		'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
		{'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
		'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
		{'IpProtocol': 'icmp', 'FromPort': 8, 'ToPort': -1,
		'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
	])
print('security group is created')

# Launching New EC2 Instance
print("Launching New EC2 Instance...")
instances = EC2_RESOURCE.create_instances(
	ImageId='ami-0e68dc81dc36750a1',
	MinCount=1,
	MaxCount=1,
	InstanceType='t2.micro',
	KeyName='ec2keypair',
	SecurityGroups=['http&ssh'],
	BlockDeviceMappings=[{"DeviceName": "/dev/xvda",
		"Ebs" : { "VolumeSize" : 10 }}]
)

# Creating Tag
print("Creating Tag...")
i = instances[0]
print('instance', i.id, 'is created')
i.wait_until_running()
print('instance', i.id, 'is running')

EC2_RESOURCE.meta.client.create_tags(Resources=[i.id],
	Tags=[{'Key':'Name', 'Value':'Linux Server'}])

# Creating EBS Volume
print("Creating EBS Volume...")
subnet = EC2_RESOURCE.Subnet(i.subnet_id)
zone = subnet.availability_zone

volume = EC2_RESOURCE.create_volume(
	AvailabilityZone = zone,
	Size=20)
while EC2_RESOURCE.Volume(volume.id).state != 'available':
	time.sleep(5)

# Attach EBS Volume to Instance
print("Attaching EBS Volume to Instance...")
volume_id = volume.id
instance_id = i.id
dev = "/dev/sdh"

EC2_RESOURCE.Volume(volume_id).attach_to_instance(
	InstanceId = instance_id,
	Device = dev)

# List All EBS Volumes
print("Listing All EBS Volumes...")
volumes = EC2_RESOURCE.volumes.all()
for v in volumes:
	print(v.volume_id + ' ' +
		str(v.size) + ' ' +
		v.availability_zone)

# List All EIP Addresses
print("Listing All EIP Addresses...")
addresses = EC2_RESOURCE.vpc_addresses.all()
for a in addresses:
	print(a.allocation_id + ' ' + a.public_ip)

# Allocate and Associate EIP
print("Allocating and Associating EIP...")
eip = EC2_RESOURCE.meta.client.allocate_address()
allocation_id = eip["AllocationId"]
vpc_address = EC2_RESOURCE.VpcAddress(allocation_id)
vpc_address.associate(InstanceId = instance_id)
print(vpc_address.public_ip)
