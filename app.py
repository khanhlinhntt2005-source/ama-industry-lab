import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

# ============================
# INITIALIZATION
# ============================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.phase = "pre"
    st.session_state.day = 0
    st.session_state.cash = 100_000_000
    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.sentiment = 0.5
    st.session_state.fatigue = 0.0
    st.session_state.total_revenue_pre = 0
    st.session_state.action_done = False

# ============================
# HEADER
# ============================

st.title("🎬 AMA Industry Simulation – 14 Day Challenge")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("⭐ Fame", round(st.session_state.fame,2))
col3.metric("🤝 Trust", round(st.session_state.trust,2))
col4.metric("❤️ Sentiment", round(st.session_state.sentiment,2))

st.progress(st.session_state.day / 14)

st.divider()

# ============================
# PHASE 1 – 14 DAYS (MULTI ACTION)
# ============================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day + 1} / 14")
    st.write(f"🎯 Action còn lại hôm nay: {st.session_state.action_points}")

    activity = st.selectbox("Chọn hoạt động", [
        "Minishow (15M)",
        "Chạy Ads (10M)",
        "Chạy Ads lớn (20M)",
        "Thuê Mentor (500k/giờ)",
        "Tham khảo chuyên gia thị trường (1M)",
        "Luyện tập"
    ])

    # -------------------------
    # MENTOR HOUR INPUT
    # -------------------------

    if activity == "Thuê Mentor (500k/giờ)":
        mentor_hours = st.slider("Chọn số giờ mentor",1,5,1)
    else:
        mentor_hours = 0

    if st.button("🎯 Thực hiện"):

        if st.session_state.action_points <= 0:
            st.warning("Hết lượt hành động hôm nay.")
        else:

            effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

            # ---------------------
            # MINISHOW
            # ---------------------
            if activity == "Minishow (15M)":
                st.session_state.cash -= 15_000_000
                success = random.random() < st.session_state.fame

                if success:
                    revenue = 20_000_000
                    st.session_state.cash += revenue
                    st.session_state.total_revenue_pre += revenue
                    effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                    st.session_state.chat_log.append("🎉 Minishow thành công! Audience phản ứng tốt.")
                else:
                    effect = {"trust":-0.1,"sentiment":-0.15,"fatigue":0.1}
                    st.session_state.chat_log.append("⚠️ Minishow thất bại. Thời điểm chưa phù hợp.")

            # ---------------------
            # ADS
            # ---------------------
            elif activity == "Chạy Ads (10M)":
                st.session_state.cash -= 10_000_000
                effect = {"fame":0.05,"sentiment":0.03,"fatigue":0.05}
                st.session_state.chat_log.append("📢 Ads nhẹ giúp tăng nhận diện.")

            elif activity == "Chạy Ads lớn (20M)":
                st.session_state.cash -= 20_000_000
                effect = {"fame":0.12,"trust":-0.1,"sentiment":-0.1,"fatigue":0.2}
                st.session_state.chat_log.append("⚠️ Ads quá đà. Audience bắt đầu nghi ngờ.")

            # ---------------------
            # MENTOR
            # ---------------------
            elif activity == "Thuê Mentor (500k/giờ)":
                cost = mentor_hours * 500_000
                st.session_state.cash -= cost
                st.session_state.mentor_hours_used += mentor_hours

                effect = {
                    "trust":0.02*mentor_hours,
                    "sentiment":0.05*mentor_hours,
                    "fatigue":0.01*mentor_hours
                }

                st.session_state.chat_log.append(
                    f"👨‍🏫 Mentor hỗ trợ {mentor_hours} giờ. Đội cải thiện cấu trúc bài."
                )

            # ---------------------
            # CONSULT EXPERT
            # ---------------------
            elif activity == "Tham khảo chuyên gia thị trường (1M)":
                st.session_state.cash -= 1_000_000

                insight_quality = random.random()

                if insight_quality > 0.5:
                    effect = {"fame":0.05,"trust":0.05}
                    st.session_state.chat_log.append(
                        "📊 Chuyên gia: Audience Gen Z thích storytelling cá nhân."
                    )
                else:
                    effect = {"trust":-0.02}
                    st.session_state.chat_log.append(
                        "🤔 Insight chưa đủ rõ ràng."
                    )

            # ---------------------
            # PRACTICE
            # ---------------------
            elif activity == "Luyện tập":
                effect = {"trust":0.02,"sentiment":0.04,"fatigue":-0.05}
                st.session_state.chat_log.append(
                    "🎵 Luyện tập giúp đội gắn kết hơn."
                )

            # UPDATE STATE
            for key in effect:
                st.session_state[key] = max(
                    0,
                    st.session_state[key] + effect[key]
                )

            st.session_state.action_points -= 1

    # -------------------------
    # CHATBOX DISPLAY
    # -------------------------

    st.divider()
    st.subheader("💬 Nhật ký đội")

    for msg in reversed(st.session_state.chat_log[-8:]):
        st.write(msg)

    # -------------------------
    # END DAY
    # -------------------------

    if st.session_state.action_points == 0:
        if st.button("🌙 Kết thúc ngày"):
            st.session_state.day += 1
            st.session_state.action_points = 3

            # fatigue decay tự nhiên
            st.session_state.fatigue = max(
                0,
                st.session_state.fatigue - 0.05
            )

            if st.session_state.day >= 14:
                st.session_state.phase = "post"

            st.rerun()

# ============================
# PHASE 2 – RELEASE & MARKET
# ============================

if st.session_state.phase == "post":

    st.subheader("🎬 RELEASE MV & MARKET SIMULATION")

    # ======================
    # 1️⃣ GIÁM KHẢO CHẤM
    # ======================

    narrative = st.slider("Câu chuyện",0.0,1.0,0.7)
    visual = st.slider("Hình ảnh",0.0,1.0,0.7)
    emotion = st.slider("Cảm xúc",0.0,1.0,0.7)

    if st.button("🚀 Release MV"):

        quality = (narrative + visual + emotion)/3

        st.metric("🎯 Điểm chất lượng tổng", round(quality,2))

        # ======================
        # 2️⃣ AUDIENCE SEGMENTS
        # ======================

        audiences = {
            "Gen Z Chill": {
                "size": 2_000_000,
                "sensitivity": 0.6
            },
            "Mainstream Pop": {
                "size": 1_800_000,
                "sensitivity": 0.5
            },
            "Underground/Rap": {
                "size": 1_200_000,
                "sensitivity": 0.7
            }
        }

        capital = st.session_state.cash
        results = []

        for day in range(60):

            total_views = 0
            total_revenue = 0

            for group, data in audiences.items():

                match_score = (
                    0.4*quality +
                    0.3*st.session_state.fame +
                    0.2*st.session_state.sentiment -
                    0.1*st.session_state.fatigue
                )

                match_score = max(0, min(1, match_score))

                daily_attention = data["size"] * 0.01 * match_score

                ctr = 0.05 * data["sensitivity"] * quality
                views = daily_attention * ctr

                # YouTube VN realistic revenue
                revenue_stream = views * 12  # 12 VND per view

                # Merch chỉ 1% fan mua
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

        # ======================
        # 3️⃣ GRAPHS
        # ======================

        col1,col2 = st.columns(2)

        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df["day"],
                y=df["views"],
                mode="lines"
            ))
            fig1.update_layout(
                title="Lượt xem theo ngày",
                template="plotly_dark"
            )
            st.plotly_chart(fig1,use_container_width=True)

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df["day"],
                y=df["revenue"]
            ))
            fig2.update_layout(
                title="Doanh thu theo ngày",
                template="plotly_dark"
            )
            st.plotly_chart(fig2,use_container_width=True)

        with col2:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=df["day"],
                y=df["capital"],
                mode="lines"
            ))
            fig3.update_layout(
                title="Vốn tích lũy",
                template="plotly_dark"
            )
            st.plotly_chart(fig3,use_container_width=True)

        st.metric("💰 Vốn cuối 60 ngày", f"{int(capital):,} VND")

        # ======================
        # 4️⃣ PASS / FAIL
        # ======================

        fame_ok = st.session_state.fame > 0.9
        trust_ok = st.session_state.trust > 0.8
        sentiment_ok = st.session_state.sentiment > 0.8
        revenue_ok = st.session_state.total_revenue_pre >= 500_000_000

        if fame_ok and trust_ok and sentiment_ok and revenue_ok:
            st.success("🎉 ĐỘI ĐẠT CHUẨN TOÀN DIỆN!")
        else:
            st.error("❌ CHƯA ĐẠT YÊU CẦU TOÀN DIỆN")
