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
# PHASE 1 – 14 DAYS
# ============================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day + 1} / 14")

    if not st.session_state.action_done:

        options = [
            "Minishow (15M)",
            "Chạy Ads (10M)",
            "Chạy Ads lớn (20M)",
            "Thuê Mentor (5M)",
            "Luyện Tập"
        ]

        # Unlock Sponsor
        if st.session_state.fame > 0.7:
            options.append("Ký Sponsor (Thu 100M)")

        # Unlock Big Showcase
        if st.session_state.fame > 0.8 and st.session_state.trust > 0.7:
            options.append("Big Showcase (40M)")

        activity = st.selectbox("Chọn hoạt động", options)

        if st.button("🎯 Thực hiện"):

            effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

            # -----------------
            # MINISHOW
            # -----------------
            if activity == "Minishow (15M)":
                st.session_state.cash -= 15_000_000
                success = random.random() < st.session_state.fame

                if success:
                    revenue = 17_500_000
                    st.session_state.cash += revenue
                    st.session_state.total_revenue_pre += revenue
                    effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                    st.success(f"Minishow thành công! +{revenue:,} VND")
                else:
                    effect = {"fame":0.05,"trust":-0.05,"sentiment":-0.1,"fatigue":0.1}
                    st.warning("Minishow thất bại")

            # -----------------
            # ADS NHẸ
            # -----------------
            elif activity == "Chạy Ads (10M)":
                st.session_state.cash -= 10_000_000
                effect = {"fame":0.05,"trust":0.03,"sentiment":0.02,"fatigue":0.05}

            # -----------------
            # ADS LỚN
            # -----------------
            elif activity == "Chạy Ads lớn (20M)":
                st.session_state.cash -= 20_000_000
                effect = {"fame":0.15,"trust":-0.1,"sentiment":-0.15,"fatigue":0.2}

            # -----------------
            # MENTOR
            # -----------------
            elif activity == "Thuê Mentor (5M)":
                st.session_state.cash -= 5_000_000
                effect = {"fame":0.02,"trust":0.05,"sentiment":0.1,"fatigue":0.02}

            # -----------------
            # LUYỆN TẬP
            # -----------------
            elif activity == "Luyện Tập":
                effect = {"fame":0.02,"trust":0.02,"sentiment":0.05,"fatigue":-0.1}

            # -----------------
            # SPONSOR
            # -----------------
            elif activity == "Ký Sponsor (Thu 100M)":
                revenue = 100_000_000
                st.session_state.cash += revenue
                st.session_state.total_revenue_pre += revenue
                effect = {"trust":0.1,"sentiment":0.05}
                st.success("Ký sponsor thành công! +100M")

            # -----------------
            # BIG SHOWCASE
            # -----------------
            elif activity == "Big Showcase (40M)":
                st.session_state.cash -= 40_000_000
                success = random.random() < st.session_state.fame

                if success:
                    revenue = 200_000_000
                    st.session_state.cash += revenue
                    st.session_state.total_revenue_pre += revenue
                    effect = {"fame":0.2,"trust":0.1,"sentiment":0.15,"fatigue":0.2}
                    st.success("Big Showcase bùng nổ! +200M")
                else:
                    effect = {"trust":-0.2,"sentiment":-0.2,"fatigue":0.3}
                    st.error("Big Showcase thất bại")

            # UPDATE
            for key in effect:
                st.session_state[key] = max(
                    0,
                    st.session_state[key] + effect[key]
                )

            st.session_state.action_done = True

    else:
        if st.button("🌙 Kết thúc ngày"):
            st.session_state.day += 1
            st.session_state.action_done = False

            # FATIGUE NATURAL RECOVERY
            st.session_state.fatigue = max(
                0,
                st.session_state.fatigue - 0.05
            )

            # END OF 14 DAYS
            if st.session_state.day >= 14:

                st.subheader("🏁 KIỂM TRA ĐIỀU KIỆN")

                fame_ok = st.session_state.fame > 0.9
                trust_ok = st.session_state.trust > 0.8
                sentiment_ok = st.session_state.sentiment > 0.8
                revenue_ok = st.session_state.total_revenue_pre >= 500_000_000

                st.write("Fame > 0.9:", fame_ok)
                st.write("Trust > 0.8:", trust_ok)
                st.write("Sentiment > 0.8:", sentiment_ok)
                st.write("Doanh thu ≥ 500M:", revenue_ok)

                st.metric("💰 Tổng doanh thu",
                          f"{int(st.session_state.total_revenue_pre):,} VND")

                if fame_ok and trust_ok and sentiment_ok and revenue_ok:
                    st.success("🎉 VƯỢT MÔ PHỎNG!")
                    st.session_state.phase = "post"
                else:
                    st.error("❌ THẤT BẠI.")
                    st.stop()

            st.rerun()

# ============================
# PHASE 2 – POST SIMULATION
# ============================

if st.session_state.phase == "post":

    st.subheader("📈 Mô phỏng 60 ngày sau ra mắt")

    capital = st.session_state.cash
    results = []

    success_score = (
        0.3 * (st.session_state.fame) +
        0.3 * (st.session_state.trust) +
        0.2 * (st.session_state.sentiment) -
        0.2 * (st.session_state.fatigue)
    )

    success_score = max(0, min(1, success_score))
    fail = random.random() > success_score

    for day in range(60):

        if fail:
            multiplier = np.random.normal(0.7,0.2)
        else:
            multiplier = np.random.normal(1.4,0.2)

        views = 200_000 * multiplier
        revenue = views * 500

        capital += revenue

        results.append({"day":day,"capital":capital})

    df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["day"],y=df["capital"]))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)

    st.metric("💰 Vốn cuối",f"{int(capital):,} VND")
