import contextlib
import os
from io import StringIO

import altair as alt
import streamlit as st
from google.cloud import bigquery

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="BigQuery 实战平台",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 初始化 Client (缓存以加速)
@st.cache_resource
def get_client():
    return bigquery.Client(project="webeye-internal-test")


client = get_client()

# --- 2. 实战目录定义 ---
# 映射：显示名称 -> 文件名
TUTORIALS = {
    "01. 进阶查询 (Advanced Query)": "01_advanced_query.py",
    "02. 资源管理 (Manage Resources)": "02_manage_resources.py",
    "03. 数据写入 (Data Ingestion)": "03_data_ingestion.py",
    "04. 成本估算 (Cost Estimation)": "04_cost_estimation.py",
    "05. Schema 演进 (Evolution)": "05_schema_evolution.py",
    "06. 分区与分簇 (Partitioning)": "06_partitioning_clustering.py",
    "07. 复杂数据 (Nested/Repeated)": "07_nested_repeated_data.py",
    "08. 机器学习 (BQML)": "08_bigquery_ml.py",
    "09. 自定义函数 (UDFs)": "09_user_defined_functions.py",
    "10. 物化视图 (Materialized Views)": "10_materialized_views.py",
    "11. 脚本编程 (Scripting)": "11_scripting_loops.py",
    "12. 存储过程 (Stored Procedures)": "12_stored_procedures.py",
    "13. 定时任务 (Scheduled Queries)": "13_scheduled_queries.py",
}

# --- 3. Sidebar 导航 ---
st.sidebar.title("🚀 BigQuery 实战")
selected_tutorial = st.sidebar.radio(
    "选择章节", ["🛠️ SQL Playground (游乐场)"] + list(TUTORIALS.keys())
)

st.sidebar.divider()
st.sidebar.info("Tips: 下拉选择不同章节，可以在右侧直接运行代码或查看可视化成果。")

# --- 4. 核心逻辑 ---

# === 模式 A: SQL Playground ===
if selected_tutorial == "🛠️ SQL Playground (游乐场)":
    st.header("🛠️ SQL 在线游乐场")
    st.markdown("直接编写 SQL 并运行，支持自动图表生成。")

    col1, col2 = st.columns([3, 1])
    with col1:
        default_sql = """SELECT title, SUM(views) as views
FROM `bigquery-public-data.wikipedia.pageviews_2020`
WHERE date(datehour) = '2020-01-01'
GROUP BY title
ORDER BY views DESC
LIMIT 10"""
        user_sql = st.text_area("输入 SQL", value=default_sql, height=250)

    with col2:
        st.write("快捷模板:")
        if st.button("查日志"):
            user_sql = (
                "SELECT * FROM `webeye-internal-test.learning_bq.app_logs` LIMIT 20"
            )
            st.rerun()

    if st.button("运行查询 ▶️", type="primary"):
        try:
            query_job = client.query(user_sql)
            df = query_job.to_dataframe()
            st.success(f"查询成功! 扫描: {query_job.total_bytes_processed} Bytes")
            st.dataframe(df)

            # 智能绘图
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0 and len(df.columns) >= 2:
                st.caption("自动生成的图表预览")
                st.bar_chart(df.set_index(df.columns[0])[num_cols[0]])
        except Exception as e:
            st.error(f"出错: {e}")

# === 模式 B: 实战章节学习 ===
else:
    file_name = TUTORIALS[selected_tutorial]
    st.header(f"📘 {selected_tutorial}")

    # 创建两个 Tab: 代码运行 vs 可视化展示
    tab_code, tab_viz = st.tabs(
        ["📝 代码实验室 (Code Lab)", "📊 可视化深度演示 (Deep Dive)"]
    )

    # --- Tab 1: 代码编辑与运行 ---
    with tab_code:
        st.markdown(f"当前文件: `{file_name}`")

        # 读取源码
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                code_content = f.read()
        else:
            code_content = "# 文件未找到"

        # 代码编辑器
        edited_code = st.text_area(
            "源码 (支持在线修改运行):", value=code_content, height=400
        )

        # 运行按钮
        if st.button(f"运行 {file_name} 脚本 ▶️"):
            # 使用 empty 占位符以便后续隐藏
            exec_info = st.empty()
            exec_info.info("正在执行脚本，正在捕获输出...")

            # --- 黑科技: 捕获 Print 输出 redirection ---
            output_capture = StringIO()
            try:
                with contextlib.redirect_stdout(output_capture):
                    # 创建一个独立的执行环境，注入必要的库
                    exec_env = {"__name__": "__main__"}
                    exec(edited_code, exec_env)

                # 执行成功，清除提示并显示结果
                exec_info.empty()
                st.subheader("🖥️ 终端输出")
                st.code(output_capture.getvalue(), language="text")
                st.success("脚本执行完毕!")

            except Exception as e:
                # 即使出错也清除“正在运行”提示
                exec_info.empty()
                st.error(f"脚本执行出错: {e}")
                st.subheader("Traceback")
                st.code(output_capture.getvalue(), language="text")

    # --- Tab 2: 定制化可视化展示 ---
    with tab_viz:
        st.markdown("针对本章节的重点成果展示。")

        # 针对 01_进阶查询 的展示
        if "01" in file_name:
            st.subheader("📊 公共数据集查询演示")
            st.markdown("查询 `usa_names` 公共数据集并进行可视化。")
            if st.button("查看名字分布 (CA, 10)"):
                q = """
                SELECT name, SUM(number) as total_count
                FROM `bigquery-public-data.usa_names.usa_1910_current`
                WHERE state = 'CA'
                GROUP BY name ORDER BY total_count DESC LIMIT 10
                """
                df = client.query(q).to_dataframe()
                st.bar_chart(df.set_index("name"))
                st.dataframe(df)

        # 针对 08_机器学习 的特殊展示
        elif "08" in file_name:
            st.subheader("🧠 BQML 聚类结果可视化")
            if st.button("加载聚类散点图"):
                q = """
                SELECT centroid_id, title, total_views, language_count
                FROM ML.PREDICT(MODEL `webeye-internal-test.learning_bq.sample_kmeans_model`, 
                (SELECT title, SUM(views) as total_views, COUNT(DISTINCT wiki) as language_count
                 FROM `bigquery-public-data.wikipedia.pageviews_2020`
                 WHERE date(datehour) = '2020-01-02' GROUP BY title LIMIT 300))
                """
                df_ml = client.query(q).to_dataframe()

                # 数据清洗
                df_ml["centroid_id"] = df_ml["centroid_id"].astype(str)
                df_ml["total_views"] = df_ml["total_views"].astype(int)
                df_ml["language_count"] = df_ml["language_count"].astype(int)

                chart = (
                    alt.Chart(df_ml)
                    .mark_circle(size=60)
                    .encode(
                        x=alt.X("total_views", title="Views"),
                        y=alt.Y("language_count", title="Languages"),
                        color="centroid_id",
                        tooltip=["title"],
                    )
                    .interactive()
                )
                st.altair_chart(chart, use_container_width=True)

        # 针对 06_分区 的特殊展示
        elif "06" in file_name:
            st.subheader("⚡️ 分区裁剪 (Pruning) 效果演示")
            st.info("对比：查询全表 vs 查询分区")

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("普通查询成本 (模拟数据量)", "1.2 GB", delta="-100%")
            with col_b:
                st.metric("分区查询成本", "10 MB", delta="节省 99.2%")

            q_logs = "SELECT event_type, count(*) as c FROM `webeye-internal-test.learning_bq.app_logs` GROUP BY 1"
            if st.button("查看现有的日志分布"):
                try:
                    df = client.query(q_logs).to_dataframe()
                    st.bar_chart(df.set_index("event_type"))
                except:
                    st.warning(
                        "表可能不存在，请先在 'Code Lab' 运行 06 脚本创建并填充数据。"
                    )

        # 针对 07_嵌套数据 的特殊展示
        elif "07" in file_name:
            st.subheader("🧱 嵌套数据 (STRUCT/ARRAY) 展示")
            st.markdown("展示 `UNNEST` 后的扁平化订单数据。")
            if st.button("执行 UNNEST 查询"):
                try:
                    q = "SELECT order_id, i.sku, i.quantity FROM `webeye-internal-test.learning_bq.complex_orders`, UNNEST(items) as i LIMIT 10"
                    df = client.query(q).to_dataframe()
                    st.table(df)
                except:
                    st.warning("表可能不存在，请先在 'Code Lab' 运行 07 脚本。")

        # 针对 10_物化视图 的特殊展示
        elif "10" in file_name:
            st.subheader("🚀 物化视图 (Materialized Views) 极致加速")
            st.write("MV 会自动维护预聚合结果。")
            if st.button("查看 MV 聚合结果"):
                try:
                    q = "SELECT * FROM `webeye-internal-test.learning_bq.daily_event_stats` LIMIT 10"
                    df = client.query(q).to_dataframe()
                    st.line_chart(df.set_index("event_date"))
                except:
                    st.warning("物化视图可能不存在，请先运行 10 脚本。")

        # 针对 11_脚本 的特殊展示
        elif "11" in file_name:
            st.subheader("📜 脚本化执行历史")
            st.write("BigQuery Scripting 会产生多个 Child Jobs。")
            # 这里可以查询 INFORMATION_SCHEMA.JOBS_BY_USER ... 稍微复杂这不展开

        # 其他章节
        else:
            st.info(
                "� 该章节成果主要体现为后台逻辑（如资源创建、Schema 变更、定时任务配置）。"
            )
            st.markdown("建议在 **'📝 代码实验室'** 中运行脚本，并观察控制台输出。")
