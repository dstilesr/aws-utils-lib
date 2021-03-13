#!/bin/bash

#################################################
# Script for initial setup of the library.
# You must create the bucket to store the assets
# and stacks BEFORE setup!
#################################################

# Setup directory to store metadata with .env file for bucket name
export DS_DIR_NAME=~/.ds-utils-data
if [ ! -d $DS_DIR_NAME ]; then
  echo "Making metadata directory $DS_DIR_NAME"
  mkdir -p $DS_DIR_NAME
  echo "Bucker Name: $1"
  echo "export ASSETS_BUCKET_NAME=$1" > $DS_DIR_NAME/.env
fi

# Read variables
source $DS_DIR_NAME/.env

# Sync local stacks and assets files with bucket
echo "Syncing stacks to s3://$ASSETS_BUCKET_NAME..."
aws s3 sync ./aws-stacks/ s3://$ASSETS_BUCKET_NAME/aws-stacks/

echo "Syncing assets to s3://$ASSETS_BUCKET_NAME..."
aws s3 sync ./assets/ s3://$ASSETS_BUCKET_NAME/assets/
