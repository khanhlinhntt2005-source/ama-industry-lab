import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

# ======================================================
# INITIALIZE STATE
# ======================================================

def init():
    st.session_state.phase = "pre"
    st.session_state.day = 1
    st.session_state.cash = 100_000_000

    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.sentiment = 0.5
    st.session_state.fatigue = 0.0

    st.session_state.total_revenue_pre = 0
    st.session_state.action_points = 3
    st.session_state.chat = []
    st.session_state.history = []

if "phase" not in st.session_state:
    init()

# ======================================================
# HEADER
# ======================================================

st.title("🎬 AMA Industry Simulation – 14 Ngày Sống Còn")

col1,col2,col3,col4 = st.columns(4)

col1.metric("💰 Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("⭐ Fame", round(st.session_state.fame,2))
col3.metric("🤝 Trust", round(st.session_state.trust,2))
col4.metric("❤️ Sentiment", round(st.session_state.sentiment,2))

progress = min(1.0, max(0.0, (st.session_state.day-1) / 14))
st.progress(progress)

st.divider()

# ======================================================
# PHASE 1 – 14 DAYS BUILDING
# ======================================================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day} / 14")
    st.write(f"🎯 Action còn lại: {st.session_state.action_points}")

    activity = st.selectbox("Chọn hoạt động", [
        "Minishow (15M)",
        "Chạy Ads (10M)",
        "Chạy Ads lớn (20M)",
        "Thuê Mentor (500k/giờ)",
        "Tham khảo chuyên gia (1M)",
        "Luyện tập"
    ])

    mentor_hours = 1
    if activity == "Thuê Mentor (500k/giờ)":
        mentor_hours = st.slider("Số giờ mentor",1,5,1)

    colA,colB = st.columns(2)

    # ================= THỰC HIỆN =================

    if colA.button("🎯 Thực hiện"):

        if st.session_state.action_points <= 0:
            st.warning("Hết lượt hành động hôm nay.")
            st.stop()

        effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

        # ---------- MINISHOW ----------
        if activity == "Minishow (15M)":

            if st.session_state.cash < 15_000_000:
                st.error("Không đủ tiền.")
                st.stop()

            st.session_state.cash -= 15_000_000

            success_rate = (
                0.4*st.session_state.fame +
                0.3*st.session_state.sentiment -
                0.2*st.session_state.fatigue
            )

            success = random.random() < success_rate

            if success:
                revenue = random.randint(18_000_000,25_000_000)
                st.session_state.cash += revenue
                st.session_state.total_revenue_pre += revenue
                effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                st.session_state.chat.append(f"🎉 Minishow thắng lớn +{revenue:,}")
            else:
                effect = {"trust":-0.1,"sentiment":-0.15,"fatigue":0.15}
                st.session_state.chat.append("⚠️ Minishow flop.")

        # ---------- ADS ----------
        elif activity == "Chạy Ads (10M)":
            st.session_state.cash -= 10_000_000
            effect = {"fame":0.05,"sentiment":0.03,"fatigue":0.05}
            st.session_state.chat.append("📢 Ads tăng nhận diện.")

        elif activity == "Chạy Ads lớn (20M)":
            st.session_state.cash -= 20_000_000
            effect = {"fame":0.15,"trust":-0.1,"sentiment":-0.1,"fatigue":0.2}
            st.session_state.chat.append("⚠️ Overexposure.")

        # ---------- MENTOR ----------
        elif activity == "Thuê Mentor (500k/giờ)":
            cost = mentor_hours * 500_000
            st.session_state.cash -= cost
            effect = {
                "trust":0.03*mentor_hours,
                "sentiment":0.05*mentor_hours,
                "fatigue":0.02*mentor_hours
            }
            st.session_state.chat.append(f"👨‍🏫 Mentor {mentor_hours} giờ.")

        # ---------- CONSULT ----------
        elif activity == "Tham khảo chuyên gia (1M)":
            st.session_state.cash -= 1_000_000
            insight = random.random()
            if insight > 0.5:
                effect = {"fame":0.05,"trust":0.05}
                st.session_state.chat.append("📊 Insight tốt.")
            else:
                effect = {"trust":-0.02}
                st.session_state.chat.append("🤔 Insight yếu.")

        # ---------- PRACTICE ----------
        elif activity == "Luyện tập":
            effect = {"trust":0.02,"sentiment":0.04,"fatigue":-0.05}
            st.session_state.chat.append("🎵 Luyện tập ổn.")

        # UPDATE STATS
        for key in effect:
            st.session_state[key] = min(1.0, max(0.0, st.session_state[key] + effect[key]))

        st.session_state.action_points -= 1
        st.rerun()

    # ================= KẾT THÚC NGÀY =================

    if colB.button("🌙 Kết thúc ngày"):

        # Lưu lịch sử
        st.session_state.history.append({
            "day":st.session_state.day,
            "cash":st.session_state.cash,
            "fame":st.session_state.fame,
            "trust":st.session_state.trust,
            "sentiment":st.session_state.sentiment
        })

        # Reset action
        st.session_state.action_points = 3
        st.session_state.fatigue = max(0, st.session_state.fatigue - 0.05)

        # CHUYỂN NGÀY HOẶC PHASE
        if st.session_state.day >= 14:
            st.session_state.phase = "release"
        else:
            st.session_state.day += 1

        st.rerun()

    # ================= CHAT =================

    st.divider()
    st.subheader("💬 Nhật ký đội")
    for msg in reversed(st.session_state.chat[-6:]):
        st.write(msg)

    # ================= GRAPH =================

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)

        col1,col2 = st.columns(2)

        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=df["day"],y=df["cash"]))
            fig1.update_layout(template="plotly_dark",title="Vốn theo ngày")
            st.plotly_chart(fig1,use_container_width=True)

        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df["day"],y=df["fame"]))
            fig2.update_layout(template="plotly_dark",title="Fame theo ngày")
            st.plotly_chart(fig2,use_container_width=True)

# ======================================================
# PHASE 2 – RELEASE MV
# ======================================================

if st.session_state.phase == "release":

    st.subheader("🎬 Chấm điểm MV")

    narrative = st.slider("Câu chuyện",0.0,1.0,0.7)
    visual = st.slider("Hình ảnh",0.0,1.0,0.7)
    emotion = st.slider("Cảm xúc",0.0,1.0,0.7)

    if st.button("🚀 Release MV"):

        st.session_state.quality = (
            0.3*narrative +
            0.3*visual +
            0.4*emotion
        )

        st.session_state.phase = "market"
        st.rerun()

# ======================================================
# PHASE 3 – MARKET 60 DAYS
# ======================================================

if st.session_state.phase == "market":

    st.subheader("📈 Thị trường 60 ngày")

    capital = st.session_state.cash
    quality = st.session_state.quality

    results = []

    for d in range(60):

        fluctuation = np.random.normal(1,0.2)

        base_score = (
            0.3*quality +
            0.3*st.session_state.fame +
            0.2*st.session_state.trust +
            0.2*st.session_state.sentiment
        )

        if random.random() < 0.5:
            base_score *= random.uniform(0.5,0.9)

        views = 500_000 * base_score * fluctuation
        revenue = views * 15

        capital += revenue

        results.append({
            "day":d,
            "capital":capital,
            "views":views
        })

    df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["day"],y=df["capital"]))
    fig.update_layout(template="plotly_dark",title="Vốn tích lũy 60 ngày")
    st.plotly_chart(fig,use_container_width=True)

    st.metric("💰 Vốn cuối cùng",f"{int(capital):,} VND")

    # ================= ĐIỀU KIỆN THẮNG =================

    win = (
        capital >= 500_000_000 and
        st.session_state.fame > 0.9 and
        st.session_state.trust > 0.8 and
        st.session_state.sentiment > 0.8
    )

    if win:
        st.success("🏆 Bạn đã vượt qua mô phỏng!")
    else:
        st.error("❌ Bạn thất bại.")
