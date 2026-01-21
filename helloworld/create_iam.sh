SA_NAME="ai-app-v3"
PROJECT_ID=$(gcloud config get-value project)
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 1. 创建 Service Account
gcloud iam service-accounts create ${SA_NAME} --display-name="${SA_NAME}"

# 2. 授予您（部署者）扮演新 SA 的权限 (roles/iam.serviceAccountUser)
DEPLOYER_IDENTITY=$(gcloud config get-value account)
gcloud iam service-accounts add-iam-policy-binding ${SA_EMAIL} \
    --member="user:${DEPLOYER_IDENTITY}" \
    --role="roles/iam.serviceAccountUser"

# 3. 授予新 SA 运行时的权限 (Vertex AI User)
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/aiplatform.user"

# 4. 授予新 SA 运行时的权限 (Cloud Run Admin)
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/run.admin"

echo "创建的 SA 邮箱地址是: ${SA_EMAIL}"