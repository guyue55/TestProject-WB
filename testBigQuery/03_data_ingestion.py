from google.cloud import bigquery
import pandas as pd
import datetime
import time

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
TABLE_ID = f"{DATASET_ID}.users"

client = bigquery.Client(project=PROJECT_ID)

def insert_streaming_data():
    """
    方法 1: 流式插入 (Streaming Insert)
    ---
    ✅ 优点: 数据秒级可见，适合实时监控、日志流。
    ❌ 缺点: 按插入字节收费 (昂贵)，在数据落盘前(buffer期)无法更新/删除。
    """
    print("--- 开始流式插入 ---")
    
    rows_to_insert = [
        {"id": 101, "username": "alice", "email": "alice@example.com", "created_at": str(datetime.datetime.now()), "tags": ["admin", "editor"]},
        {"id": 102, "username": "bob", "email": "bob@example.com", "created_at": str(datetime.datetime.now()), "tags": ["viewer"]}
    ]

    # insert_rows_json 接受字典列表
    errors = client.insert_rows_json(TABLE_ID, rows_to_insert)
    
    if errors == []:
        print("流式插入成功！(数据可能需要几秒到几分钟才能完全可查询)")
    else:
        print(f"流式插入遇到错误: {errors}")

def load_data_from_dataframe():
    """
    方法 2: 批量加载 Job (Load Job)
    ---
    ✅ 优点: 完全免费！吞吐量巨大，支持原子性提交。
    ❌ 缺点: 非实时，通常用于 T+1 或小时级离线同步。
    💡 最佳实践: 只要不要求秒级实时，永远优先选择 Load Job。
    """
    print("\n--- 开始批量加载 (Load Job) ---")
    
    # 模拟一些本地数据
    data = {
        "id": [201, 202, 203],
        "username": ["charlie", "david", "eve"],
        "email": ["c@ex.com", "d@ex.com", "e@ex.com"],
        "created_at": [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()],
        "tags": [["vip"], [], ["new_user", "promo"]]
    }
    df = pd.DataFrame(data)

    # 配置加载作业
    job_config = bigquery.LoadJobConfig(
        # 指定写入模式:
        # WRITE_TRUNCATE: 覆盖原表
        # WRITE_APPEND: 追加 (默认)
        # WRITE_EMPTY: 仅当表为空时写入
        write_disposition="WRITE_APPEND",
    )

    # 发起加载任务
    job = client.load_table_from_dataframe(
        df, TABLE_ID, job_config=job_config
    )

    # 等待任务完成
    job.result() 

    print(f"批量加载完成。已加载 {job.output_rows} 行。")

    # 验证数据
    table = client.get_table(TABLE_ID)
    print(f"显示表信息: {table}")
    print(f"表当前总行数: {table.num_rows}")

if __name__ == "__main__":
    insert_streaming_data()
    # 等待一小会儿让流式缓冲稍微稳定一下（虽然不能保证立刻读到）
    time.sleep(2) 
    load_data_from_dataframe()
