#!/bin/bash
# 先列出所有符合条件的项目 ID，确认一下是否都是要删除的
# gcloud projects list --filter="projectId:test-auto-*" --format="value(projectId)"

# 1. 在这里填入你想删除的项目 ID，用空格、换行或 Tab 分隔均可
PROJECTS=(
  "test-auto-gc-20251219-5433"
  "test-auto-gc-20251219-57688"
  "test-auto-gc-20251219-8830"
  "test-auto-gc-20251219-5766"
  "test-auto-gc-20251219-7551"
  "test-auto-20251218-4998"
)

echo "准备删除以下项目，共 ${#PROJECTS[@]} 个："
for id in "${PROJECTS[@]}"; do
  echo " - $id"
done

# 2. 安全确认
read -p "确定要删除以上所有项目吗？此操作不可逆（30天恢复期）。(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作已取消。"
    exit 1
fi

# 3. 循环执行删除
for pid in "${PROJECTS[@]}"; do
    echo "正在关停项目: $pid ..."
    # --quiet 参数可以跳过每条命令的手动确认 (y/n)
    # --async 参数表示发起请求后不等待删除完成，直接下一个，速度最快
    gcloud projects delete "$pid" --quiet --async
    # gcloud projects delete "$pid" 
    
    if [ $? -eq 0 ]; then
        echo "✅ 项目 $pid 已提交删除申请。"
    else
        echo "❌ 项目 $pid 删除失败，请检查 ID 是否正确或权限是否足够。"
    fi
done

echo "------------------------------------------------"
echo "所有任务已处理完毕。"