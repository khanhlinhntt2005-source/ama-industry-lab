import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide", page_title="AMA Industry Simulation Advanced")

# ============================================
# CẤU HÌNH HỆ THỐNG
# ============================================

DAYS = 60
INITIAL_CAPITAL = 100_000_000

GENRES = {
    "Indie Chill": {
        "segments": {
            "Gen Z": {"size": 80000, "ctr_base": 0.05, "retention_base": 0.65},
            "Millennials": {"size": 60000, "ctr_base": 0.04, "retention_base": 0.6}
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
    "Có fan khu vực": 0.6
}

# ============================================
# INPUT PHASE
# ============================================

st.title("🎬 AMA – Post Judge Market Engine (Advanced)")

genre = st.selectbox("Thể loại", list(GENRES.keys()))
fame_label = st.selectbox("Mức độ nổi tiếng ban đầu", list(FAME_LEVELS.keys()))

st.subheader("Điểm từ giám khảo")

narrative = st.slider("Câu chuyện", 0.0, 1.0, 0.7)
visual = st.slider("Hình ảnh", 0.0, 1.0, 0.7)
emotion = st.slider("Cảm xúc", 0.0, 1.0, 0.7)
technical = st.slider("Kỹ thuật", 0.0, 1.0, 0.7)
market_fit = st.slider("Phù hợp thị trường", 0.0, 1.0, 0.7)
originality = st.slider("Sáng tạo", 0.0, 1.0, 0.7)

# ============================================
# CHI PHÍ BỔ SUNG
# ============================================

st.subheader("Chiến lược bổ sung")

minishow = st.checkbox("Tổ chức Minishow (chi phí 15 triệu)")
collab = st.checkbox("Collab với đội khác (chia fan base, tăng reach)")
extra_mentor = st.checkbox("Thuê thêm mentor ngoài 30h (500k/giờ, giả định 10 giờ = 5 triệu)")

# ============================================
# ADMIN CONTROL – CORY CAN THIỆP
# ============================================

st.subheader("Admin Control – Cory")

cory_boost = st.slider("Tăng nhận diện (Admin Boost)", 0.0, 0.5, 0.0)
cory_trust_boost = st.slider("Tăng độ tin tưởng thuật toán", 0.0, 0.3, 0.0)

# ============================================
# SIMULATION
# ============================================

if st.button("🚀 Chạy mô phỏng 60 ngày"):

    fame = FAME_LEVELS[fame_label]
    trust = 0.3 + cory_trust_boost
    capital = INITIAL_CAPITAL

    # Chi phí bổ sung
    if minishow:
        capital -= 15_000_000
        fame += 0.1
        trust += 0.05

    if extra_mentor:
        capital -= 5_000_000
        narrative += 0.05
        technical += 0.05

    if collab:
        fame += 0.15
        trust += 0.05

    fame += cory_boost

    history = []
    sponsor_unlocked = False

    for day in range(DAYS):

        total_views = 0
        total_watch_time = 0
        total_revenue = 0

        for seg_name, seg in GENRES[genre]["segments"].items():

            impressions = seg["size"] * trust * (1 + fame)

            ctr = seg["ctr_base"] + 0.02 * visual + 0.01 * fame
            retention = seg["retention_base"] + 0.2 * narrative + 0.1 * emotion

            ctr *= np.random.normal(1, 0.03)
            retention *= np.random.normal(1, 0.03)

            views = impressions * ctr
            watch_time = views * retention

            streaming_revenue = views * 500

            merch_revenue = views * (0.02 * originality) * 100_000

            total_views += views
            total_watch_time += watch_time
            total_revenue += streaming_revenue + merch_revenue

        avg_retention = total_watch_time / (total_views + 1)

        if not sponsor_unlocked and avg_retention > GENRES[genre]["sponsor_threshold"]:
            sponsor_unlocked = True
            sponsor_money = 20_000_000
            total_revenue += sponsor_money

        capital += total_revenue

        performance_score = (avg_retention + market_fit) / 2
        trust += 0.015 * (performance_score - 0.5)
        trust = max(0.1, min(1.2, trust))

        fame += 0.01 * performance_score
        fame = min(1.5, fame)

        history.append({
            "Ngày": day + 1,
            "Lượt xem": total_views,
            "Doanh thu": total_revenue,
            "Vốn tích lũy": capital
        })

    df = pd.DataFrame(history)

    st.subheader("📈 Diễn biến 60 ngày")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ngày"], y=df["Lượt xem"], name="Lượt xem"))
    fig.add_trace(go.Scatter(x=df["Ngày"], y=df["Doanh thu"], name="Doanh thu"))
    fig.add_trace(go.Scatter(x=df["Ngày"], y=df["Vốn tích lũy"], name="Vốn tích lũy"))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Vốn cuối cùng", f"{int(capital):,} VND")

    # Monte Carlo Risk
    st.subheader("📉 Phân tích rủi ro (Monte Carlo 500 lần)")

    outcomes = []

    for _ in range(500):
        sim_cap = INITIAL_CAPITAL
        sim_trust = 0.3
        sim_fame = FAME_LEVELS[fame_label]

        for day in range(DAYS):
            sim_views = 100000 * sim_trust * (1 + sim_fame)
            sim_revenue = sim_views * (0.4 + 0.3 * narrative) * 500
            sim_cap += sim_revenue
            sim_trust += 0.01 * (market_fit - 0.5)
            sim_fame += 0.01 * (narrative - 0.5)

        outcomes.append(sim_cap)

    prob_success = np.mean(np.array(outcomes) > 120_000_000)

    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=outcomes))
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.metric("Xác suất đạt >120 triệu", f"{round(prob_success*100,2)} %")
