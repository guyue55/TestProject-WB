from google.cloud import bigquery

PROJECT_ID = "webeye-internal-test"
DATASET_ID = f"{PROJECT_ID}.learning_bq"
MODEL_ID = f"{DATASET_ID}.sample_kmeans_model"

client = bigquery.Client(project=PROJECT_ID)


def train_kmeans_model():
    """
    使用 SQL 直接在 BigQuery 中训练 K-Means 聚类模型。
    场景: 我们想根据 Wikipedia 的浏览量数据，把不同的 Title 聚类成几组（热门/冷门等）。

    💡 为什么用 BQML?
    通常 ML 流程是: 数据库 -> 导出 CSV -> Python/Spark 训练。数据移动非常慢且不安全。
    BQML 则是 "代码移动到数据旁"，直接在数据库内部训练，非常适合大规模数据集。
    """
    print(f"--- 1.开始训练 BQML 模型: {MODEL_ID} ---")
    print("这可能需要几分钟，因为是在训练模型...")

    # CREATE OR REPLACE MODEL
    # OPTIONS(model_type='kmeans', num_clusters=3, standardize_features=TRUE)
    query = f"""
        CREATE OR REPLACE MODEL `{MODEL_ID}`
        OPTIONS(model_type='kmeans', num_clusters=3, standardize_features = TRUE) AS
        
        SELECT
            SUM(views) as total_views,
            COUNT(DISTINCT wiki) as language_count
        FROM `bigquery-public-data.wikipedia.pageviews_2020`
        WHERE date(datehour) = '2020-01-01'
        GROUP BY title
        HAVING total_views > 1000  -- 只取有一定访问量的数据训练
        LIMIT 10000 -- 数据量控制，演示用
    """

    job = client.query(query)
    job.result()  # 等待完成
    print("模型训练完成！")


def predict_using_model():
    """使用训练好的模型进行预测 (Clustering)"""
    print("\n--- 2. 使用模型预测 (ML.PREDICT) ---")

    # ML.PREDICT(MODEL `model_name`, TABLE `input_data`)
    query = f"""
        SELECT 
            centroid_id, 
            title, 
            total_views
        FROM
            ML.PREDICT(MODEL `{MODEL_ID}`, 
            (
                SELECT
                    title,
                    SUM(views) as total_views,
                    COUNT(DISTINCT wiki) as language_count
                FROM `bigquery-public-data.wikipedia.pageviews_2020`
                WHERE date(datehour) = '2020-01-02' -- 预测第二天的数据
                GROUP BY title
                LIMIT 10
            ))
        ORDER BY total_views DESC
    """

    df = client.query(query).to_dataframe()
    print("预测结果 (前10行):")
    print(df)


if __name__ == "__main__":
    train_kmeans_model()
    predict_using_model()
