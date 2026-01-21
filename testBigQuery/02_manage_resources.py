from google.cloud import bigquery
from google.cloud.exceptions import NotFound, Conflict

PROJECT_ID = "webeye-internal-test"
client = bigquery.Client(project=PROJECT_ID)

# 定义我们要创建的 Dataset ID 和 Table ID
DATASET_ID = f"{PROJECT_ID}.learning_bq"
TABLE_ID = f"{DATASET_ID}.users"

def create_dataset():
    """创建 Dataset"""
    try:
        # 先检查是否存在
        client.get_dataset(DATASET_ID)
        print(f"Dataset {DATASET_ID} 已经存在。")
    except NotFound:
        # 不存在则创建
        dataset = bigquery.Dataset(DATASET_ID)
        # 💡 关键设置: 显式指定 location (如 'US', 'asia-northeast1')。
        # 不同 location 的数据无法 JOIN。如果不指定，默认为 US，但建议要在代码中显式写明。
        dataset.location = "US" 
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"成功创建 Dataset: {dataset.dataset_id}")

def create_table_with_schema():
    """创建一个带有明确 Schema 的 Table"""
    
    # 1. 定义 Schema
    # 💡 最佳实践: 相比于让 BigQuery 自动推断 (autodetect)，生产环境强力推荐明确指定 Schema。
    # 这能避免数据类型错误（比如把 '001' 识别成整数 1），并作为文档存在。
    schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED", description="用户ID"),
        bigquery.SchemaField("username", "STRING", mode="REQUIRED", description="用户名"),
        bigquery.SchemaField("email", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("tags", "STRING", mode="REPEATED", description="用户标签(数组)"),
    ]

    table = bigquery.Table(TABLE_ID, schema=schema)

    try:
        table = client.create_table(table)
        print(f"成功创建表: {table.full_table_id}")
    except Conflict:
        print(f"表 {TABLE_ID} 已经存在。")

if __name__ == "__main__":
    create_dataset()
    create_table_with_schema()
