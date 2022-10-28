#!/usr/bin/env python3

import argparse
import boto3
import os
import random
import sys
from botocore.config import Config

def init_boto3(region): 
    config = Config(region_name = region)
    client = boto3.client('ec2', config=config)

    return client

def get_instances(client, name=False, instance_id=False):
    if name:
        response = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [name]}])
    if instance_id: 
        response = client.describe_instances(InstanceIds=[instance_id])

    return response

def get_instance_public_dns(instance_response):
    instances = {}
    all_instances = []
    oldest = 0
    newest = 0

    for r in instance_response['Reservations']:
        for instance in r['Instances']:
            public_dns = instance['PublicDnsName']
            launch_time_epoch = int(instance['LaunchTime'].timestamp())
            all_instances.append(public_dns)

            if launch_time_epoch < oldest or oldest == 0:
                oldest = launch_time_epoch
                instances['oldest'] = public_dns
            
            if launch_time_epoch > newest  or newest == 0:
                newest = launch_time_epoch
                instances['newest'] = public_dns

            instances['random'] = random.choice(all_instances)

    return instances

def return_error(error, code = 1):
       print(str(error))
       sys.exit(code)

def main():
    parser = argparse.ArgumentParser(description='A helpful too for SSH\'ing into EC2 instances')

    parser.add_argument('--name', '-n', default=False, help='Shared name tag between instances')
    parser.add_argument('--instance', '-i', default=False, help='Instance ID')

    parser.add_argument('--user', '-u', default=False, help='SSH User')
    parser.add_argument('--region', '-g', default='us-east-1', help='EC2 Region (default: us-east-1)')

    parser.add_argument('--random', '-r', action='store_true', help='Connect to a random instance in a cluster')
    parser.add_argument('--oldest', '-o', action='store_true', help='Connect to the oldest instance in a cluster')
    parser.add_argument('--newest', '-e', action='store_true', help='Connect to the newest instance in a cluster')

    args = parser.parse_args()

    if args.name and args.instance:
        return_error('Error: You may not use both name (-n) and instance (-i) at the same time.', 2)

    boto3_client = init_boto3(args.region)
    raw_instances = get_instances(boto3_client, args.name, args.instance)

    if len(raw_instances['Reservations']) == 0:
        return_error('No instances found!')

    if not args.user:
        ssh_user_string = ''
    else:
        ssh_user_sring = args.user + '@'
    
    instances = get_instance_public_dns(raw_instances)

    if args.random or (not args.random and not args.oldest and not args.newest):
        os.system('ssh ' + ssh_user_sring + instances['random'])
    elif args.oldest:
        os.system('ssh ' + ssh_user_sring + instances['oldest'])
    elif args.newest:
        os.system('ssh ' + ssh_user_sring + instances['newest'])


if __name__ == "__main__":
    main()
