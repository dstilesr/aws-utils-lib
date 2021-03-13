#!/bin/bash

#################################################
# Bootstrap script for MLFlow instance (Ubuntu)
#################################################

# Install nginx
apt-get update \
  && apt upgrade -y \
  && apt install -y nginx jq

# Install Python, mlflow
apt install -y python3-pip \
  && pip3 install -U pip mlflow boto3

# Make tracking URL
mkdir -p /mnt/mlflow/params-metrics \
  && chmod -R a+rwx /mnt/mlflow

# Start nginx
systemctl start nginx

#################################################
# Get assets from bucket

# Bucket name from parameter
export ASSETS_BUCKET=$(aws ssm get-parameter --name=/mlflow/assets-bucket-name-ssm | jq -r .Parameter.Value)
export MLFLOW_ASSETS_DIR=/home/ubuntu/mlflow

# Copy assets
aws s3 cp s3://$ASSETS_BUCKET/assets/mlflow-instance $MLFLOW_ASSETS_DIR --recursive

#################################################
# Setup nginx server
# Here we assume the mlflow assets are stored in /home/ubuntu/mlflow/
# At a later stage one might store them in an S3 bucket and download them

# Link config file
cp $MLFLOW_ASSETS_DIR/mlflow_server.conf /etc/nginx/sites-available/mlflow_server.conf
unlink /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/mlflow_server.conf /etc/nginx/sites-enabled/mlflow_server.conf

# Restart nginx
systemctl restart nginx

#################################################
# Setup MLFlow daemon

# Change permissions of launch file to allow execution
chmod 005 $MLFLOW_ASSETS_DIR/mlflow-launch.sh

# Add service to systemd and start mlflow as daemon
cp $MLFLOW_ASSETS_DIR/mlflow-server.service /etc/systemd/system/mlflow-server.service \
  && systemctl daemon-reload \
  && systemctl enable mlflow-server \
  && systemctl start mlflow-server
