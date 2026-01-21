# 安全策略

## 🔒 支持的版本

我们目前支持以下版本的安全更新：

| 版本 | 支持状态 |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## 🐛 报告安全漏洞

我们非常重视项目的安全性。如果你发现了安全漏洞，请负责任地向我们披露。

### 📧 如何报告

**请勿通过公开的 GitHub Issue 报告安全漏洞。**

请通过以下方式之一报告安全问题：

1. **优先选择**: 使用 GitHub 的私密安全漏洞报告功能
   - 进入仓库的 "Security" 标签页
   - 点击 "Report a vulnerability"
   - 填写漏洞详情

2. **邮件报告**: 发送邮件到 security@example.com（请替换为实际邮箱）
   - 主题格式：`[SECURITY] 简要描述`
   - 附上详细的漏洞信息

### 📝 报告应包含的信息

为了帮助我们更好地理解和修复问题，请在报告中包含以下信息：

- **漏洞类型**: 例如 SQL 注入、权限提升、信息泄露等
- **影响范围**: 哪些组件或功能受影响
- **复现步骤**: 详细的步骤说明
- **影响评估**: 漏洞可能造成的影响
- **概念验证**: 如果可能，提供 PoC 代码或截图
- **建议修复方案**: 如果你有修复建议（可选）
- **发现者信息**: 你的姓名/昵称（用于致谢，可选）

### ⏱️ 响应时间

我们承诺：

- **初步响应**: 在 **48 小时内**确认收到报告
- **问题评估**: 在 **7 天内**评估漏洞的严重性和影响范围
- **修复计划**: 在 **14 天内**提供修复计划或时间表
- **发布修复**: 根据严重性，在 **30-90 天内**发布安全补丁

### 🏆 致谢

我们感谢所有负责任地披露安全问题的研究人员。在你同意的情况下，我们将：

- 在 CHANGELOG 中公开致谢
- 在安全公告中提及你的贡献
- 在项目的 SECURITY.md 中列出你的名字

## 🔐 安全最佳实践

### 对于贡献者

如果你为本项目贡献代码，请遵循以下安全实践：

#### 1. 凭证和密钥管理

- ❌ **永远不要**将凭证、密钥或敏感信息提交到代码仓库
- ✅ 使用环境变量或 GCP Secret Manager 存储敏感信息
- ✅ 确保 `.gitignore` 包含 `.env`、`credentials.json` 等文件
- ✅ 使用 `gcloud auth application-default login` 而非硬编码凭证

**错误示例：**
```python
# ❌ 不要这样做
PROJECT_ID = "my-gcp-project"
API_KEY = "AIzaSyD-abcd1234567890"
```

**正确示例：**
```python
# ✅ 推荐做法
import os
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
# 使用 Application Default Credentials
from google.cloud import bigquery
client = bigquery.Client()  # 自动使用 ADC
```

#### 2. SQL 注入防护

- ✅ **始终**使用参数化查询
- ❌ **永远不要**使用字符串拼接构建 SQL 查询

**错误示例：**
```python
# ❌ 存在 SQL 注入风险
query = f"SELECT * FROM users WHERE name = '{user_input}'"
```

**正确示例：**
```python
# ✅ 使用参数化查询
from google.cloud.bigquery import ScalarQueryParameter
query = "SELECT * FROM users WHERE name = @name"
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        ScalarQueryParameter("name", "STRING", user_input)
    ]
)
```

#### 3. IAM 权限最小化

- ✅ 遵循**最小权限原则**
- ✅ 为不同环境使用不同的服务账号
- ✅ 定期审计和轮换服务账号密钥
- ❌ 避免使用 `roles/owner` 或 `roles/editor` 等过于宽泛的角色

**推荐权限：**
```bash
# BigQuery 用户（仅查询）
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/bigquery.user"

# BigQuery 数据编辑（创建表）
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/bigquery.dataEditor"
```

#### 4. 依赖安全

- ✅ 定期更新依赖包到最新稳定版本
- ✅ 使用 `pip-audit` 或 `safety` 扫描漏洞
- ✅ 在 CI/CD 中集成依赖安全检查

```bash
# 安装并运行安全扫描
pip install pip-audit
pip-audit
```

#### 5. 代码审查

- ✅ 所有代码必须经过至少一次审查
- ✅ 关注安全相关的代码变更（认证、授权、数据处理）
- ✅ 使用自动化工具（Ruff、Bandit）进行静态分析

### 对于用户

如果你使用本项目，请注意：

#### 1. 环境隔离

- ✅ 在测试环境中使用独立的 GCP 项目
- ✅ 不要在生产环境直接运行未经验证的脚本
- ✅ 使用 `--dry-run` 预览 BigQuery 查询的影响

#### 2. 成本控制

- ✅ 设置 BigQuery 查询的 `maximum_bytes_billed`
- ✅ 启用 GCP Billing Alerts
- ✅ 定期审查资源使用情况

```python
# 设置查询成本上限（1GB）
job_config = bigquery.QueryJobConfig()
job_config.maximum_bytes_billed = 1024 * 1024 * 1024
```

#### 3. 数据保护

- ✅ 使用 BigQuery 的列级加密和行级安全策略
- ✅ 定期备份重要数据
- ✅ 遵守 GDPR、CCPA 等数据保护法规

## 🚨 已知安全注意事项

### GCP 凭证泄露

**风险**: 如果 Application Default Credentials 被泄露，攻击者可能获得你的 GCP 资源访问权限。

**缓解措施**:
- 凭证文件通常位于 `~/.config/gcloud/application_default_credentials.json`
- 确保此文件权限设置为 `600` (仅所有者可读写)
- 不要将此文件提交到版本控制
- 定期轮换凭证

```bash
# 检查凭证文件权限
ls -l ~/.config/gcloud/application_default_credentials.json

# 如果权限不正确，修改为 600
chmod 600 ~/.config/gcloud/application_default_credentials.json
```

### BigQuery 数据泄露

**风险**: 错误的 IAM 配置可能导致敏感数据泄露。

**缓解措施**:
- 使用 `allAuthenticatedUsers` 或 `allUsers` 时要格外小心
- 启用 BigQuery Audit Logs 监控数据访问
- 对敏感列使用 Cloud DLP 进行脱敏

### Cloud Run 公开暴露

**风险**: Cloud Run 服务默认可能公开访问。

**缓解措施**:
```bash
# 部署时限制访问（仅允许认证用户）
gcloud run deploy SERVICE_NAME \
  --no-allow-unauthenticated \
  --region REGION
```

## 📚 安全资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [BigQuery Security and Identity Management](https://cloud.google.com/bigquery/docs/access-control)
- [CWE/SANS Top 25 Most Dangerous Software Errors](https://cwe.mitre.org/top25/)

## 📜 披露政策

我们遵循**协调披露**原则：

1. 安全研究人员私密报告漏洞
2. 我们确认并开发修复方案
3. 我们发布安全补丁
4. 在补丁发布 **30 天后**，我们和报告者可以公开披露详情

## 🔄 安全更新订阅

要接收安全更新通知：

- 在 GitHub 上 "Watch" 本仓库并选择 "Custom" -> "Security alerts"
- 关注项目的 Release 页面

---

**最后更新**: 2026-01-21

如有任何安全疑问，请联系：security@example.com（请替换为实际联系方式）
