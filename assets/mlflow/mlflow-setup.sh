#!/bin/bash

# Install nginx
yum update -y
amazon-linux-extras install nginx1 -y

# Install Python, mlflow
yum install -y python3 \
  && pip3 install -U pip mlflow boto3

# Make tracking URL
mkdir -p /mnt/mlflow/params-metrics
chmod -R a+rwx /mnt/mlflow
