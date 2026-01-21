from google.cloud import bigquery

PROJECT_ID = "webeye-internal-test"
client = bigquery.Client(project=PROJECT_ID)


def run_scripting_demo():
    """
    演示 BigQuery Scripting: 变量声明、WHILE 循环、IF 判断。
    这让 SQL 具备了编程语言的控制流能力。
    """
    print("--- 运行脚本化 SQL (BigQuery Scripting) ---")

    # 一个带有逻辑的脚本：
    # 1. 定义变量 date_var, limit_var
    # 2. 循环打印日期（模拟每日处理）
    # 3. 动态查询
    query = """
        -- 声明变量
        DECLARE date_var DATE DEFAULT DATE('2020-01-01');
        DECLARE limit_var INT64 DEFAULT 3;
        
        -- 简单的循环示例
        WHILE date_var <= DATE('2020-01-03') DO
            
            -- 在控制台打印信息 (相当于 Python print)
            SELECT format("正在处理日期: %t", date_var) as status_message;
            
            -- 执行查询 (这里只是演示，可以是复杂的 UPDATE/INSERT)
            SELECT 
                wiki,    -- 记得我们修复过这个问题，用 wiki 而不是 language
                title, 
                SUM(views) as daily_views
            FROM `bigquery-public-data.wikipedia.pageviews_2020`
            WHERE date(datehour) = date_var
            GROUP BY wiki, title
            ORDER BY daily_views DESC
            LIMIT 5; 
            -- 💡 坑点注意: LIMIT 子句不直接支持脚本变量 (e.g. LIMIT limit_var)。
            -- 如果非要用变量控制 LIMIT，必须使用 EXECUTE IMMEDIATE "SELECT ... LIMIT ?" USING limit_var;
            
            -- 增加日期
            SET date_var = DATE_ADD(date_var, INTERVAL 1 DAY);
            
        END WHILE;
    """

    # 注意: 脚本化查询通常会返回多个 Job 结果（每个 SELECT 都是一个子 Job）
    parent_job = client.query(query)

    # 等待整个脚本执行完成
    parent_job.result()
    print("脚本执行完成！(可在 BigQuery 控制台查看多个子任务的输出)")


if __name__ == "__main__":
    run_scripting_demo()
