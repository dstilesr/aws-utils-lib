#!/bin/bash

#################################################
# Bootstrap script for MLFlow instance (Ubuntu)
#################################################

# Make tracking URL
mkdir -p /mnt/mlflow/params-metrics \
  && chmod -R a+rwx /mnt/mlflow

# Start nginx
systemctl start nginx

#################################################
# Get assets from bucket

export MLFLOW_ASSETS_DIR=/home/ubuntu/mlflow

# Copy assets
aws s3 cp s3://$ASSETS_BUCKET/assets/mlflow-instance $MLFLOW_ASSETS_DIR/ --recursive

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

# Set artifact root to S3 Bucket in launch file
echo "--default-artifact-root $MLFLOW_BUCKET" >> $MLFLOW_ASSETS_DIR/mlflow-launch.sh

# Change permissions of launch file to allow execution
chmod 005 $MLFLOW_ASSETS_DIR/mlflow-launch.sh

# Add service to systemd and start mlflow as daemon
cp $MLFLOW_ASSETS_DIR/mlflow-server.service /etc/systemd/system/mlflow-server.service \
  && systemctl daemon-reload \
  && systemctl enable mlflow-server \
  && systemctl start mlflow-server
