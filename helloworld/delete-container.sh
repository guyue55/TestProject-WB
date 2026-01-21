PROJECT_ID=$(gcloud config get-value project) # 自动获取当前项目 ID
REGION="europe-west1"

CONTAINER_NAME="helloworld"

gcloud run services list --region $REGION
gcloud run services describe $CONTAINER_NAME --region $REGION

gcloud run services delete $CONTAINER_NAME --region $REGION
