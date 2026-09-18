import os
import sys
import stat
import fnmatch
from pathlib import Path
from aws_helpers import get_buckets, S3_RESOURCE, make_str_unique, enable_public_bucket_access
from botocore.exceptions import ClientError

def print_usage(argv):
	print(f"Usage: {argv[0]} [BUCKET] [LOCAL DIRECTORY]")	
	print(f"If no bucket matches input, '{argv[0]}' will try to create it using a unique string.")

def try_create_bucket(bucket_name):
	try:
		S3_RESOURCE.create_bucket(Bucket=bucket_name)
		print(f"Created bucket named '{bucket_name}'")
		return bucket_name
	except ClientError as e:
		print(f"Could not create bucket '{bucket_name}': {e}")

	return None

def get_bucket_name(bucket_specified):
	for bucket in get_buckets():
		if bucket.name == bucket_specified:
			print(f"Found bucket '{bucket.name}'")
			return bucket.name

	bucket_name = try_create_bucket(bucket_specified)
	if bucket_name is not None:
		return bucket_name

	while(bucket_name is None):
		bucket_name = try_create_bucket(make_str_unique(bucket_specified))

	return bucket_name

def upload_directory(bucket, local_path, cloud_parent=None):
	local_path = Path(local_path)

	if cloud_parent is None:
		cloud_parent = local_path.name 
   
	for entry in local_path.iterdir():
		cloud_path = f"{cloud_parent}/{entry.name}" 

		if entry.is_dir():
			upload_directory(bucket, entry, cloud_path)
		else:
			bucket.upload_file(Filename=str(entry.resolve()), Key=cloud_path)
			print(f"Uploaded '{cloud_path}'")

def main(argv, argc):
	if argc != 3:
		print_usage(argv)
		return 1

	bucket_specified = argv[1].lower()
	directory = Path(os.path.expanduser(argv[2]))

	if not directory.is_dir():
		return 1

	bucket_name = get_bucket_name(bucket_specified)
	bucket = S3_RESOURCE.Bucket(bucket_name)
	enable_public_bucket_access(bucket_name)
	
	upload_directory(bucket, directory)

if __name__ == '__main__':
    sys.exit(main(sys.argv, len(sys.argv)))
