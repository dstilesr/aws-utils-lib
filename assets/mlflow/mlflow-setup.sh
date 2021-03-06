#!/bin/bash

# Install nginx
apt-get update \
  && apt upgrade -y \
  && apt install -y nginx

# Install Python, mlflow
apt install -y python3-pip \
  && pip3 install -U pip mlflow boto3

# Make tracking URL
mkdir -p /mnt/mlflow/params-metrics \
  && chmod -R a+rwx /mnt/mlflow
