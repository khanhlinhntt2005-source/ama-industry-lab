import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide", page_title="Hệ thống Nghệ thuật Mô phỏng AMA")

# ==================================================
# INITIALIZATION
# ==================================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.phase = "pre"
    st.session_state.day = 0
    st.session_state.cash = 100_000_000
    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.sentiment = 0.5
    st.session_state.fatigue = 0.0
    st.session_state.action_done = False
    st.session_state.history_pre = []
    st.session_state.history_post = []

# ==================================================
# HEADER
# ==================================================

st.title("Hệ thống Nghệ thuật Mô phỏng AMA - Block sản xuất MV")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("⭐ Danh tiếng", round(st.session_state.fame,2))
col3.metric("🤝 Độ tin cậy", round(st.session_state.trust,2))
col4.metric("❤️ Sentiment", round(st.session_state.sentiment,2))

st.progress(st.session_state.day / 14 if st.session_state.phase=="pre" else 1.0)

st.divider()

# ==================================================
# PHASE 1 – PRE RELEASE (14 DAYS)
# ==================================================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day + 1} / 14")

    if not st.session_state.action_done:

        activity = st.selectbox("Chọn hoạt động hôm nay", [
            "Minishow (15M)",
            "Chạy Ads (10M)",
            "Chạy Ads Số lượng lớn (20M)",
            "Collab",
            "Thuê Mentor (5M)",
            "Luyện Tập",
            "Scandal PR - Các học sinh sẽ bốc thăm ngẫu nhiên 1 ngày mà scandal bắt buộc xảy ra"
        ])

        if st.button("🎯 Thực hiện hành động hôm nay"):

            effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

            # ------------------------
            # MINISHOW
            # ------------------------
            if activity == "Minishow (15M)":
                st.session_state.cash -= 15_000_000
                ticket_success = random.random() < st.session_state.fame

                if ticket_success:
                    revenue = 17_500_000
                    st.session_state.cash += revenue
                    effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                    st.success(f"Minishow thành công! Thu về {revenue:,} VND")
                else:
                    effect = {"fame":0.05,"trust":-0.05,"sentiment":-0.1,"fatigue":0.1}
                    st.warning("Minishow thất bại. Bán vé kém!")

            # ------------------------
            # ADS NHẸ
            # ------------------------
            elif activity == "Chạy Ads (10M)":
                st.session_state.cash -= 10_000_000
                effect = {"fame":0.05,"trust":0.05,"sentiment":0.02,"fatigue":0.05}

            # ------------------------
            # ADS NẶNG (OVEREXPOSURE)
            # ------------------------
            elif activity == "Chạy Ads Số lượng lớn (20M)":
                st.session_state.cash -= 20_000_000
                effect = {"fame":0.12,"trust":-0.1,"sentiment":-0.15,"fatigue":0.2}

            # ------------------------
            # COLLAB
            # ------------------------
            elif activity == "Collab":
                overlap = random.random()
                if overlap > 0.5:
                    effect = {"fame":0.15,"trust":0.08,"sentiment":0.05,"fatigue":0.1}
                    st.success("Collab phù hợp audience!")
                else:
                    effect = {"fame":0.1,"trust":-0.05,"sentiment":-0.1,"fatigue":0.1}
                    st.warning("Collab không đúng phân khúc.")

            # ------------------------
            # MENTOR
            # ------------------------
            elif activity == "Thuê Mentor (5M)":
                st.session_state.cash -= 5_000_000
                effect = {"fame":0.02,"trust":0.03,"sentiment":0.1,"fatigue":0.02}

            # ------------------------
            # SCANDAL
            # ------------------------
            elif activity == "Scandal PR":
                effect = {"fame":0.2,"trust":-0.2,"sentiment":-0.3,"fatigue":0.2}
                st.error("Scandal xảy ra! Danh tiếng tăng nhưng mức độ đáng tin cậy giảm mạnh.")

            # ------------------------
            # LUYỆN TẬP
            # ------------------------
            else:
                effect = {"fame":0.02,"trust":0.02,"sentiment":0.05,"fatigue":-0.1}

            # UPDATE STATE
            for key in effect:
                setattr(
                    st.session_state,
                    key,
                    max(0, getattr(st.session_state, key) + effect[key])
                )

            st.session_state.action_done = True

    else:

        st.info("Bạn đã hoàn thành hành động hôm nay.")

        if st.button("🌙 Kết thúc ngày"):

            st.session_state.day += 1

            st.session_state.history_pre.append({
                "day": st.session_state.day,
                "cash": st.session_state.cash,
                "fame": st.session_state.fame,
                "trust": st.session_state.trust,
                "sentiment": st.session_state.sentiment,
                "fatigue": st.session_state.fatigue
            })

            st.session_state.action_done = False

            if st.session_state.day >= 14:
                st.session_state.phase = "rating"

            st.rerun()

# ==================================================
# PRE ANALYTICS
# ==================================================

if len(st.session_state.history_pre) > 0:
    df_pre = pd.DataFrame(st.session_state.history_pre)

    st.subheader("📊 Phân tích giai đoạn chuẩn bị")

    colA, colB = st.columns(2)

    with colA:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_pre["day"], y=df_pre["cash"], mode="lines+markers"))
        fig1.update_layout(title="Vốn theo ngày", template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df_pre["day"], y=df_pre["trust"]))
        fig2.update_layout(title="Mức độ đáng tin cậy theo ngày", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    with colB:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_pre["day"],
            y=df_pre["fame"],
            fill='tozeroy'
        ))
        fig3.update_layout(title="Tăng trưởng Danh tiếng", template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=st.session_state.trust,
            gauge={'axis': {'range': [0,1]}}
        ))
        fig4.update_layout(title="Mức độ tin cậy hiện tại", template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# PHASE 2 – RATING
# ==================================================

if st.session_state.phase == "rating":

    st.subheader("🏁 Nhập điểm giám khảo")

    narrative = st.slider("Câu chuyện mang bản sắc cá nhân",0.0,1.0,0.7)
    visual = st.slider("Hình ảnh",0.0,1.0,0.7)
    emotion = st.slider("Cảm xúc",0.0,1.0,0.7)

    if st.button("🚀 Ra mắt sản phẩm"):

        st.session_state.rating = {
            "narrative": narrative,
            "visual": visual,
            "emotion": emotion
        }

        st.session_state.phase = "post"
        st.rerun()

# ==================================================
# PHASE 3 – POST RELEASE (60 DAYS – WEIGHTED & BRUTAL)
# ==================================================

if st.session_state.phase == "post":

    st.subheader("📈 Mô phỏng thị trường 60 ngày (Weighted Reality Engine)")

    rating = st.session_state.rating
    capital = st.session_state.cash

    # -------------------------------
    # 1️⃣ TÍNH CHẤT LƯỢNG CHUYÊN MÔN (30%)
    # -------------------------------
    quality_score = (
        rating["narrative"] +
        rating["visual"] +
        rating["emotion"]
    ) / 3

    # -------------------------------
    # 2️⃣ MARKET SUCCESS SCORE (0–1)
    # -------------------------------
    success_score = (
        0.30 * quality_score +
        0.20 * st.session_state.fame +
        0.20 * st.session_state.trust +
        0.20 * st.session_state.sentiment -
        0.20 * st.session_state.fatigue
    )

    # -------------------------------
    # 3️⃣ PENALTY LOGIC (NGHỊCH NGU)
    # -------------------------------

    if st.session_state.fatigue > 0.7:
        success_score -= 0.2

    if st.session_state.trust < 0.2:
        success_score -= 0.25

    if st.session_state.cash < 20_000_000:
        success_score -= 0.15

    success_score = max(0, min(1, success_score))

    failure_probability = 1 - success_score

    # Nếu hệ thống đánh giá thấp → tối thiểu 50% fail
    if success_score < 0.5:
        failure_probability = max(failure_probability, 0.5)

    is_failure = random.random() < failure_probability

    st.metric("🔥 Market Success Score", round(success_score,2))
    st.metric("💣 Xác suất thất bại", round(failure_probability,2))

    results = []

    # -------------------------------
    # 4️⃣ SIMULATE 60 DAYS
    # -------------------------------

    for day in range(60):

        # Volatility thật
        base_fluctuation = np.random.normal(1, 0.15)

        if is_failure:
            # Case thất bại → market lạnh
            attention_multiplier = np.random.normal(0.6, 0.2)
        else:
            # Case thành công → market ấm
            attention_multiplier = np.random.normal(1.3, 0.15)

        attention = (
            200_000 *
            (1 + st.session_state.fame) *
            attention_multiplier *
            base_fluctuation
        )

        # CTR phụ thuộc visual + sentiment
        ctr = (
            0.03 +
            0.02 * rating["visual"] +
            0.01 * st.session_state.sentiment
        )

        # Retention phụ thuộc narrative + emotion + trust
        retention = (
            0.4 +
            0.3 * rating["narrative"] +
            0.2 * rating["emotion"] +
            0.1 * st.session_state.trust
        )

        retention = max(0, min(1, retention))

        views = max(0, attention * ctr)
        engagement = views * retention

        # Doanh thu streaming
        streaming_revenue = views * 500

        # Merch phụ thuộc sentiment
        merch_revenue = engagement * 0.02 * 100_000 * st.session_state.sentiment

        revenue = streaming_revenue + merch_revenue

        capital += revenue

        results.append({
            "day": day,
            "capital": capital,
            "views": views,
            "retention": retention,
            "revenue": revenue
        })

    df = pd.DataFrame(results)

    # -------------------------------
    # 5️⃣ GRAPHS
    # -------------------------------

    col1, col2 = st.columns(2)

    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["day"],
            y=df["capital"],
            mode="lines",
            line=dict(width=3)
        ))
        fig1.update_layout(
            title="Tăng trưởng vốn 60 ngày",
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df["day"],
            y=df["revenue"]
        ))
        fig2.update_layout(
            title="Doanh thu theo ngày",
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df["day"],
            y=df["views"],
            fill='tozeroy'
        ))
        fig3.update_layout(
            title="Lượt xem",
            template="plotly_dark"
        )
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=df["day"],
            y=df["retention"]
        ))
        fig4.update_layout(
            title="Retention Rate",
            template="plotly_dark"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------
    # 6️⃣ FINAL RESULT
    # -------------------------------

    st.metric("💰 Vốn cuối cùng", f"{int(capital):,} VND")

    if capital < 120_000_000:
        st.error("❌ Thất bại thương mại. Sản phẩm không đạt ROI yêu cầu.")
    else:
        st.success("🏆 Thành công thương mại! ROI đạt yêu cầu.")
