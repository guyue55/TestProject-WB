# 贡献指南

感谢你对 TestProject 的兴趣！我们欢迎各种形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)

## 行为准则

参与本项目即表示你同意遵守我们的行为准则：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 Issue 并包含以下信息：

- **清晰的标题**：简要描述问题
- **详细描述**：详细说明问题是什么
- **复现步骤**：列出重现问题的步骤
  1. 执行 '...'
  2. 点击 '...'
  3. 看到错误
- **期望行为**：描述你期望发生什么
- **实际行为**：描述实际发生了什么
- **截图**：如果适用，添加截图帮助解释问题
- **环境信息**：
  - OS: [e.g. macOS 14.0]
  - Python 版本: [e.g. 3.11.5]
  - GCloud SDK 版本: [e.g. 456.0.0]

### 建议新功能

如果你有新功能的想法：

1. 先检查 Issues 看是否已有人提出
2. 创建一个 Feature Request Issue
3. 清楚地描述功能和使用场景
4. 解释为什么这个功能对项目有价值

### 提交代码

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/TestProject.git
   cd TestProject
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **设置上游仓库**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/TestProject.git
   ```

5. **进行更改**
   - 编写代码
   - 添加测试
   - 更新文档

6. **保持同步**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

7. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

8. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **创建 Pull Request**
   - 在 GitHub 上打开 Pull Request
   - 填写 PR 模板
   - 等待代码审查

## 开发流程

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r helloworld/requirements.txt

# 配置 GCloud
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 运行测试

```bash
# 运行 BigQuery 测试脚本
cd testBigQuery
python 01_advanced_query.py

# 测试 Cloud Run 部署
cd helloworld
./build.sh
```

### 代码检查

```bash
# 格式化代码（推荐使用 black）
pip install black
black .

# 代码检查（推荐使用 ruff）
pip install ruff
ruff check .

# 类型检查（可选）
pip install mypy
mypy .
```

## 代码规范

### Python 代码风格

遵循 [PEP 8](https://pep8.org/) 规范：

- 使用 4 个空格缩进（不使用 Tab）
- 每行最多 88 个字符（Black 默认）
- 使用有意义的变量名
- 添加适当的注释和文档字符串

**示例：**

```python
def query_bigquery(client: bigquery.Client, query: str) -> List[Dict]:
    """
    执行 BigQuery 查询并返回结果。

    Args:
        client: BigQuery 客户端实例
        query: SQL 查询语句

    Returns:
        查询结果的列表，每个元素是一个字典

    Raises:
        google.api_core.exceptions.GoogleAPIError: 查询执行失败
    """
    job = client.query(query)
    results = job.result()
    return [dict(row) for row in results]
```

### Shell 脚本规范

- 使用 `#!/bin/bash` 作为第一行
- 使用 2 个空格缩进
- 添加错误处理 `set -euo pipefail`
- 添加注释说明脚本用途

**示例：**

```bash
#!/bin/bash
set -euo pipefail

# 构建 Docker 镜像并推送到 GCR
# 用法: ./build.sh [IMAGE_NAME]

IMAGE_NAME="${1:-my-app}"
PROJECT_ID=$(gcloud config get-value project)

echo "Building image: ${IMAGE_NAME}"
docker build -t "gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest" .
```

### 文档规范

- README 使用中文或英文，保持一致
- 代码注释使用中文（本项目）
- 使用 Markdown 格式
- 添加代码示例和截图

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构（既不是新功能也不是修复）
- `perf`: 性能优化
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动
- `ci`: CI/CD 配置文件和脚本的变动

### 示例

```bash
# 新功能
git commit -m "feat(bigquery): add materialized views example"

# Bug 修复
git commit -m "fix(cloudrun): correct Dockerfile path"

# 文档
git commit -m "docs: update README with setup instructions"

# 重构
git commit -m "refactor(scripts): simplify IAM creation logic"
```

## Pull Request 指南

### PR 标题

使用与 commit 相同的规范：

```
feat(bigquery): add cost estimation example
```

### PR 描述模板

```markdown
## 描述
简要描述此 PR 的目的和更改内容

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 测试
描述你如何测试这些更改

## 截图（如适用）
添加相关截图

## 检查清单
- [ ] 代码遵循项目的代码规范
- [ ] 我已经进行了自我审查
- [ ] 我已经添加了注释，特别是在难以理解的部分
- [ ] 我已经更新了相关文档
- [ ] 我的更改没有产生新的警告
- [ ] 我已经添加了测试来验证我的修复/功能
- [ ] 新旧测试都通过
```

## 审查流程

1. 提交 PR 后，维护者会进行审查
2. 可能会要求修改或提供更多信息
3. 所有讨论解决后，PR 会被合并
4. 合并后，你的贡献将出现在下一个版本中

## 获得帮助

如果你有任何问题：

- 查看现有的 [Issues](https://github.com/OWNER/TestProject/issues)
- 创建新的 Issue 提问
- 在 PR 中 @mention 维护者

## 许可

通过贡献代码，你同意你的贡献将在 MIT 许可证下授权。

---

再次感谢你的贡献！🎉
