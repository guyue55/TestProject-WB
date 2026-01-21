import contextlib
import os
from io import StringIO

import altair as alt
import streamlit as st
from google.cloud import bigquery
from streamlit_ace import st_ace  # 导入 Ace 编辑器

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

# --- 2. 实战目录定义与分组 ---
PHASES = {
    "1️⃣ 基础与成本 (Phase 1)": {
        "01. 进阶查询 (Advanced Query)": "01_advanced_query.py",
        "02. 资源管理 (Manage Resources)": "02_manage_resources.py",
        "03. 数据写入 (Data Ingestion)": "03_data_ingestion.py",
        "04. 成本估算 (Cost Estimation)": "04_cost_estimation.py",
    },
    "2️⃣ 性能与架构 (Phase 2)": {
        "05. Schema 演进 (Evolution)": "05_schema_evolution.py",
        "06. 分区与分簇 (Partitioning)": "06_partitioning_clustering.py",
        "07. 复杂数据 (Nested/Repeated)": "07_nested_repeated_data.py",
    },
    "3️⃣ 高级 SQL 与 ML (Phase 3)": {
        "08. 机器学习 (BQML)": "08_bigquery_ml.py",
        "09. 自定义函数 (UDFs)": "09_user_defined_functions.py",
        "10. 物化视图 (Materialized Views)": "10_materialized_views.py",
    },
    "4️⃣ 自动化编程 (Phase 4)": {
        "11. 脚本编程 (Scripting)": "11_scripting_loops.py",
        "12. 存储过程 (Stored Procedures)": "12_stored_procedures.py",
        "13. 定时任务 (Scheduled Queries)": "13_scheduled_queries.py",
    },
}

# 扁平化映射方便后续查找
TUTORIAL_MAP = {}
for p in PHASES.values():
    TUTORIAL_MAP.update(p)

# --- 3. Sidebar 导航 (学习路径强化) ---
st.sidebar.title("🚀 BigQuery 学习地图")

# A. 进度统计
st.sidebar.metric("实战章节总计", f"{len(TUTORIAL_MAP)}", "Active")

# B. 游乐场入口
if "selection" not in st.session_state:
    st.session_state.selection = "🛠️ SQL Playground (游乐场)"


def set_selection(val):
    st.session_state.selection = val


st.sidebar.button(
    "🛠️ SQL Playground (游乐场)",
    on_click=set_selection,
    args=("🛠️ SQL Playground (游乐场)",),
    use_container_width=True,
    type="primary"
    if st.session_state.selection == "🛠️ SQL Playground (游乐场)"
    else "secondary",
)

st.sidebar.markdown("---")
st.sidebar.subheader("📘 学习路径 (Course Path)")

# C. 序号增强的分组导航
for phase_name, items in PHASES.items():
    is_expanded = st.session_state.selection in items
    with st.sidebar.expander(f"**{phase_name}**", expanded=is_expanded):
        for label in items.keys():
            if st.button(
                label,
                key=f"btn_{label}",
                use_container_width=True,
                type="primary" if st.session_state.selection == label else "secondary",
            ):
                st.session_state.selection = label
                st.rerun()

st.sidebar.divider()
st.sidebar.info("💡 建议按照 01-13 的顺序进行实战，以获得最佳学习效果。")

selected_tutorial = st.session_state.selection

# --- 4. 核心逻辑 ---

# === 模式 A: SQL Playground ===
if selected_tutorial == "🛠️ SQL Playground (游乐场)":
    st.header("🛠️ SQL 在线游乐场")
    st.markdown("直接编写 SQL 并运行，支持自动图表生成。")

    # 快捷模板逻辑
    if "sql_input" not in st.session_state:
        st.session_state.sql_input = """SELECT title, SUM(views) as views
FROM `bigquery-public-data.wikipedia.pageviews_2020`
WHERE date(datehour) = '2020-01-01'
GROUP BY title
ORDER BY views DESC
LIMIT 10"""

    # 初始化 Ace 更新标识
    if "ace_update_key" not in st.session_state:
        st.session_state.ace_update_key = 0

    # --- 一体化 IDE 容器 ---
    with st.container(border=True):
        # 1. 工具栏 Header
        p_col1, p_col2 = st.columns([2, 3])
        with p_col1:
            st.markdown("🔍 **SQL Editor**")
        with p_col2:
            # 使用横向按钮组作为快捷模板，避免 selectbox 的状态死循环
            sub_col1, sub_col2, sub_col3 = st.columns([1, 1, 1])
            with sub_col1:
                if st.button(
                    "📋 查日志", use_container_width=True, help="载入 APP 日志查询模板"
                ):
                    st.session_state.sql_input = "SELECT * FROM `webeye-internal-test.learning_bq.app_logs` LIMIT 20"
                    st.session_state.ace_update_key += 1  # 强制编辑器刷新
                    st.rerun()
            with sub_col2:
                if st.button(
                    "🗺️ 维基百科",
                    use_container_width=True,
                    help="载入维基百科热词查询模板",
                ):
                    st.session_state.sql_input = """SELECT title, SUM(views) as views
FROM `bigquery-public-data.wikipedia.pageviews_2020`
WHERE date(datehour) = '2020-01-01'
GROUP BY title
ORDER BY views DESC
LIMIT 10"""
                    st.session_state.ace_update_key += 1
                    st.rerun()
            with sub_col3:
                # 运行按钮放在最右侧
                run_playground = st.button(
                    "运行 ▶️", type="primary", use_container_width=True, key="run_sql_pg"
                )

        # 2. 编辑器 Body
        user_sql = st_ace(
            value=st.session_state.sql_input,
            language="sql",
            theme="monokai",
            height=200,
            font_size=14,
            auto_update=True,  # 开启自动同步，无需手动点击 Apply
            # 使用动态 key，当点击模板按钮时，这个 key 会改变，强制编辑器重新加载内容
            key=f"sql_playground_editor_{st.session_state.ace_update_key}",
        )
        st.session_state.sql_input = user_sql

    # 3. 输出结果
    if run_playground:
        if not user_sql.strip():
            st.warning("SQL 不能为空")
        else:
            output_container = st.container(border=True)
            with output_container:
                status = st.empty()
                status.info("⚡ 正在执行查询...")
                try:
                    query_job = client.query(user_sql)
                    df = query_job.to_dataframe()
                    status.empty()
                    st.success(
                        f"✅ 查询成功! 扫描: {query_job.total_bytes_processed} Bytes"
                    )
                    st.dataframe(df)

                    num_cols = df.select_dtypes(include=["number"]).columns
                    if len(num_cols) > 0 and len(df.columns) >= 2:
                        st.caption("自动生成的图表预览")
                        st.bar_chart(df.set_index(df.columns[0])[num_cols[0]])
                except Exception as e:
                    status.empty()
                    st.error(f"❌ 出错: {e}")

# === 模式 B: 实战章节学习 ===
else:
    file_name = TUTORIAL_MAP[selected_tutorial]
    st.header(f"📘 {selected_tutorial}")

    # 创建两个 Tab: 代码运行 vs 可视化展示
    tab_code, tab_viz = st.tabs(
        ["📝 代码实验室 (Code Lab)", "📊 可视化深度演示 (Deep Dive)"]
    )

    # --- Tab 1: 代码编辑 与 运行 (一体化 IDE 风格) ---
    with tab_code:
        # 0. 读取源码内容
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                code_content = f.read()
        else:
            code_content = "# 文件未找到"

        # 在同一个 border 容器内，实现 Header + Body 结构
        with st.container(border=True):
            # 1. 顶部工具栏 (Header)
            tool_col1, tool_col2 = st.columns([5, 1])
            with tool_col1:
                st.markdown(f"📄 **{file_name}**")
            with tool_col2:
                run_btn = st.button("运行 ▶️", type="primary", use_container_width=True)

            # 紧贴下方的编辑器
            edited_code = st_ace(
                value=code_content,
                language="python",
                theme="monokai",
                keybinding="vscode",
                height=450,
                font_size=14,
                wrap=True,
                auto_update=True,  # 开启自动同步
                key=f"ace_{file_name}",
            )

        # 3. 输出区 (紧随其后)
        if run_btn:
            output_container = st.container(border=True)
            with output_container:
                status_placeholder = st.empty()
                status_placeholder.info("⚡ 正在执行...")

                output_capture = StringIO()
                try:
                    with contextlib.redirect_stdout(output_capture):
                        exec_env = {"__name__": "__main__"}
                        exec(edited_code, exec_env)

                    status_placeholder.empty()
                    st.success("✅ 执行完毕")
                    st.code(
                        output_capture.getvalue() or "> 脚本正常结束", language="text"
                    )

                except Exception as e:
                    status_placeholder.empty()
                    st.error(f"❌ 出错: {e}")
                    st.code(
                        output_capture.getvalue() + f"\n\n[Error]: {e}", language="text"
                    )

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
                except Exception:
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
                except Exception:
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
                except Exception:
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
