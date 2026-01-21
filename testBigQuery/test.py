from google.cloud import bigquery

# 初始化客户端
# 如果你已经用 gcloud 设置了默认项目，这里可以不传 project 参数
client = bigquery.Client(project="webeye-internal-test")

# 编写 SQL (推荐使用标准 SQL)
query = """
    SELECT name, SUM(number) as total_count
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    ORDER BY total_count DESC
    LIMIT 10
"""

# # A. 执行 SQL 查询并获取结果
# # 这是最基础的用法，适用于获取少量数据或执行管理任务。
# # 执行查询
# query_job = client.query(query)

# # 等待任务完成并获取结果
# results = query_job.result()

# print("查询结果：")
# for row in results:
#     print(f"姓名: {row.name}, 总数: {row.total_count}")

# B. 直接转换为 Pandas DataFrame (推荐)
# 如果你要处理数据，这种方式最高效。
df = client.query(query).to_dataframe()

# 现在你可以像操作普通 Pandas 数据一样操作它
print(df.head())