from google.cloud import bigquery_datatransfer
from google.protobuf import timestamp_pb2
import time

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
# 如果我们想运行刚刚定义的存储过程
QUERY_STRING = f"CALL `{DATASET_ID}.cleanup_old_logs`(30);"

def create_scheduled_query():
    """
    创建定时查询 (Scheduled Query)。
    使用 Data Transfer Service API。
    """
    print("--- 创建定时查询任务 ---")
    
    # 注意: 初始化的是 DataTransferServiceClient，不是 BigQuery Client
    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    # 1. 定义 Parent (Project Location)
    # 必须指定 Location，例如 projects/{project_id}/locations/{location}
    parent = transfer_client.common_project_path(PROJECT_ID)
    
    # 2. 配置传输任务
    transfer_config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id="learning_bq",
        display_name="Daily Log Cleanup (Demo)",
        data_source_id="scheduled_query",
        params={
            "query": QUERY_STRING
        },
        schedule="every 24 hours", # 设置调度频率
        disabled=True, # 为了防止演示产生垃圾任务，我们默认禁用它
    )

    try:
        response = transfer_client.create_transfer_config(
            parent=parent,
            transfer_config=transfer_config
        )
        print(f"定时查询已创建: {response.name}")
        print("状态: 已禁用 (Disabled) -- 避免意外运行")
        print(f"调度: {response.schedule}")
        print(f"查询语句: {response.params['query']}")
    except Exception as e:
        print(f"创建失败: {e}")
        print("常见原因:")
        print("1. ⚠️ 需要启用 Billing (Data Transfer Service 是付费服务，虽然有免费额度)。")
        print("2. 权限不足: Service Account 需要 'BigQuery Data Transfer Agent' 角色。")

if __name__ == "__main__":
    create_scheduled_query()
