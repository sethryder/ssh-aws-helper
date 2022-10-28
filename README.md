# ssh-aws-helper
Helpful tool for SSH'ing into EC2 instances.

## What, Why?

When looking around I found some existing tools for helping you SSH into EC2 instances. But they all required the use of the SSM agent. 

I wanted a simple tool that used native SSH and helped me target instances to log in to.

## Setup

### Requirments
* Python 3.6+
* Boto3

```
pip install -r requirements.txt
```

### AWS Config
`ssh-aws-helper` uses boto3 to get the list of instances from you account. So you will need a config setup with your keys.

By default this is in `~/.aws/credentials`

```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXX
```

You will also most likely want to setup a default region in the `~/.aws/config`. This will save you from having set the region everytime you run `ssh-aws-helper`.
```
[default]
region = us-east-1
```

### Symlink

For ease of use I would recommend setting up a symlink from wherever you clone this repo to.

For example:
```
ln -s /home/seth/dev/ssh-aws-helper/sshelper.py /usr/local/bin/sshelper
```

## Usage
```
usage: sshelper.py [-h] [--name NAME] [--instance INSTANCE] [--user USER]
                   [--region REGION] [--random] [--oldest] [--newest]

A helpful too for SSH'ing into EC2 instances

optional arguments:
  -h, --help                            Show this help message and exit
  --name NAME, -n NAME                  Shared name tag between instances
  --instance INSTANCE, -i INSTANCE      Instance ID
  --user USER, -u USER                  SSH User
  --region REGION, -g REGION            EC2 Region (default: us-east-1)
  --random, -r (default)                Connect to a random instance in a cluster
  --oldest, -o                          Connect to the oldest instance in a cluster
  --newest, -e                          Connect to the newest instance in a cluster
```

## Examples

Connect to the newest instance with name tag `api`

```
sshelper -n api -e
```

Connect to a specific instance id with the `seth` user
```
sshelper -i i-1234567890abcdef0 -u seth
```

