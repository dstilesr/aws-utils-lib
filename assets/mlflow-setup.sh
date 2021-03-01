#!/bin/bash

# Install Python
yum update -y
yum install -y python3 \
  && pip3 install -U pip

# Install MLFlow
pip3 install --no-cache-dir mlflow boto3
