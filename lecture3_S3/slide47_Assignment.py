import os
import sys
import fnmatch
from aws_helpers import get_buckets, S3_RESOURCE, make_str_unique
from botocore.exceptions import ClientError

def print_usage(argv):
	print(f"Usage: {argv[0]} [BUCKET] [LOCAL DIRECTORY]")	
	print(f"If no bucket matches input, '{argv[0]}' will try to create it using a unique string.")

def is_directory(path):
	try:
		file_mode = os.stat(path).st_mode
		if stat.S_ISDIR(file_mode):
			return True
		else:
			print(f"'{path}' exists but is not a directory.")
	except FileNotFoundError:
		print(f"'{path}' does not exist.")

	return False

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
		if bucket.name is bucket_specified:
			print(f"Found bucket '{bucket_name}'")
			return bucket.name

	bucket_name = try_create_bucket(bucket_specified)
	if bucket_name is not None:
		return bucket_name

	while(bucket_name is None):
		bucket_name = try_create_bucket(make_str_unique(bucket_specified))

	return bucket_name

def main(argv, argc):
	if argc != 3:
		print_usage(argv)
		return 1

	if not is_directory(argv[2]):
		print_usage(argv)
		return 1

	bucket_specified = argv[1].lower()
	local_directory = argv[2]

	bucket_name = get_bucket_name(bucket_specified)
	bucket = S3_RESOURCE.Bucket(bucket_name)

	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv, len(sys.argv)))
