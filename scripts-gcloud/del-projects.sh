# 1. 先列出所有符合条件的项目 ID，确认一下是否都是要删除的
gcloud projects list --filter="projectId:test-auto-*" --format="value(projectId)"

# 2. 批量删除（慎用！请确保上一步列出的 ID 都是测试项目）
for project in $(gcloud projects list --filter="projectId:test-auto-*" --format="value(projectId)"); do
  echo "删除项目: $project"
  gcloud projects delete $project --quiet
#   gcloud projects delete $project
done

# 注：--quiet 参数可以跳过手动确认步骤，直接执行删除。