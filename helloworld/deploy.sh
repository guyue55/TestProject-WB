PROJECT_ID=$(gcloud config get-value project) # 自动获取当前项目 ID

# # 指定 Service Account 进行部署
SA_NAME="ai-app-v3"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 部署 Cloud Run 服务（默认使用 ADC）
# gcloud run deploy helloworld --source . --region europe-west1
# 构建镜像
gcloud builds submit --tag gcr.io/${PROJECT_ID}/helloworld:v3 . --region europe-west1


# # 获取您的部署身份（Cloud Shell 中 gcloud 登录的邮箱）
# DEPLOYER_IDENTITY=$(gcloud config get-value account)
# echo "您的部署身份是: ${DEPLOYER_IDENTITY}"
# # # # 为 Service Account 分配必要的角色（例如：Cloud Run 执行角色）
# # gcloud projects add-iam-policy-binding ${PROJECT_ID} \
# #     --member="user:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
# #     --role="roles/run.invoker"
# gcloud iam service-accounts add-iam-policy-binding ${SA_EMAIL} \
#     --member="user:${DEPLOYER_IDENTITY}" \
#     --role="roles/iam.serviceAccountUser"

# gcloud run deploy helloworld \
#     --source . \
#     --platform managed \
#     --region europe-west1 \
#     --service-account ${SA_EMAIL} \
#     --allow-unauthenticated

# # 部署 Cloud Run 服务（指定 Service Account）
# gcloud run deploy helloworld --source . --platform managed --region europe-west1 --service-account ${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --allow-unauthenticated

gcloud run deploy helloworld \
    --image gcr.io/${PROJECT_ID}/helloworld:v3 \
    --platform managed \
    --region europe-west1 \
    --service-account ${SA_EMAIL} \
    --allow-unauthenticated

# 验证绑定
gcloud run services describe helloworld --region europe-west1 --format='value(spec.template.spec.serviceAccountName)'