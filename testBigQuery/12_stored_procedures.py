from google.cloud import bigquery

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
PROCEDURE_ID = f"{DATASET_ID}.cleanup_old_logs"
# 目标表（我们在 Phase 2 中创建的 app_logs）
TARGET_TABLE = f"{DATASET_ID}.app_logs"

client = bigquery.Client(project=PROJECT_ID)

def create_stored_procedure():
    """
    创建存储过程 (Stored Procedure)。
    场景: 定期清理 N 天前的日志。把这个逻辑封装起来，以后只需要调用 CALL cleanup_old_logs(30) 即可。
    """
    print(f"--- 1. 创建存储过程: {PROCEDURE_ID} ---")
    
    # 定义过程：接受一个 INT64 参数 days_to_keep
    query = f"""
        CREATE OR REPLACE PROCEDURE `{PROCEDURE_ID}`(days_to_keep INT64)
        BEGIN
            -- 声明变量用于打印日志
            DECLARE cutoff_date DATE;
            SET cutoff_date = DATE_SUB(CURRENT_DATE(), INTERVAL days_to_keep DAY);
            
            -- 事务处理 (Optional, BigQuery 对单表操作默认是原子的)
            -- 打印开始清理
            SELECT format("开始清理 %t 之前的数据...", cutoff_date);
            
            -- 执行删除
            DELETE FROM `{TARGET_TABLE}`
            WHERE date(event_timestamp) < cutoff_date;
            
            -- 打印完成
            SELECT "清理完成！";
            
        END;
    """
    
    job = client.query(query)
    job.result()
    print("存储过程创建成功！")

def call_procedure():
    """在 Python 中调用存储过程"""
    print("\n--- 2. 调用存储过程 ---")
    
    # 比如清理 7 天前的数据
    query = f"CALL `{PROCEDURE_ID}`(7);"
    
    job = client.query(query)
    # 存储过程同样可能产生多个结果集
    job.result()
    print("存储过程调用结束。")

if __name__ == "__main__":
    # 确保存储过程依赖的表存在
    try:
        client.get_table(TARGET_TABLE)
        create_stored_procedure()
        call_procedure()
    except Exception as e:
        print(f"依赖表不存在或其他错误: {e}")
        print("请确保先运行过 06_partitioning_clustering.py")
