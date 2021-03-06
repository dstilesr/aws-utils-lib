# Data Science Utils Lib

## Contents
- [About](#about)
- [Repository Contents](#repository-contents)
- [Launching a Stack](#launching-a-stack)

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


[Back to top.](#data-science-utils-lib)
