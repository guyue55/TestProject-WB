# TestProject

一个用于验证和测试 Google Cloud Platform (GCP) 相关功能的综合性项目集合。

## 📋 项目简介

本项目包含多个子项目，用于学习、测试和验证 GCP 的各项服务和功能，主要聚焦于：

- **BigQuery**: 数据仓库和分析
- **Cloud Build & Cloud Run**: 容器化部署
- **GCloud CLI**: 命令行工具和脚本

## 🗂️ 项目结构

```
TestProject/
├── testBigQuery/          # BigQuery 完整学习教程（13个实战脚本）
│   ├── 01_advanced_query.py
│   ├── 02_manage_resources.py
│   ├── 03_data_ingestion.py
│   ├── 04_cost_estimation.py
│   ├── 05_schema_evolution.py
│   ├── 06_partitioning_clustering.py
│   ├── 07_nested_repeated_data.py
│   ├── 08_bigquery_ml.py
│   ├── 09_user_defined_functions.py
│   ├── 10_materialized_views.py
│   ├── 11_scripting_loops.py
│   ├── 12_stored_procedures.py
│   ├── 13_scheduled_queries.py
│   └── README_BigQuery.md  # 详细的 BigQuery 学习指南
│
├── helloworld/            # Cloud Run 部署示例
│   ├── main.py           # Flask 应用
│   ├── Dockerfile        # 容器镜像配置
│   ├── build.sh          # 构建脚本
│   ├── deploy.sh         # 部署脚本
│   └── requirements.txt  # Python 依赖
│
└── scripts-gcloud/        # GCloud CLI 实用脚本
    ├── glcoud 常用命令.md
    ├── create_iam-sheet.sh
    ├── del-projects.sh
    └── ...

```

## 🚀 快速开始

### 前置要求

1. **Google Cloud SDK**
   ```bash
   # macOS
   brew install --cask google-cloud-sdk

   # 或下载安装包
   # https://cloud.google.com/sdk/docs/install
   ```

2. **Python 3.8+**
   ```bash
   python --version
   ```

3. **认证配置**
   ```bash
   # 登录 Google Cloud
   gcloud auth login

   # 设置默认项目
   gcloud config set project YOUR_PROJECT_ID

   # 配置应用默认凭证（用于 BigQuery 等 API）
   gcloud auth application-default login
   ```

### 安装依赖

```bash
# 安装 Python 依赖（根据子项目需要）
cd testBigQuery
pip install -r ../helloworld/requirements.txt

# 或使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 子项目详细说明

### 1. BigQuery 学习教程 (`testBigQuery/`)

完整的 BigQuery 从入门到精通实战教程，包含 13 个渐进式脚本：

**Phase 1: 基础建设**
- 安全查询（参数化）
- 资源管理（表/数据集）
- 数据导入（流式/批量）
- 成本预估

**Phase 2: 性能优化**
- Schema 动态演进
- 分区和分簇优化
- 嵌套和数组数据

**Phase 3: 高级应用**
- BigQuery ML（SQL 训练模型）
- 自定义函数（UDF）
- 物化视图

**Phase 4: 自动化**
- 脚本编程
- 存储过程
- 定时任务

👉 详细学习路径请查看：[testBigQuery/README_BigQuery.md](./testBigQuery/README_BigQuery.md)

### 2. Cloud Run 示例 (`helloworld/`)

演示如何将 Python Flask 应用容器化并部署到 Cloud Run：

```bash
cd helloworld

# 构建镜像
./build.sh

# 部署到 Cloud Run
./deploy.sh

# 连接到运行中的容器（调试）
./connect-container.sh
```

**关键文件：**
- `main.py`: Flask 应用入口
- `Dockerfile`: 多阶段构建配置
- `cloudbuild.yaml-tmp`: Cloud Build CI/CD 配置模板
- `create_iam.sh`: IAM 权限配置脚本

### 3. GCloud 实用脚本 (`scripts-gcloud/`)

常用的 GCloud CLI 操作脚本和命令速查：

- `glcoud 常用命令.md`: 命令速查手册
- `create_iam-sheet.sh`: 批量创建服务账号
- `del-projects.sh`: 批量删除项目（测试环境清理）
- `tail_build_log.sh`: 实时查看构建日志

## ⚙️ 配置说明

### GCP 项目设置

```bash
# 查看当前配置
gcloud config list

# 设置项目
gcloud config set project YOUR_PROJECT_ID

# 设置默认区域
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

### BigQuery 区域配置

⚠️ **重要**: BigQuery 数据集有区域限制，不同区域的表无法 JOIN。

建议在代码中显式指定：
```python
from google.cloud import bigquery

client = bigquery.Client()
dataset = bigquery.Dataset("my_project.my_dataset")
dataset.location = "US"  # 或 "EU", "asia-northeast1"
```

## 🛡️ 最佳实践

### 成本控制
1. ✅ 使用 `dry_run` 预估查询成本
2. ✅ 设置 `maximum_bytes_billed` 防止意外账单
3. ✅ 优先使用批量加载（Load Job）而非流式插入
4. ✅ 为大表启用分区和分簇

### 安全性
1. ✅ 使用参数化查询防止 SQL 注入
2. ✅ 不要在代码中硬编码凭证
3. ✅ 使用服务账号并遵循最小权限原则
4. ✅ 定期轮换密钥

### 开发规范
1. ✅ 使用 Infrastructure as Code 管理资源
2. ✅ 在 `.gitignore` 中排除敏感文件
3. ✅ 使用环境变量区分开发/测试/生产环境

## 🔧 故障排查

### 常见错误

**1. `403 Permission Denied`**
```bash
# 重新登录并授权
gcloud auth application-default login

# 检查 IAM 权限
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:YOUR_EMAIL"
```

**2. `404 Not Found: Dataset/Table`**
- 检查项目 ID 是否正确
- 确认资源的区域（location）
- 验证数据集/表名拼写

**3. BigQuery 区域错误**
```
Cannot query over table from multiple locations
```
解决：确保所有表都在同一区域，或创建数据集时指定 `location`

**4. Docker 构建失败**
```bash
# 清理缓存重新构建
docker system prune -a
docker build --no-cache -t my-image .
```

## 📖 参考资源

- [BigQuery 官方文档](https://cloud.google.com/bigquery/docs)
- [Cloud Run 文档](https://cloud.google.com/run/docs)
- [GCloud CLI 参考](https://cloud.google.com/sdk/gcloud/reference)
- [Python Client for BigQuery](https://googleapis.dev/python/bigquery/latest/index.html)

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

详见：[CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件

## ✨ 致谢

感谢 Google Cloud Platform 提供的强大云服务和详尽文档。

---

**最后更新**: 2026-01-21
**维护者**: [@apple](https://github.com/apple)
