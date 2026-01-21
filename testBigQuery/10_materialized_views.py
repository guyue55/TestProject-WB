from google.cloud import bigquery
from google.cloud.exceptions import NotFound

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
# 这里的 app_logs 是我们在 Phase 2 脚本 06 中创建的
BASE_TABLE_ID = f"{DATASET_ID}.app_logs"
MV_ID = f"{DATASET_ID}.daily_log_summary"

client = bigquery.Client(project=PROJECT_ID)


def create_materialized_view():
    """
    创建物化视图 (Materialized View)。
    MV 类似于普通视图，但它会预先计算并缓存结果，且在新数据到达时自动递增更新。
    非常适合用于聚合查询 (SUM, COUNT) 的加速。
    """
    print(f"--- 1. 创建物化视图: {MV_ID} ---")

    # 注意: MV 的 SQL 必须是标准的聚合查询，且尽量简单
    query = f"""
        CREATE MATERIALIZED VIEW `{MV_ID}`
        OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
        AS 
        SELECT
            date(event_timestamp) as log_date,
            event_type,
            COUNT(*) as event_count
        FROM `{BASE_TABLE_ID}`
        GROUP BY 1, 2
    """

    try:
        # 使用 DDL 创建
        query_job = client.query(query)
        query_job.result()
        print("物化视图创建成功！")
    except Exception as e:
        print(f"创建 MV 时遇到警告或错误: {e}")


def query_tuning_demonstration():
    """
    演示 'Smart Tuning' (智能重写)。
    即使我们查询的是原始表 (app_logs)，BigQuery 也会智能地重定向到 MV 以节省成本。
    """
    print("\n--- 2. 演示智能查询重写 ---")

    # 这是一个针对 *原始表* 的查询
    sql = f"""
        SELECT
            date(event_timestamp) as log_date,
            event_type,
            COUNT(*) as event_count
        FROM `{BASE_TABLE_ID}` 
        WHERE date(event_timestamp) = CURRENT_DATE()
        GROUP BY 1, 2
    """

    # 使用 Dry Run 来查看优化效果
    job_config = bigquery.QueryJobConfig(dry_run=True)
    query_job = client.query(sql, job_config=job_config)

    # 在实际执行计划中，如果有 'Optimized with Materialized View' 之类的信息，说明命中
    # 大多数情况下，bytes_processed 会显著变小
    print(f"查询原始表预计扫描字节: {query_job.total_bytes_processed}")

    print("\n如果是全表扫描 app_logs，字节数会更多。")
    print("由于命中了 MV (或 BigQuery 评估 MV 更优)，扫描量通常非常小。")


if __name__ == "__main__":
    # 需要先保证 base task 06 运行过
    try:
        client.get_table(BASE_TABLE_ID)
        create_materialized_view()
        query_tuning_demonstration()
    except NotFound:
        print(
            f"错误: 基础表 {BASE_TABLE_ID} 不存在。请先运行 06_partitioning_clustering.py"
        )
