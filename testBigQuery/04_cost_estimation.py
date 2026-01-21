from google.cloud import bigquery

# 初始化
PROJECT_ID = "webeye-internal-test"
client = bigquery.Client(project=PROJECT_ID)

def estimate_query_cost():
    """演示 Dry Run (预运行) 来估算成本"""
    
    # 这是一个比较大的 Public Data 查询 (Wikipedia 访问记录)
    # 如果不加 LIMIT 直接跑，或者不小心写了 SELECT *，数据量可能很大
    query = """
        SELECT wiki, title, SUM(views) as total_views
        FROM `bigquery-public-data.wikipedia.pageviews_2020`
        WHERE date(datehour) = '2020-01-01'
        GROUP BY wiki, title
        ORDER BY total_views DESC
        LIMIT 10
    """

    # 1. 配置 Dry Run
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # 2. 发起查询请求 (此时不会真正运行，也不会计费)
    query_job = client.query(query, job_config=job_config)

    # 3. 查看统计信息
    bytes_processed = query_job.total_bytes_processed
    gb_processed = bytes_processed / (1024 * 1024 * 1024)
    
    print(f"--- 成本预估 ---")
    print(f"此查询将扫描: {bytes_processed} 字节")
    print(f"约合: {gb_processed:.2f} GB")
    
    # BigQuery 免费额度通常是每月 1TB (On-demand)
    # 假设价格是 $5.00 per TB (具体看区域)
    cost = (bytes_processed / (1024 ** 4)) * 5.00
    print(f"预计费用 (按 $5/TB 计算): ${cost:.4f}")

    # 如果你能接受这个成本，再把 dry_run=False 真正跑一次
    # real_job = client.query(query) ...


def run_safe_query_with_limit():
    """演示使用 maximum_bytes_billed 作为安全断路器"""
    print("\n--- 安全查询演示 (Maximum Bytes Billed) ---")
    
    query = """
        SELECT wiki, title, SUM(views) as total_views
        FROM `bigquery-public-data.wikipedia.pageviews_2020`
        WHERE date(datehour) = '2020-01-01'
        GROUP BY wiki, title
        ORDER BY total_views DESC
        LIMIT 10
    """
    
    # 设置硬限制：例如 100 MB
    # 💡 最佳实践: 在所有生产环境查询中，都应该根据预估设置这个值。
    # 它充当“熔断器”，防止因为手误写错 SQL (如漏掉分区条件) 导致产生天价账单。
    _limit_mb = 1
    LIMIT_BYTES = _limit_mb * 1024 * 1024 
    
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=LIMIT_BYTES
    )

    try:
        print(f"尝试运行查询，由于 maximum_bytes_billed 设置为 {LIMIT_BYTES} 字节 ({_limit_mb}MB)...")
        # 真正发起查询，而不是 dry_run
        query_job = client.query(query, job_config=job_config)
        results = query_job.result() # 等待完成
        print("查询成功完成 (这不应该发生，除非数据量很小)")
        
    except Exception as e:
        print("\n[预期内的报错] 查询被拦截了！这帮你省钱了。")
        print(f"错误详情: {e}")

if __name__ == "__main__":
    estimate_query_cost()
    run_safe_query_with_limit()
