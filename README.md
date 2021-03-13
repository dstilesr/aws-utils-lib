# Data Science Utils Lib

## Contents
- [About](#about)
- [Repository Contents](#repository-contents)
  - [Directories](#directories)
  - [Adding a New Stack](#adding-a-new-stack)
- [Setup](#setup)
  - [Sync Stacks to Bucket](#sync-stacks-to-bucket)
  - [Install Python Library](#install-python-library)
- [Launching a Stack](#launching-a-stack)
  - [Direct](#direct)
  - [With Python Library](#with-python-library)
  - [Launch MLFlow Instance](#launch-mlflow-instance)
  - [Note on MLFlow Startup](#note-on-mlflow-startup)

## About
This repo contains several utilities for Data Science and ML Engineering work. I made
this both for personal use and for practice using AWS.

## Repository Contents

### Directories
The `aws-stacks` directory contains several CloudFormation stacks as `.yml` files.
The idea is to have stacks for everyday tasks such as training an ML model, or setting
up a logging / tracking server.

The `assets` directory contains bootstrap scripts and configuration files that may be used
with the stacks. The assets associated with a given stack, say `my-stack.yml`, in aws-stacks
should be stored in a directory `assets/my-stack`, that is, with the same name as the stack.

### Adding a New Stack
In order to add a new stack, first create the CloudFormation `.yml` template and store it in
the `aws-stacks` directory. When making the template, take the following into account:
- If the templates uses a CIDR range of addresses to allow SSH access
  to an instance and / or the name of a key to gain SSH access, name these parameters `SSHAccessAddresses`
  and `KeyNameParameter`, respectively.
- If the templates uses assets that must be copied to the instance on startup (such as a bootstrap script),
  save these files in the `assets` folder under a subdirectory with the same name as the stack, as was
  said [above](#directories). Additionally, you should add a parameter `AssetsBucketName` to the stack
  (no default value) to pass the name of the assets bucket, and your instances should have permissions to
  read from this bucket.
  

## Setup

### Sync Stacks to Bucket
In order to set up the library for use, do the following:
- Create an S3 bucket to store the stacks and assets.
- Ensure you have the aws CLI installed.
- Run the `setup.sh` script with `bash setup.sh your-bucket-name`. This will create a
  `~/.ds-utils-data` directory to store metadata. Within it there will be a `.env` file
  with the bucket name. Additionally, it will sync your `aws-stacks` and `assets` directories
  to the bucket.

If you have already performed the initial setup and have added new stacks or assets, you can once
again run the `setup.sh` script with `bash setup.sh` to sync these to the bucket.

### Install Python Library
In order to install the python library to manage the stacks, first navigate to the `python-lib` directory
and then run the setup script with
```shell
python setup.py install
```

## Launching a Stack

### Direct
To launch a stack from the AWS CLI, use the following command:
```shell
aws cloudformation create-stack --stack-name <name> --template-body=file://<path-to-file> --capabilities CAPABILITY_NAMED_IAM
```
Use the name of the `.yml` file as the name of the stack, and include additional stack parameters 
with the `--parameters ParameterKey=parameter,ParameterValue=value` syntax, or via a JSON file.

### With Python Library
If you have installed the [python library](#install-python-library), you can launch a stack more easily
with
```shell
python -m ds_utils_lib.aws_utils launch --stack_name=a-stack-name
```
To add parameters, such as `KeyNameParameter`, for example, you can add them as flags. So for example to set this 
parameter you could run 
```shell
python -m ds_utils_lib.aws_utils launch --stack_name=a-stack-name --KeyNameParameter=a-key-name
```

Additionally, you can also delete a stack with the python library as follows:
```shell
python -m ds_utils_lib.aws_utils delete --stack_name=a-stack-name
```

### Launch MLFlow Instance
In order to launch an mlflow instance, do the following:
- First, create the instance with the `mlflow-instance` stack.
- Then, copy the mlflow assets to the instance with
```shell
scp -i <key-file> -r assets/mlflow-instance/ ubuntu@<instance-ip>:~/mlflow/
```
- Next, ssh into the instance:
```shell
ssh -i <key-file> ubuntu@<instance-ip>
```
- Finally, once logged in to the instance, run the bootstrap script:
```shell
sudo bash /home/ubuntu/mlflow/mlflow-bootstrap.sh
```

### Note on MLFlow Startup
This procedure is a bit clumsy, as this should all be done by simply running a bootstrap
script on instance startup, but this will be done in a later iteration. Ideally, one could 
store the `assets` directory in an S3 bucket and then copy the scripts from there during 
the instance startup.

[Back to top.](#data-science-utils-lib)
