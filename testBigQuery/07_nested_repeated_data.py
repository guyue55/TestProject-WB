from google.cloud import bigquery
import json

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
TABLE_ID = f"{DATASET_ID}.complex_orders"

client = bigquery.Client(project=PROJECT_ID)

def create_complex_table():
    """
    创建一个包含嵌套(STRUCT)和重复(ARRAY)字段的表。
    这模拟了电商订单结构：一个订单包含多个商品(Items)，每个商品有自己的属性。
    """
    print(f"--- 创建复杂结构表: {TABLE_ID} ---")
    
    schema = [
        bigquery.SchemaField("order_id", "STRING", mode="REQUIRED"),
        # 嵌套 + 重复 = 结构体数组 (Array of Structs)
        bigquery.SchemaField(
            "items", 
            "RECORD", 
            mode="REPEATED", # 表示这是一个数组
            fields=[
                bigquery.SchemaField("sku", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
            ]
        ),
        # 💡 NoSQL 能力: 
        # 传统数据库需要 Order表 和 OrderItems表 进行 Join。
        # BigQuery 这里直接把 Items 数组存在包含它们的 Order 行里。读取时无需 Join，速度极快。
        # 简单的 Struct (收货地址)
        bigquery.SchemaField(
            "shipping_address",
            "RECORD",
            mode="NULLABLE",
            fields=[
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("zipcode", "STRING"),
            ]
        )
    ]

    table = bigquery.Table(TABLE_ID, schema=schema)
    try:
        table = client.create_table(table)
        print("表创建成功。")
    except Exception as e:
        print(f"表可能已存在: {e}")

def insert_complex_data():
    """插入嵌套数据，直接使用 Python 字典即可"""
    print("\n--- 插入复杂数据 ---")
    
    rows = [
        {
            "order_id": "ORD-001",
            "items": [
                {"sku": "A100", "quantity": 1, "price": 29.99},
                {"sku": "B200", "quantity": 2, "price": 9.99}
            ],
            "shipping_address": {"city": "New York", "zipcode": "10001"}
        },
        {
            "order_id": "ORD-002",
            "items": [
                {"sku": "A100", "quantity": 5, "price": 29.99}
            ],
            "shipping_address": {"city": "San Francisco", "zipcode": "94105"}
        }
    ]
    
    errors = client.insert_rows_json(TABLE_ID, rows)
    if not errors:
        print("复杂数据插入成功！")
    else:
        print(f"插入错误: {errors}")

def query_nested_data():
    """
    关键知识点: UNNEST()
    在 SQL 中，你不能直接 `SELECT items` 得到扁平化结果。需要使用 UNNEST() 将数组“炸开”成行。
    """
    print("\n--- 查询并展开数组 (UNNEST) ---")
    
    # 场景: 计算每个 SKU 的总销售量
    # CROSS JOIN UNNEST(items) 将每一行订单炸开成多行商品
    query = f"""
        SELECT 
            i.sku,
            SUM(i.quantity) as total_quantity,
            SUM(i.quantity * i.price) as total_revenue
        FROM `{TABLE_ID}`,
        UNNEST(items) as i 
        GROUP BY i.sku
        ORDER BY total_revenue DESC
    """
    
    # 💡 语法解析: 
    # `FROM table, UNNEST(items) as i` 这种写法是 Standard SQL 的简写，
    # 等同于 `FROM table CROSS JOIN UNNEST(items) as i`。
    # 它把一行 (Order) 变成了多行 (Items)，每行包含 Order 原始列 + 对应的单个 Item。
    
    # 注意: 数据刚插入可能需要一点时间才能查到 (Streaming Buffer)
    try:
        query_job = client.query(query)
        print("查询结果:")
        for row in query_job:
            print(f"SKU: {row.sku}, 销量: {row.total_quantity}, 营收: {row.total_revenue:.2f}")
    except Exception as e:
        print(f"查询出错 (可能是数据还没这就绪): {e}")

if __name__ == "__main__":
    # client.delete_table(TABLE_ID, not_found_ok=True)
    create_complex_table()
    insert_complex_data()
    import time
    print("等待几秒让数据对流式API可见...")
    time.sleep(3)
    query_nested_data()
