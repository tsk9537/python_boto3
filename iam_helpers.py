import json
import boto3
from botocore.exceptions import ClientError


def create_user(iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Create user
    response = iam.create_user(UserName=iam_user_name)

    print(response)

    return response


def list_users():
    # Create IAM client
    iam = boto3.client('iam')

    # List users with the pagination interface
    paginator = iam.get_paginator('list_users')

    for response in paginator.paginate():
        print(response)


def update_user(iam_user_name, new_iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Update a user name
    iam.update_user(UserName=iam_user_name, NewUserName=new_iam_user_name)


def delete_user(iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Delete a user
    iam.delete_user(UserName=iam_user_name)


def create_policy(policy_name):
    # Create IAM client
    iam = boto3.client('iam')

    # EXAMPLE - Create a policy
    my_managed_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "logs:CreateLogGroup",
                "Resource": "RESOURCE_ARN"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DeleteItem",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:Scan",
                    "dynamodb:UpdateItem"
                ],
                "Resource": "RESOURCE_ARN"
            }
        ]
    }

    response = iam.create_policy(PolicyName=policy_name, PolicyDocument=json.dumps(my_managed_policy))

    print(response)

    return response


def get_iam_policy(poilcy_arn):
    #
    # EXAMPLE policy_arn: arn:aws:iam::aws:policy/AWSLambdaExecute
    #
    # Create IAM client
    iam = boto3.client('iam')

    # Get a policy
    response = iam.get_policy(PolicyArn=poilcy_arn)

    print(response['Policy'])

    return response['Policy']


def attach_managed_role_to_policy(policy_arn, role_name):
    #
    # EXAMPLE policy_arn: arn:aws:iam::aws:policy/AWSLambdaExecute
    #
    # EXAMPLE role_name: AmazonDynamoDBFullAccess
    # Create IAM client
    iam = boto3.client('iam')

    # Attach a role policy
    iam.attach_role_policy(PolicyArn=policy_arn, RoleName=role_name)


def detach_managed_role_from_policy(policy_arn, role_name):
    #
    # EXAMPLE policy_arn: arn:aws:iam::aws:policy/AWSLambdaExecute
    #
    # EXAMPLE role_name: AmazonDynamoDBFullAccess
    # Create IAM client
    iam = boto3.client('iam')

    # Detach a role policy
    iam.detach_role_policy(PolicyArn=policy_arn, RoleName=role_name)


def create_access_key(iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Create an access key
    response = iam.create_access_key(UserName=iam_user_name)

    print(response['AccessKey'])

    return response['AccessKey']


def list_users_access_keys(iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # List access keys through the pagination interface.
    paginator = iam.get_paginator('list_access_keys')

    for response in paginator.paginate(UserName=iam_user_name):
        print(response)


def get_last_used_access_key(access_key_id):
    # Create IAM client
    iam = boto3.client('iam')

    # Get last use of access key
    response = iam.get_access_key_last_used(AccessKeyId=access_key_id)

    print(response['AccessKeyLastUsed'])

    return response['AccessKeyLastUsed']


def update_access_key_status(access_key_id, status, iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Update access key to be active
    iam.update_access_key(AccessKeyId=access_key_id, Status=status, UserName=iam_user_name)


def delete_access_key(access_key_id, iam_user_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Delete access key
    iam.delete_access_key(AccessKeyId=access_key_id, UserName=iam_user_name)


def list_server_certificates():
    # Create IAM client
    iam = boto3.client('iam')

    # List server certificates through the pagination interface
    paginator = iam.get_paginator('list_server_certificates')

    for response in paginator.paginate():
        print(response['ServerCertificateMetadataList'])


def get_server_certificate(certificate_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Get the server certificate
    response = iam.get_server_certificate(ServerCertificateName=certificate_name)

    print(response['ServerCertificate'])

    return response['ServerCertificate']


def update_server_certificate(certificate_name, new_certificate_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Update the name of the server certificate
    iam.update_server_certificate(ServerCertificateName=certificate_name, NewServerCertificateName=new_certificate_name)


def delete_server_certificate(certificate_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Delete the server certificate
    iam.delete_server_certificate(ServerCertificateName=certificate_name)


def create_account_alias(alias_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Create an account alias
    iam.create_account_alias(AccountAlias=alias_name)


def list_account_aliases():
    # Create IAM client
    iam = boto3.client('iam')

    # List account aliases through the pagination interface
    paginator = iam.get_paginator('list_account_aliases')

    for response in paginator.paginate():
        print(response['AccountAliases'])


def delete_account_alias(alias_name):
    # Create IAM client
    iam = boto3.client('iam')

    # Delete an account alias
    iam.delete_account_alias(AccountAlias=alias_name)