#!/usr/bin/env bash
# set -euo pipefail

SA_NAME="test-api-sheet-gcp"
PROJECT_ID=$(gcloud config get-value project)
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 1. 创建 Service Account
gcloud iam service-accounts create ${SA_NAME} --display-name="${SA_NAME}"

# 3. 在组织级别授予：项目创建者权限
gcloud organizations add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/resourcemanager.projectCreator"

# 4. 在组织级别授予：结算账号用户权限
gcloud organizations add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/billing.user"

# 5. 在组织级别授予：项目 IAM 管理员权限 (用于给销售授权)
gcloud organizations add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/resourcemanager.projectIamAdmin"

echo "创建的 SA 邮箱地址是: ${SA_EMAIL}"