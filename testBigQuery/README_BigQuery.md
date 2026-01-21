# 🚀 BigQuery 实战学习指南

欢迎来到 BigQuery 学习之旅！本文档是一份 **"从入门到精通"** 的实战手册，涵盖了 13 个精心设计的 Python 脚本，带你系统掌握 BigQuery 的核心能力。

> **💡 使用指南**: 建议按顺序阅读和运行脚本。在 VS Code 中，按住 `Cmd/Ctrl` 点击蓝色的文件名即可直接跳转到源码。

---

## 🚀 快速开始与认证 (Quick Start & Auth)

在运行任何代码之前，必须解决**身份认证**问题。新手最常遇到的错误是 `403 Permission Denied`。

### 1. 本地开发认证 (Local Auth)
Google Cloud 推荐使用 **Application Default Credentials (ADC)**。在终端运行：

```bash
gcloud auth application-default login
```
这会打开浏览器登录你的 Google 账号，并在本地生成一个凭证文件。Python 代码会自动读取它，无需硬编码 Key。

### 2. 必备权限 (IAM)
你的账号（或 Service Account）至少需要以下权限：
*   `BigQuery User`: 运行查询 (Job User)。
*   `BigQuery Data Editor`: 创建/修改 Dataset 和 Table。

### 3. 理解区域 (Location) ⚠️
**非常重要**：BigQuery 资源是分区域的（如 `US`, `EU`, `asia-northeast1`）。
*   **铁律**: 位于 `US` 的表无法与位于 `EU` 的表进行 JOIN。
*   **代码习惯**: 在创建 Dataset 时显式指定 `location`。本教程默认使用 `US`。

---

## 📚 知识图谱 (Table of Contents)

### Phase 1: 基础建设 (Essentials)
1. **[进阶查询 (Advanced Query)](01_advanced_query.py)** - *安全第一：如何防止 SQL 注入？*
2. **[资源管理 (Manage Resources)](02_manage_resources.py)** - *告别手动：如何用代码管理表结构？*
3. **[数据写入 (Data Ingestion)](03_data_ingestion.py)** - *数据上云：流式插入 vs 批量加载*
4. **[成本控制 (Cost Estimation)](04_cost_estimation.py)** - *省钱指南：如何在运行前预知费用？*

### Phase 2: 性能与优化 (Optimization)
5. **[Schema 演进 (Schema Evolution)](05_schema_evolution.py)** - *拥抱变化：业务变更了，表结构怎么改？*
6. **[性能优化 (Partitioning & Clustering)](06_partitioning_clustering.py)** - *提速降本：如何让查询快 10 倍且省钱？*
7. **[复杂数据 (Nested & Repeated Data)](07_nested_repeated_data.py)** - *NoSQL 能力：如何处理数组和嵌套结构？*

### Phase 3: 高级应用 (Advanced Analytics)
8. **[机器学习 (BigQuery ML)](08_bigquery_ml.py)** - *SQL 即模型：不懂 Python 也能训练 AI？*
9. **[自定义函数 (UDFs)](09_user_defined_functions.py)** - *无限扩展：标准 SQL 不够用怎么办？*
10. **[物化视图 (Materialized Views)](10_materialized_views.py)** - *实时加速：如何实现零维护的实时报表？*

### Phase 4: 自动化 (Automation)
11. **[脚本编程 (Scripting)](11_scripting_loops.py)** - *图灵完备：在 SQL 里写循环和变量*
12. **[存储过程 (Stored Procedures)](12_stored_procedures.py)** - *逻辑封装：如何构建可复用的 ETL？*
13. **[定时任务 (Scheduled Queries)](13_scheduled_queries.py)** - *全自动：每天早上 8 点自动跑报表*

---

## 🔍 详细说明

### 1. 进阶查询与安全性 (Parameterized Queries)
*   **痛点**: 直接拼接字符串写 SQL (`"SELECT * FROM users WHERE name = '" + input + "'"`) 极易导致 SQL 注入攻击，且无法复用查询缓存。
*   **解决方案**: 使用 **参数化查询** (`@parameter`)。BigQuery 会自动处理转义，既安全又高效。
*   **源码**: [01_advanced_query.py](./01_advanced_query.py)

### 2. 资源管理 (Infrastructure as Code)
*   **痛点**: 在控制台手动建表容易点错，且在测试/生产环境难以保证一致性。
*   **解决方案**: 使用代码（IoC）来定义 Schema。确保 `created_at` 是 `TIMESTAMP` 而不是 `STRING`，从源头规范数据。
*   **源码**: [02_manage_resources.py](./02_manage_resources.py)

### 3. 数据写入 (Data Ingestion)
*   **场景**: 
    *   **流式插入 (Streaming)**: 实时性要求高（秒级可见），如网站点击日志。但需付费。
    *   **批量加载 (Load Job)**: 周期性数据同步（如每日对账），完全免费，吞吐量极大。
*   **源码**: [03_data_ingestion.py](./03_data_ingestion.py)

### 4. 成本控制 (Cost Estimation)
*   **痛点**: 写了一个 `SELECT *` 扫描了 10TB 数据，第二天收到几千美元账单。
*   **解决方案**: 
    1.  **Dry Run (预运行)**: 免费获取查询将扫描的字节数，心中有数再执行。
    2.  **Maximum Bytes Billed**: 设置“熔断器”，超过预算直接报错不执行。
*   **源码**: [04_cost_estimation.py](./04_cost_estimation.py)

### 5. Schema 演进 (Schema Evolution)
*   **痛点**: 业务发展快，表结构经常变（比如新增 `phone` 字段），删表重建数据会丢。
*   **解决方案**: 使用 API 动态添加列 (`NULLABLE` 模式)。
*   **Pro Tip**: 更新前重新 `get_table()` 避免版本冲突 (412 Error)。
*   **源码**: [05_schema_evolution.py](./05_schema_evolution.py)

### 6. 性能优化 (Partitioning & Clustering)
这是 BigQuery 最重要的优化手段，**必学！**
*   **分区 (Partitioning)**: 把大表切成“面包片”（按两切）。查询 `WHERE date='2023-01-01'` 时，还没碰数据就过滤掉了 99% 的无关文件。
*   **分簇 (Clustering)**: 在切片里再进行排序整理。查询 `WHERE user_id=1001` 时，直接定位到那个块，进一步减少扫描。
*   **源码**: [06_partitioning_clustering.py](./06_partitioning_clustering.py)

### 7. 复杂数据结构 (Nested & Repeated Data)
*   **痛点**: 电商订单（Order）和商品（Items）是一对多关系。传统数据库需要两张表 Join，慢且复杂。
*   **解决方案**: BigQuery 支持 **数组 (ARRAY)** 和 **结构体 (STRUCT)**。把 Items 直接嵌套在 Order 也就是一行里。读取时不需要 Join，性能极快。
*   **关键技**: `UNNEST()` 操作符，把数组“炸开”成行。
*   **源码**: [07_nested_repeated_data.py](./07_nested_repeated_data.py)

### 8. 机器学习 (BigQuery ML)
*   **痛点**: 数据在数据库，模型训练在 Python/Spark。数据搬运即费时又不安全。
*   **解决方案**: **数据不动，代码动**。直接用 SQL (`CREATE MODEL`) 训练模型。
*   **能力**: 回归、分类、聚类 (K-Means)、推荐系统、甚至调用 TensorFlow 模型。
*   **源码**: [08_bigquery_ml.py](./08_bigquery_ml.py)

### 9. 自定义函数 (UDFs)
*   **痛点**: 想要从 `User-Agent` 中提取浏览器版本，或者解密一段数据，标准 SQL 函数做不到。
*   **解决方案**: 编写 **JavaScript UDF**。利用 JS 强大的生态（正则、逻辑判断）来扩展 SQL 能力。
*   **源码**: [09_user_defined_functions.py](./09_user_defined_functions.py)

### 10. 物化视图 (Materialized Views)
*   **痛点**: Dashboard 每分钟刷新一次，每次都扫描 100 亿行日志计算 `COUNT(*)`，慢且贵。
*   **解决方案**: 建立 MV。BigQuery 自动维护一份预计算好的结果。
*   **黑科技**: **Smart Tuning**。你不需要改业务代码，继续查原始大表，BigQuery 会自动把查询“偷偷”重定向到 MV，瞬间返回结果。
*   **源码**: [10_materialized_views.py](./10_materialized_views.py)

### 11. 脚本编程 (Scripting)
*   **痛点**: 只能写单条 SQL，无法做复杂逻辑判断（如“如果今天是周末则跳过”）。
*   **解决方案**: BigQuery Scripting，让 SQL 像 Python 一样支持 `DECLARE` 变量, `IF/ELSE` 分支, `WHILE` 循环。
*   **源码**: [11_scripting_loops.py](./11_scripting_loops.py)

### 12. 存储过程 (Stored Procedures)
*   **痛点**: 每天的数据清理逻辑写了一堆 SQL，每次都要复制粘贴运行。
*   **解决方案**: 封装成 `PROCEDURE`。以后只需要执行 `CALL cleanup_logs(7)`，代码复用性 Max。
*   **源码**: [12_stored_procedures.py](./12_stored_procedures.py)

### 13. 定时任务 (Scheduled Queries)
*   **痛点**: 每天手动运行脚本太累，用 Crontab 管理又不稳定。
*   **解决方案**: 使用 GCP 原生的 Data Transfer Service。全托管，支持失败重试和邮件报警。
*   **源码**: [13_scheduled_queries.py](./13_scheduled_queries.py)

---

## 🛡️ 上线前检查清单 (Pre-flight Checklist)

在将你的代码推向生产环境前，请核对以下几点：

1.  [ ] **拒绝 `SELECT *`**: 永远只查询需要的列。除了省钱，也能减少传输延迟。
2.  [ ] **必须分区 (Partitioning)**: 只要表可能超过 1GB，就必须按时间（如 `created_at`）分区。
3.  [ ] **设置 `maximum_bytes_billed`**: 为每个查询设置预算熔断，防止意外的天价账单。
4.  [ ] **不要使用 `LIMIT` 省钱**: `LIMIT` 只是减少了返回的行数，**不会**减少扫描的字节数（也就是不会省钱）。要省钱必须用 `WHERE` 分区列。
5.  [ ] **优先使用 `Load Job`**: 尽量避免使用 `INSERT VALUES` (Streaming)，除非你真的需要秒级实时性。Load Job 既免费又快。

---

## 🛠 环境准备

请确保安装了以下依赖：

```bash
pip install -r requirements.txt
```
