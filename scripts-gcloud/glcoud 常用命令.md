当然！我已经为您准备了一份涵盖日常配置、管理计算资源和部署应用等方面最常用的 `gcloud` 命令清单。

---

##⚡ gcloud 日常常用命令清单###1. 基础配置与认证 (`gcloud auth` & `gcloud config`)这是您开始使用 `gcloud` 或切换工作环境时最常用的命令。

| 命令 | 用途 | 示例 |
| --- | --- | --- |
| `gcloud init` | **初始化向导。** 交互式设置认证、选择项目和默认区域。 | `gcloud init` |
| `gcloud auth login` | **登录/认证。** 通过浏览器登录 Google 账号。 | `gcloud auth login` |
| `gcloud config list` | **查看当前配置。** 显示当前激活的项目 ID、用户、区域等。 | `gcloud config list` |
| `gcloud config set project` | **设置默认项目。** 设定接下来所有操作默认使用的项目。 | `gcloud config set project [PROJECT_ID]` |
| `gcloud config set compute/region` | **设置默认区域。** 设定 GCE、Cloud Run 等资源的默认部署区域。 | `gcloud config set compute/region us-central1` |
| `gcloud components update` | **更新 CLI 组件。** 确保所有 `gcloud` 工具和组件都是最新版本。 | `gcloud components update` |
| `gcloud help [COMMAND]` | **获取帮助。** 查看任何命令的详细用法、参数和示例。 | `gcloud compute instances create --help` |

###2. 计算资源管理 (Compute Engine - GCE)用于管理虚拟机 (VM) 实例、SSH 连接和防火墙规则。

| 命令 | 用途 | 示例 |
| --- | --- | --- |
| `gcloud compute instances list` | **列出 VM 实例。** 显示所有 VM 实例的名称、状态、区域等。 | `gcloud compute instances list` |
| `gcloud compute instances create` | **创建 VM。** 根据指定配置创建新的虚拟机实例。 | `gcloud compute instances create my-vm --machine-type e2-micro` |
| `gcloud compute ssh` | **SSH 连接。** 通过 SSH 快速连接到指定的 VM 实例。 | `gcloud compute ssh my-vm` |
| `gcloud compute instances stop` | **停止 VM。** 停止运行中的 VM 实例。 | `gcloud compute instances stop my-vm` |
| `gcloud compute instances delete` | **删除 VM。** 删除指定的虚拟机实例。 | `gcloud compute instances delete my-vm` |
| `gcloud compute firewall-rules list` | **列出防火墙规则。** 查看项目的防火墙规则列表。 | `gcloud compute firewall-rules list` |

###3. 无服务器应用部署 (Cloud Run)用于部署、更新和管理无服务器容器服务。

| 命令 | 用途 | 示例 |
| --- | --- | --- |
| `gcloud run deploy` | **部署/更新服务。** 部署新服务或更新现有服务。 | `gcloud run deploy my-app --source . --allow-unauthenticated` |
| `gcloud run services list` | **列出服务。** 查看所有已部署的 Cloud Run 服务。 | `gcloud run services list` |
| `gcloud run services delete` | **删除服务。** 删除指定的 Cloud Run 服务。 | `gcloud run services delete my-app` |
| `gcloud run services update-traffic` | **管理流量。** 拆分/迁移流量到不同的版本。 | `gcloud run services update-traffic my-app --to my-app-v2=50` |

###4. 存储管理 (Cloud Storage)用于管理 Cloud Storage 存储桶（Bucket）和文件对象。

| 命令 | 用途 | 示例 |
| --- | --- | --- |
| `gcloud storage buckets list` | **列出存储桶。** 查看项目中的所有存储桶。 | `gcloud storage buckets list` |
| `gcloud storage cp` | **复制文件。** 复制本地文件到存储桶或在存储桶之间复制。 | `gcloud storage cp ./image.jpg gs://my-bucket/` |
| `gcloud storage ls` | **列出对象。** 查看存储桶中的文件和文件夹。 | `gcloud storage ls gs://my-bucket/` |
| `gcloud storage rm` | **删除对象。** 删除存储桶中的文件。 | `gcloud storage rm gs://my-bucket/old-file.txt` |

###5. 身份与访问管理 (IAM)用于管理用户、服务账号和权限。

| 命令 | 用途 | 示例 |
| --- | --- | --- |
| `gcloud projects get-iam-policy` | **查看项目策略。** 显示项目的 IAM 策略（权限）。 | `gcloud projects get-iam-policy [PROJECT_ID]` |
| `gcloud iam service-accounts list` | **列出服务账号。** 查看项目中的所有服务账号。 | `gcloud iam service-accounts list` |

---

您想知道如何管理 **Google Kubernetes Engine (GKE)** 集群的命令，还是 **Cloud SQL**（托管数据库）的命令？请告诉我您的下一步需求！