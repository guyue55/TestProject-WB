#!/bin/bash

PROJECT_ID=$(gcloud config get-value project)
LOCATION=us-central1
SERVICE_NAME="${SERVICE_NAME:-storycraft-service-test}"

# 允许所有用户调用该服务
gcloud run services add-iam-policy-binding ${SERVICE_NAME} --member=allUsers --role=roles/run.invoker --region=${LOCATION} --project=${PROJECT_ID}
