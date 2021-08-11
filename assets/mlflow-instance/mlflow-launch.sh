#!/bin/bash

#################################################
# Script to launch MLFlow server
#################################################

mlflow server \
  --backend-store-uri /mnt/mlflow/params-metrics \
  --port 5000 \
  --host 0.0.0.0 \