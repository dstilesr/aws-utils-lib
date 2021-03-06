# Data Science Utils Lib

## Contents
- [About](#about)
- [Repository Contents](#repository-contents)
- [Launching a Stack](#launching-a-stack)
  - [Launch MLFlow Instance](#launch-mlflow-instance)
  - [Note on MLFlow Startup](#note-on-mlflow-startup)

## About
This repo contains several utilities for Data Science and ML Engineering work. I made
this both for personal use and for practice using AWS.

## Repository Contents
The `aws-stacks` directory contains several CloudFormation stacks as `.yml` files.
The idea is to have stacks for everyday tasks such as training an ML model, or setting
up a logging / tracking server.

The `assets` directory contains bootstrap scripts and configuration files that may be used
with the stacks.

## Launching a Stack
To launch a stack from the AWS CLI, use the following command:
```shell
aws cloudformation create-stack --stack-name <name> --template-body=file://<path-to-file> --capabilities CAPABILITY_NAMED_IAM
```
Use the name of the `.yml` file as the name of the stack, and include additional stack parameters 
with the `--parameters ParameterKey=parameter,ParameterValue=value` syntax, or via a JSON file.

### Launch MLFlow Instance
In order to launch an mlflow instance, do the following:
- First, create the instance with the `mlflow-instance` stack.
- Then, copy the mlflow assets to the instance with
```shell
scp -i <key-file> -r assets/mlflow/ ubuntu@<instance-ip>:~/mlflow/
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
