PROJECT_ID=$(gcloud config get-value project) # 自动获取当前项目 ID
REGION="europe-west1"

# 构建镜像
gcloud builds submit --tag gcr.io/${PROJECT_ID}/helloworld:v1 . --region=${REGION}

# 查看 Artifact Registry 仓库
gcloud artifacts repositories list