import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import math

st.set_page_config(layout="wide", page_title="AMA Market Outcome Engine")

# =====================================================
# CONFIG
# =====================================================

DAYS = 60
INITIAL_CAPITAL = 100_000_000

GENRES = {
    "Indie Chill": {
        "segments": {
            "Gen Z": {"size": 80000, "ctr_base": 0.05, "retention_base": 0.65},
            "Millennials": {"size": 60000, "ctr_base": 0.04, "retention_base": 0.6},
            "Art Niche": {"size": 20000, "ctr_base": 0.06, "retention_base": 0.75}
        },
        "sponsor_threshold": 0.65
    },
    "Commercial Pop": {
        "segments": {
            "Teen Market": {"size": 150000, "ctr_base": 0.06, "retention_base": 0.55},
            "Mainstream": {"size": 200000, "ctr_base": 0.05, "retention_base": 0.5}
        },
        "sponsor_threshold": 0.6
    }
}

FAME_LEVELS = {
    "Chưa ai biết": 0.1,
    "Có fan địa phương": 0.3,
    "Đã có fan khu vực": 0.6
}

# =====================================================
# INPUT PHASE (POST-JUDGE)
# =====================================================

st.title("🎬 AMA – Mô phỏng thị trường sau khi sản phẩm hoàn thành")

st.subheader("Nhập kết quả chấm điểm từ giám khảo")

genre = st.selectbox("Thể loại", list(GENRES.keys()))
fame_label = st.selectbox("Mức độ nổi tiếng ban đầu", list(FAME_LEVELS.keys()))

narrative = st.slider("Điểm Câu chuyện (0-1)", 0.0, 1.0, 0.7)
visual = st.slider("Điểm Hình ảnh (0-1)", 0.0, 1.0, 0.7)
emotion = st.slider("Điểm Cảm xúc (0-1)", 0.0, 1.0, 0.7)
technical = st.slider("Điểm Kỹ thuật (0-1)", 0.0, 1.0, 0.7)
market_fit = st.slider("Điểm Phù hợp thị trường (0-1)", 0.0, 1.0, 0.7)
originality = st.slider("Điểm Sáng tạo (0-1)", 0.0, 1.0, 0.7)

# =====================================================
# SIMULATION ENGINE
# =====================================================

if st.button("🚀 Chạy mô phỏng 60 ngày"):

    fame = FAME_LEVELS[fame_label]
    trust = 0.3
    capital = INITIAL_CAPITAL

    history = []

    sponsor_unlocked = False
    sponsor_revenue = 0

    for day in range(DAYS):

        total_views = 0
        total_watch_time = 0
        total_revenue = 0

        for seg_name, seg in GENRES[genre]["segments"].items():

            impressions = seg["size"] * trust * (1 + fame)

            ctr = seg["ctr_base"] + 0.02 * visual + 0.01 * fame
            retention = seg["retention_base"] + 0.2 * narrative + 0.1 * emotion

            ctr *= np.random.normal(1, 0.05)
            retention *= np.random.normal(1, 0.05)

            views = impressions * ctr
            watch_time = views * retention

            streaming_revenue = views * 500

            merch_conversion = 0.02 * originality
            merch_revenue = views * merch_conversion * 100_000

            total_views += views
            total_watch_time += watch_time
            total_revenue += streaming_revenue + merch_revenue

        # Sponsor unlock logic
        avg_retention = total_watch_time / (total_views + 1)

        if (not sponsor_unlocked) and avg_retention > GENRES[genre]["sponsor_threshold"]:
            sponsor_unlocked = True
            sponsor_revenue = 20_000_000
            total_revenue += sponsor_revenue

        capital += total_revenue

        performance_score = (avg_retention + market_fit) / 2
        trust += 0.02 * (performance_score - 0.5)
        trust = max(0.1, min(1.0, trust))

        fame += 0.01 * performance_score
        fame = min(1.0, fame)

        history.append({
            "Ngày": day + 1,
            "Lượt xem": total_views,
            "Watch Time": total_watch_time,
            "Doanh thu": total_revenue,
            "Vốn tích lũy": capital
        })

    df = pd.DataFrame(history)

    st.subheader("📊 Diễn biến 60 ngày")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ngày"], y=df["Lượt xem"], name="Lượt xem"))
    fig.add_trace(go.Scatter(x=df["Ngày"], y=df["Doanh thu"], name="Doanh thu"))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Vốn cuối cùng sau 60 ngày", f"{int(capital):,} VND")

    # Monte Carlo Risk Simulation
    st.subheader("📉 Phân tích rủi ro (Monte Carlo 300 lần)")

    outcomes = []

    for _ in range(300):
        sim_capital = INITIAL_CAPITAL
        trust_sim = 0.3
        fame_sim = FAME_LEVELS[fame_label]

        for day in range(DAYS):
            views_sim = 100000 * trust_sim * (1 + fame_sim)
            revenue_sim = views_sim * (0.4 + 0.3 * narrative) * 500
            sim_capital += revenue_sim
            trust_sim += 0.01 * (market_fit - 0.5)
            fame_sim += 0.01 * (narrative - 0.5)

        outcomes.append(sim_capital)

    risk_df = pd.DataFrame({"Vốn cuối": outcomes})

    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=risk_df["Vốn cuối"]))
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.metric("Xác suất đạt > 120 triệu",
              f"{round((risk_df['Vốn cuối'] > 120_000_000).mean()*100,2)} %")
