import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Text2sql-Benchmark",
    page_icon="🧪",
    layout="wide"
)

# function for Load results and is converted in pandas datafreme : it will be cached 
@st.cache_data
def load_results():
    with open("results/raw_results05.json") as f:
        return pd.DataFrame(json.load(f))
# results stored in df
df = load_results()

#       HAED
st.title("🧪 Text2sql-Benchmark")
st.caption("Benchmarking LLMs on Text-to-SQL across models and prompt strategies")
st.divider()

#       FILTERS IN SIDEBAR
st.sidebar.header("Filters")
selected_models = st.sidebar.multiselect(
    "Models",
    options=df["model"].unique(),
    default=df["model"].unique()
)
selected_strategies = st.sidebar.multiselect(
    "Prompt Strategies",
    options=df["strategy"].unique(),
    default=df["strategy"].unique()
)

filtered = df[
    df["model"].isin(selected_models) &
    df["strategy"].isin(selected_strategies)
]

#       TOP METRICS/KPIs
st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Runs", len(filtered))
col2.metric("Avg Exact Match", f"{filtered['exact_match'].mean():.1%}")
col3.metric("Avg Execution Accuracy", f"{filtered['execution_accuracy'].mean():.1%}")
col4.metric("Avg Token F1", f"{filtered['token_f1'].mean():.2f}")

st.divider()

#       Leaderboard ; ON EXECUTION ACCURACCY
st.subheader("🏆 Leaderboard")

leaderboard = filtered.groupby(["model", "strategy"])[
    ["exact_match", "token_f1", "execution_accuracy", "latency_ms"]
].mean().round(3).reset_index()

leaderboard = leaderboard.sort_values("execution_accuracy", ascending=False) #<--
leaderboard.columns= ["Model", "Strategy", "Exact Match", "Token F1", "Execution Accuracy", "Latency (ms)"]

st.dataframe(
    leaderboard,
    use_container_width = True,
    hide_index = True
)

st.divider()

#       CHARTS AND GRAPHS
st.subheader("📈 Metric Comparison")

col1, col2 = st.columns(2)

with col1:
    st.write("**Execution Accuracy by Model**")
    chart_data = filtered.groupby("model")["execution_accuracy"].mean().round(3)
    st.bar_chart(chart_data)

with col2:
    st.write("**Exact Match by Prompt Strategy**")
    chart_data2 =filtered.groupby("strategy")["exact_match"].mean().round(3)
    st.bar_chart(chart_data2)

col3,col4 = st.columns(2)

with col3:
    st.write("**Avg Latency by Model (ms)**")
    latency_data = filtered.groupby("model")["latency_ms"].mean().round(1)
    st.bar_chart(latency_data)

with col4:
    st.write("**Token F1 by Model**")
    f1_data=filtered.groupby("model")["token_f1"].mean().round(3)
    st.bar_chart(f1_data)

st.divider()

#       COMPARISION BLOCK
st.subheader("🔍 Per Query Comparision")
st.caption("Pick any question and see what each model generated")

questions = filtered["question"].unique().tolist()
selected_question = st.selectbox("Select a question", questions)

example_df = filtered[filtered["question"] == selected_question][
    ["model", "strategy", "expected_sql", "generated_sql", "exact_match", "execution_accuracy", "latency_ms"]
]

for _, row in example_df.iterrows():
    with st.expander(f"**{row['model']}** | {row['strategy']} | Exec Acc: {row['execution_accuracy']} | Exact: {row['exact_match']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Expected SQL**")
            st.code(row["expected_sql"], language ="sql")
        with col2:
            st.write("**Generated SQL**")
            st.code(row["generated_sql"], language="sql")
        st.caption(f"Latency: {row['latency_ms']} ms")