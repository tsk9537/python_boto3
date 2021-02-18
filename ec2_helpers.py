import boto3
from botocore.exceptions import ClientError


def get_ec2_description():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    print(response)

    return response


def toggle_ec2_monitoring(instance_id, toggle='ON'):
    ec2 = boto3.client('ec2')
    if toggle == 'ON':
        response = ec2.monitor_instances(InstanceIds=[instance_id])
    else:
        response = ec2.unmonitor_instances(InstanceIds=[instance_id])

    print(response)


def toggle_ec2_instance(instance_id, action='ON'):
    ec2 = boto3.client('ec2')

    if action == 'ON':
        # Do a dryrun first to verify permissions
        try:
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
    else:
        # Do a dryrun first to verify permissions
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)


def reboot_instance(instance_id):
    ec2 = boto3.client('ec2')

    try:
        ec2.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise

    try:
        response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)


def describe_ec2_key_pairs():
    ec2 = boto3.client('ec2')
    response = ec2.describe_key_pairs()
    print(response)


def create_ec2_key_pair(key_pair_name):
    ec2 = boto3.client('ec2')
    response = ec2.create_key_pair(KeyName=key_pair_name)
    print(response)


def delete_ec2_key_pair(key_pair_name):
    ec2 = boto3.client('ec2')
    response = ec2.delete_key_pair(KeyName=key_pair_name)
    print(response)


def describe_ec2_regions():
    ec2 = boto3.client('ec2')

    # Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_regions()
    print('Regions:', response['Regions'])


def describe_ec2_availability_zones():
    ec2 = boto3.client('ec2')

    # Retrieves availability zones only for region of the ec2 object
    response = ec2.describe_availability_zones()
    print('Availability Zones:', response['AvailabilityZones'])


def describe_security_groups(security_group_id):
    ec2 = boto3.client('ec2')

    try:
        response = ec2.describe_security_groups(GroupIds=[security_group_id])
        print(response)
        return response
    except ClientError as e:
        print(e)


def create_security_groups(security_group_name, description):
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=security_group_name,
                                            Description=description,
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print(f'Security Group Created {security_group_id} in vpc {vpc_id}.')

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print(f'Ingress Successfully Set {data}')
    except ClientError as e:
        print(e)


def delete_security_group(security_group_id):
    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Delete security group
    try:
        response = ec2.delete_security_group(GroupId=security_group_id)
        print(f'Security Group with ID: {security_group_id} Deleted')
    except ClientError as e:
        print(e)


def describe_elastic_ip_addresses():
    ec2 = boto3.client('ec2')

    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ]

    response = ec2.describe_addresses(Filters=filters)

    print(response)

    return response


def allocate_address(allocation_id, instance_id):
    ec2 = boto3.client('ec2')

    try:
        allocation = ec2.allocate_address(Domain='vpc')
        response = ec2.associate_address(AllocationId=allocation[allocation_id],
                                        InstanceId=instance_id)
        print(response)

        return response
    except ClientError as e:
        print(e)


def release_elastic_ip_address(allocation_id):
    ec2 = boto3.client('ec2')

    try:
        response = ec2.release_address(AllocationId=allocation_id)
        print(f'Elastic IP Address with ID: {allocation_id} released')
    except ClientError as e:
        print(e)


