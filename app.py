import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

# ==================================================
# INITIALIZATION (SAFE & CLEAN)
# ==================================================

def init_state():
    st.session_state.phase = "pre"
    st.session_state.day = 1
    st.session_state.cash = 100_000_000

    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.sentiment = 0.5
    st.session_state.fatigue = 0.0

    st.session_state.total_revenue_pre = 0
    st.session_state.action_points = 3
    st.session_state.chat_log = []
    st.session_state.mentor_hours_used = 0

if "phase" not in st.session_state:
    init_state()

# ==================================================
# HEADER
# ==================================================

st.title("🎬 AMA Industry Simulation – 14 Day Challenge")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("⭐ Fame", round(st.session_state.fame,2))
col3.metric("🤝 Trust", round(st.session_state.trust,2))
col4.metric("❤️ Sentiment", round(st.session_state.sentiment,2))

st.progress(st.session_state.day / 14)

st.divider()

# ==================================================
# PHASE 1 – 14 DAYS (MULTI ACTION)
# ==================================================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day} / 14")
    st.write(f"🎯 Action còn lại: {st.session_state.action_points}")

    activity = st.selectbox("Chọn hoạt động", [
        "Minishow (15M)",
        "Chạy Ads (10M)",
        "Chạy Ads lớn (20M)",
        "Thuê Mentor (500k/giờ)",
        "Tham khảo chuyên gia thị trường (1M)",
        "Luyện tập"
    ])

    mentor_hours = 0
    if activity == "Thuê Mentor (500k/giờ)":
        mentor_hours = st.slider("Số giờ mentor",1,5,1)

    if st.button("🎯 Thực hiện"):

        if st.session_state.action_points <= 0:
            st.warning("Hết lượt hành động hôm nay.")
        else:

            effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

            # ================= MINISHOW =================
            if activity == "Minishow (15M)":
                st.session_state.cash -= 15_000_000
                success = random.random() < st.session_state.fame

                if success:
                    revenue = 20_000_000
                    st.session_state.cash += revenue
                    st.session_state.total_revenue_pre += revenue
                    effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                    st.session_state.chat_log.append("🎉 Minishow thành công!")
                else:
                    effect = {"trust":-0.1,"sentiment":-0.15,"fatigue":0.1}
                    st.session_state.chat_log.append("⚠️ Minishow thất bại.")

            # ================= ADS NHẸ =================
            elif activity == "Chạy Ads (10M)":
                st.session_state.cash -= 10_000_000
                effect = {"fame":0.05,"sentiment":0.03,"fatigue":0.05}
                st.session_state.chat_log.append("📢 Ads giúp tăng nhận diện.")

            # ================= ADS LỚN =================
            elif activity == "Chạy Ads lớn (20M)":
                st.session_state.cash -= 20_000_000
                effect = {"fame":0.15,"trust":-0.1,"sentiment":-0.1,"fatigue":0.2}
                st.session_state.chat_log.append("⚠️ Ads quá đà gây phản tác dụng.")

            # ================= MENTOR =================
            elif activity == "Thuê Mentor (500k/giờ)":
                cost = mentor_hours * 500_000
                st.session_state.cash -= cost
                st.session_state.mentor_hours_used += mentor_hours

                effect = {
                    "trust":0.03*mentor_hours,
                    "sentiment":0.05*mentor_hours,
                    "fatigue":0.01*mentor_hours
                }

                st.session_state.chat_log.append(
                    f"👨‍🏫 Mentor hỗ trợ {mentor_hours} giờ."
                )

            # ================= CONSULT =================
            elif activity == "Tham khảo chuyên gia thị trường (1M)":
                st.session_state.cash -= 1_000_000
                insight = random.random()

                if insight > 0.5:
                    effect = {"fame":0.05,"trust":0.05}
                    st.session_state.chat_log.append("📊 Insight hữu ích.")
                else:
                    effect = {"trust":-0.02}
                    st.session_state.chat_log.append("🤔 Insight chưa rõ.")

            # ================= PRACTICE =================
            elif activity == "Luyện tập":
                effect = {"trust":0.02,"sentiment":0.04,"fatigue":-0.05}
                st.session_state.chat_log.append("🎵 Luyện tập hiệu quả.")

            # UPDATE STATE
            for key in effect:
                st.session_state[key] = max(
                    0,
                    min(1, st.session_state[key] + effect[key])
                )

            st.session_state.action_points -= 1

    # ================= CHAT LOG =================

    st.divider()
    st.subheader("💬 Nhật ký đội")

    for msg in reversed(st.session_state.chat_log[-8:]):
        st.write(msg)

    # ================= END DAY =================

    if st.session_state.action_points == 0:
        if st.button("🌙 Kết thúc ngày"):

            st.session_state.day += 1
            st.session_state.action_points = 3

            st.session_state.fatigue = max(
                0,
                st.session_state.fatigue - 0.05
            )

            if st.session_state.day > 14:
                st.session_state.phase = "release"

            st.rerun()

# ==================================================
# PHASE 2 – RELEASE & JUDGE
# ==================================================

if st.session_state.phase == "release":

    st.subheader("🎬 Release MV – Giám khảo chấm điểm")

    narrative = st.slider("Câu chuyện",0.0,1.0,0.7)
    visual = st.slider("Hình ảnh",0.0,1.0,0.7)
    emotion = st.slider("Cảm xúc",0.0,1.0,0.7)

    if st.button("🚀 Ra mắt MV"):

        st.session_state.quality = (narrative + visual + emotion)/3
        st.session_state.phase = "market"
        st.rerun()

# ==================================================
# PHASE 3 – MARKET SIMULATION (REALISTIC VN)
# ==================================================

if st.session_state.phase == "market":

    st.subheader("📈 Mô phỏng thị trường 60 ngày")

    quality = st.session_state.quality
    capital = st.session_state.cash

    audiences = {
        "Gen Z": {"size": 2_000_000,"sensitivity":0.6},
        "Mainstream": {"size":1_800_000,"sensitivity":0.5},
        "Rap/Underground":{"size":1_200_000,"sensitivity":0.7}
    }

    results = []

    for day in range(60):

        total_views = 0
        total_revenue = 0

        for group,data in audiences.items():

            match_score = (
                0.4*quality +
                0.3*st.session_state.fame +
                0.2*st.session_state.sentiment -
                0.1*st.session_state.fatigue
            )

            match_score = max(0,min(1,match_score))

            attention = data["size"] * 0.01 * match_score
            ctr = 0.05 * data["sensitivity"] * quality
            views = attention * ctr

            revenue_stream = views * 12  # realistic VN RPM
            merch_revenue = views * 0.01 * 80_000 * st.session_state.sentiment

            total_views += views
            total_revenue += revenue_stream + merch_revenue

        capital += total_revenue

        results.append({
            "day":day,
            "views":total_views,
            "revenue":total_revenue,
            "capital":capital
        })

    df = pd.DataFrame(results)

    col1,col2 = st.columns(2)

    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df["day"],y=df["views"]))
        fig1.update_layout(template="plotly_dark",title="Lượt xem")
        st.plotly_chart(fig1,use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df["day"],y=df["revenue"]))
        fig2.update_layout(template="plotly_dark",title="Doanh thu")
        st.plotly_chart(fig2,use_container_width=True)

    with col2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df["day"],y=df["capital"]))
        fig3.update_layout(template="plotly_dark",title="Vốn tích lũy")
        st.plotly_chart(fig3,use_container_width=True)

    st.metric("💰 Vốn cuối 60 ngày",f"{int(capital):,} VND")

    # ================= PASS / FAIL =================

    fame_ok = st.session_state.fame > 0.9
    trust_ok = st.session_state.trust > 0.8
    sentiment_ok = st.session_state.sentiment > 0.8
    revenue_ok = st.session_state.total_revenue_pre >= 500_000_000

    st.divider()
    st.subheader("🏁 Kết quả cuối")

    if fame_ok and trust_ok and sentiment_ok and revenue_ok:
        st.success("🎉 ĐỘI VƯỢT QUA MÔ PHỎNG!")
    else:
        st.error("❌ ĐỘI CHƯA ĐẠT YÊU CẦU.")
