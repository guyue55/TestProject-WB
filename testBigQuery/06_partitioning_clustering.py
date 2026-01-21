from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import datetime

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
# 我们将创建一个用来存储日志的新表
TABLE_ID = f"{DATASET_ID}.app_logs"

client = bigquery.Client(project=PROJECT_ID)

def create_partitioned_clustered_table():
    """
    创建一个既有分区(Partitioning)又有分簇(Clustering)的表。
    这是 BigQuery 性能优化的黄金组合。
    """
    print(f"--- 正在创建分区+分簇表: {TABLE_ID} ---")
    
    # 1. 定义 Schema
    schema = [
        bigquery.SchemaField("log_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("event_timestamp", "TIMESTAMP", mode="REQUIRED"), # 分区字段
        bigquery.SchemaField("user_id", "INTEGER", mode="NULLABLE"),           # 分簇字段
        bigquery.SchemaField("event_type", "STRING", mode="NULLABLE"),         # 分簇字段
        bigquery.SchemaField("message", "STRING", mode="NULLABLE"),
    ]

    table = bigquery.Table(TABLE_ID, schema=schema)

    # 2. 配置分区 (Partitioning)
    # 按天分区。查询时如果带上 WHERE date(event_timestamp) = ... 会极大减少扫描量
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="event_timestamp",  # 指定分区列
        expiration_ms=None,       # 数据永不过期 (可以设置例如 30天后自动删除)
    )

    # 3. 配置分簇 (Clustering)
    # 在同一个分区内，数据会根据这些字段排序。
    # 查询 WHERE user_id = 123 时，BigQuery 可以直接跳到相关的数据块，避免全分区扫描。
    table.clustering_fields = ["user_id", "event_type"]

    try:
        table = client.create_table(table)
        print(f"表创建成功: {table.full_table_id}")
        print(f"分区类型: {table.time_partitioning.type_}")
        print(f"分簇字段: {table.clustering_fields}")
    except Exception as e:
        print(f"表可能已存在或出错: {e}")

def insert_data_into_specific_partition():
    """演示插入数据"""
    print("\n--- 插入示例数据 ---")
    now = datetime.datetime.now()
    rows = [
        {"log_id": "L1", "event_timestamp": str(now), "user_id": 1001, "event_type": "login", "message": "User logged in"},
        {"log_id": "L2", "event_timestamp": str(now), "user_id": 1002, "event_type": "logout", "message": "User logged out"},
        # 故意插入一条昨天的数据 (会自动落入昨天的分区)
        {"log_id": "L3", "event_timestamp": str(now - datetime.timedelta(days=1)), "user_id": 1001, "event_type": "click", "message": "Late arriving data"},
    ]
    
    errors = client.insert_rows_json(TABLE_ID, rows)
    if not errors:
        print("数据插入成功！")
    else:
        print(f"插入错误: {errors}")

def query_optimized():
    """演示如何利用分区查询 (Pruning)"""
    print("\n--- 演示优化查询 ---")
    # 注意 WHERE 子句必须包含分区列，才能产生裁剪效果(Pruning)
    query = f"""
        SELECT *
        FROM `{TABLE_ID}`
        WHERE date(event_timestamp) = CURRENT_DATE() 
          AND user_id = 1001
    """
    
    # 💡 核心原理: Partition Pruning (分区裁剪)
    # BigQuery 看到 WHERE date(...) 条件后，会直接忽略掉昨天、前天等所有不匹配的分区文件。
    # 这就是为什么分区表能省钱的原因。如果没有这个 WHERE 条件，它会扫描全表！
    
    job_config = bigquery.QueryJobConfig(dry_run=True)
    query_job = client.query(query, job_config=job_config)
    print(f"此查询将扫描字节数: {query_job.total_bytes_processed} (如果表很大，这个数字会远小于全表扫描)")

if __name__ == "__main__":
    # 如果表已存在如果要重新演示，建议先去控制台删掉或者修改代码逻辑
    # client.delete_table(TABLE_ID, not_found_ok=True) 
    
    create_partitioned_clustered_table()
    insert_data_into_specific_partition()
    query_optimized()
