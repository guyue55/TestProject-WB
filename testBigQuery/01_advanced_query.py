from google.cloud import bigquery

# 初始化客户端
# 替换为你的项目 ID
PROJECT_ID = "webeye-internal-test"
client = bigquery.Client(project=PROJECT_ID)


def run_parameterized_query(state_name, limit_count):
    """
    运行参数化查询。
    参数化查询可以防止 SQL 注入，并且允许 BigQuery 缓存查询计划，提高效率。
    """

    # 1. 定义 SQL，使用 @符号 定义参数占位符
    # 💡 最佳实践: 永远使用参数化查询，即使是内部系统。
    # 它可以防止 SQL 注入，并且 BigQuery 可以缓存编译后的查询计划，复用性更高。
    query = """
        SELECT name, SUM(number) as total_count
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = @state
        GROUP BY name
        ORDER BY total_count DESC
        LIMIT @limit
    """

    # 2. 配置查询参数
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            # 标量参数 (Scalar)
            bigquery.ScalarQueryParameter("state", "STRING", state_name),
            bigquery.ScalarQueryParameter("limit", "INT64", limit_count),
        ]
    )

    print(f"正在查询州: {state_name}, 限制: {limit_count}...")

    # 3. 运行查询 (带有配置)
    query_job = client.query(query, job_config=job_config)

    # 4. 获取结果 (使用 Storage API 加速，因为我们刚才安装了依赖)
    # 💡 性能提示: to_dataframe() 默认尝试使用 BigQuery Storage API (二进制协议)。
    # 相比传统的 JSON REST API，下载大结果集时速度快非常多。
    # 现在的 to_dataframe 会自动尝试使用 google-cloud-bigquery-storage
    df = query_job.to_dataframe()

    print("\n查询结果 (Top Rows):")
    print(df.head())

    return df


if __name__ == "__main__":
    # 尝试查询 'CA' (加州) 的前 5 名
    run_parameterized_query("CA", 5)
