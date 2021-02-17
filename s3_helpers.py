import requests
import logging
import json
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_existing_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_fileobj(file_name):
    s3 = boto3.client('s3')
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, "BUCKET_NAME", "OBJECT_NAME")


def download_file(file_name):
    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', file_name)


def download_fileobj(file_name):
    s3 = boto3.client('s3')
    with open(file_name, 'wb') as f:
        s3.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)


def upload_multipart_file(file_name):
    # Set the desired multipart threshold value (5GB)
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5*GB)

    # Perform the transfer
    s3 = boto3.client('s3')
    s3.upload_file(file_name, 'BUCKET_NAME', 'OBJECT_NAME', Config=config)


def concurrent_download_file(file_name):
    # To consume less downstream bandwidth, decrease the maximum concurrency
    config = TransferConfig(max_concurrency=5)

    # Download an S3 object
    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', file_name, Config=config)


def threaded_download_file(file_name):
    # Disable thread use/transfer concurrency
    config = TransferConfig(use_threads=True)

    s3 = boto3.client('s3')
    s3.download_file('BUCKET_NAME', 'OBJECT_NAME', file_name, Config=config)


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def download_file_from_presigned_url(url):
    if url is not None:
        response = requests.get(url)


def create_presigned_url_expanded(client_method_name, method_parameters=None,
                                  expiration=3600, http_method=None):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(ClientMethod=client_method_name,
                                                    Params=method_parameters,
                                                    ExpiresIn=expiration,
                                                    HttpMethod=http_method)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def upload_file_with_presigned_url(response, object_name):
    if response is None:
        exit(1)

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)

    # If successful, returns HTTP status code 204
    logging.info(f'File upload HTTP status code: {http_response.status_code}')


def get_bucket_policy(bucket_name):
    # Retrieve the policy of the specified bucket
    s3 = boto3.client('s3')
    result = s3.get_bucket_policy(Bucket=bucket_name)
    print(result['Policy'])

    return result['Policy']


def set_bucket_policy(bucket_name):
    # Create a bucket policy
    bucket_name = bucket_name
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }]
    }

    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy
    s3 = boto3.client('s3')
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)


def delete_bucket_policy(bucket_name):
    # Delete a bucket's policy
    s3 = boto3.client('s3')
    s3.delete_bucket_policy(Bucket=bucket_name)


def get_bucket_acl(bucket_name):
    # Retrieve a bucket's ACL
    s3 = boto3.client('s3')
    result = s3.get_bucket_acl(Bucket=bucket_name)
    print(result)

    return result


def get_website_configuration(bucket_name):
    # Retrieve the website configuration
    s3 = boto3.client('s3')
    result = s3.get_bucket_website(Bucket=bucket_name)

    return result


def delete_website_configuration(bucket_name):
    # Delete the website configuration
    s3 = boto3.client('s3')
    s3.delete_bucket_website(Bucket=bucket_name)


def get_bucket_cors(bucket_name):
    """Retrieve the CORS configuration rules of an Amazon S3 bucket

    :param bucket_name: string
    :return: List of the bucket's CORS configuration rules. If no CORS
    configuration exists, return empty list. If error, return None.
    """

    # Retrieve the CORS configuration
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_cors(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
            return []
        else:
            # AllAccessDisabled error == bucket not found
            logging.error(e)
            return None
    return response['CORSRules']


def set_bucket_cors(bucket_name):
    # Define the configuration rules
    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['Authorization'],
            'AllowedMethods': ['GET', 'PUT'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['GET', 'PUT'],
            'MaxAgeSeconds': 3000
        }]
    }

    # Set the CORS configuration
    s3 = boto3.client('s3')
    s3.put_bucket_cors(Bucket=bucket_name,
                    CORSConfiguration=cors_configuration)


def get_client_from_vpc():
    s3_client = boto3.client(
        service_name='s3',
        endpoint_url='https://bucket.vpce-abc123-abcdefgh.s3.us-east-1.vpce.amazonaws.com'
    )

    return s3_client


def get_client_from_accesspoint():
    s3_client = boto3.client(
        service_name='s3',
        endpoint_url='https://accesspoint.vpce-abc123-abcdefgh.s3.us-east-1.vpce.amazonaws.com'
    )

    return s3_client


def get_control_client_from_vpc():
    control_client = boto3.client(
        service_name='s3control',
        endpoint_url='https://control.vpce-abc123-abcdefgh.s3.us-east-1.vpce.amazonaws.com'
    )

    return control_client
