from google.cloud import bigquery
from google.cloud.exceptions import NotFound

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
TABLE_ID = f"{DATASET_ID}.users"

client = bigquery.Client(project=PROJECT_ID)


def inspect_current_schema():
    """1. 检查当前 Schema"""
    print(f"--- 正在检查表 {TABLE_ID} 的 Schema ---")
    try:
        table = client.get_table(TABLE_ID)
        print(f"表描述: {table.description}")
        print("当前列:")
        for field in table.schema:
            print(
                f" - 字段名: {field.name}, 类型: {field.field_type}, 模式: {field.mode}, 描述: {field.description}"
            )
        return table
    except NotFound:
        print("表不存在，请先运行 02_manage_resources.py")
        return None


def add_new_column(table):
    """2. 添加新列 (Schema Evolution)"""
    # 场景: 业务变了，需要增加用户的 'phone_number'
    print("\n--- 正在尝试添加 'phone_number' 列 ---")

    # 检查是否已经存在
    current_field_names = [f.name for f in table.schema]
    if "phone_number" in current_field_names:
        print("列 'phone_number' 已经存在，跳过。")
        return

    # BigQuery 增加列非常快，不需要重建表
    # 注意: 只能添加 NULLABLE 或 REPEATED (不能添加 REQUIRED，除非表是空的)
    new_schema = table.schema[:]  # 复制当前 schema
    new_schema.append(
        bigquery.SchemaField(
            "phone_number", "STRING", mode="NULLABLE", description="用户手机号"
        )
    )

    # 关键修正: 为了防止 412 Precondition Failed，在更新前最好确保 table 对象是最新的
    # 或者直接使用 table.etag = None (但这会跳过冲突检查，风险较高)
    # 这里我们在函数开头没有重新 get，如果之前有别的操作可能会导致 etag 过期
    # 最稳妥的方式: 重新 get 一次
    table = client.get_table(TABLE_ID)
    table.schema = new_schema
    table = client.update_table(table, ["schema"])  # 明确指定只更新 schema

    # 💡 关键修正: 为了防止 "412 Precondition Failed" 错误。
    # BigQuery 使用乐观锁 (Optimistic Locking)。如果在你 update 之前，表被其他人修改了（etag 变了），update 会失败。
    # 虽然在简单脚本里概率低，但在高并发生产环境中，update 前必须重新 get_table()。
    print("列添加成功！")


def update_field_description(table):
    """3. 更新字段描述"""
    print("\n--- 正在更新 'username' 的描述 ---")

    # 获取最新的 table 避免 412
    table = client.get_table(TABLE_ID)

    new_schema = []
    for field in table.schema:
        if field.name == "username":
            # 修改描述
            new_field = field.to_api_repr()
            new_field["description"] = "更新后的用户名描述 (Updated via Python)"
            new_schema.append(bigquery.SchemaField.from_api_repr(new_field))
        else:
            new_schema.append(field)

    table.schema = new_schema
    table = client.update_table(table, ["schema"])
    print("描述更新成功！")


if __name__ == "__main__":
    table = inspect_current_schema()
    if table:
        add_new_column(table)
        update_field_description(table)

        # 再次检查确认
        print("\n--- 最终检查 ---")
        inspect_current_schema()
