from google.cloud import bigquery

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
UDF_NAME = f"{DATASET_ID}.parse_user_agent"

client = bigquery.Client(project=PROJECT_ID)

def create_persistent_udf():
    """
    创建一个持久化 UDF (User Defined Function)。
    场景: 我们想解析 User-Agent 字符串，提取浏览器信息。SQL 处理这个很麻烦，但 JavaScript 有现成的正则能力。
    """
    print(f"--- 1. 创建 JavaScript UDF: {UDF_NAME} ---")
    
    # 这是一个 JavaScript UDF，输入 STRING，输出 STRING
    query = f"""
        CREATE OR REPLACE FUNCTION `{UDF_NAME}`(ua STRING)
        RETURNS STRING
        LANGUAGE js
        AS r\"\"\"
            if (!ua) return null;
            if (ua.includes("Chrome")) return "Chrome";
            if (ua.includes("Firefox")) return "Firefox";
            if (ua.includes("Safari")) return "Safari";
            return "Other";
        \"\"\";
    """
    
    # 注意: 创建 Routine (Function) 也使用 client.query
    job = client.query(query)
    job.result()
    print("UDF 创建成功！已经被存储在 Dataset 中。")

def use_udf_in_query():
    """在查询中调用刚才定义的 UDF"""
    print("\n--- 2. 调用 UDF 进行查询 ---")
    
    # 模拟一些数据
    query = f"""
        WITH sample_data AS (
            SELECT "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36" as ua
            UNION ALL
            SELECT "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0" as ua
            UNION ALL
            SELECT "Unknown User Agent" as ua
        )
        
        SELECT 
            ua, 
            `{UDF_NAME}`(ua) as browser_type -- 调用 UDF
        FROM sample_data
    """
    
    df = client.query(query).to_dataframe()
    print("查询结果:")
    print(df)

if __name__ == "__main__":
    create_persistent_udf()
    use_udf_in_query()
