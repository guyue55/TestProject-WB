#!/usr/bin/env bash
set -euo pipefail

# Cloud Run 管理/排查脚本
# 用途：
# - 列出指定区域内的服务
# - 获取某服务的公开访问 URL
# - 查看服务的修订版本（revisions）
# - 实时拉取服务日志，便于排查问题
#
# 先决条件：
# - 已通过 `gcloud auth login` 完成认证
# - 已设置项目与区域，例如：
#   `gcloud config set project YOUR_PROJECT_ID`
#   `gcloud config set run/region europe-west1`
# - 注意：Cloud Run（托管）不支持 `instances exec` 进入容器
#
# 使用：
#   SERVICE=helloworld REGION=europe-west1 bash helloworld/connect-container.sh
# 不传环境变量时使用下列默认值。

SERVICE="${SERVICE:-helloworld}"
REGION="${REGION:-europe-west1}"

# # 列出当前区域的 Cloud Run 服务
# gcloud run services list --region "$REGION"

# # 获取服务公开 URL
URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')"
echo "$URL"

# # 查看服务的修订版本（每次部署会生成一个 revision）
# gcloud run revisions list --service "$SERVICE" --region "$REGION"

# 实时查看服务日志（默认最近 200 条，提升 verbosity 便于排查）
gcloud beta run services logs tail "$SERVICE" --region "$REGION" --verbosity=info
# 查看服务日志（默认最近 200 条，提升 verbosity 便于排查）
# gcloud beta run services logs read "$SERVICE" --region "$REGION" --verbosity=info --limit=200
