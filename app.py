import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide", page_title="AMA Industry Simulation Full")

# ============================================
# INITIALIZATION
# ============================================

if "phase" not in st.session_state:
    st.session_state.phase = "pre"
    st.session_state.day = 0
    st.session_state.cash = 100_000_000
    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.sentiment = 0.5
    st.session_state.fatigue = 0.0
    
    st.session_state.history_pre = []
    st.session_state.history_post = []

# ============================================
# HEADER
# ============================================

st.title("🎬 AMA Industry Simulation – Full System")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("Fame", round(st.session_state.fame,2))
col3.metric("Trust", round(st.session_state.trust,2))
col4.metric("Sentiment", round(st.session_state.sentiment,2))

st.write("Phase:", st.session_state.phase.upper())

st.divider()

# ============================================
# PHASE 1 – PRE RELEASE LOOP
# ============================================

if st.session_state.phase == "pre":

    st.subheader(f"📆 Ngày {st.session_state.day + 1} / 14")

    activity = st.selectbox("Chọn hoạt động", [
        "Minishow (15M)",
        "Chạy Ads (10M)",
        "Spam Ads (20M)",
        "Collab",
        "Thuê Mentor (5M)",
        "Nghỉ ngơi",
        "Scandal PR"
    ])

    if st.button("Thực hiện"):

        effect = {"fame":0,"trust":0,"sentiment":0,"fatigue":0}

        if activity == "Minishow (15M)":
            st.session_state.cash -= 15_000_000
            ticket_success = random.random() < st.session_state.fame
            if ticket_success:
                effect = {"fame":0.1,"trust":0.05,"sentiment":0.1,"fatigue":0.1}
                st.success("Minishow thành công!")
            else:
                effect = {"fame":0.05,"trust":-0.05,"sentiment":-0.1,"fatigue":0.1}
                st.warning("Minishow bán vé kém!")

        elif activity == "Chạy Ads (10M)":
            st.session_state.cash -= 10_000_000
            effect = {"fame":0.05,"trust":0.05,"sentiment":0.02,"fatigue":0.05}

        elif activity == "Spam Ads (20M)":
            st.session_state.cash -= 20_000_000
            effect = {"fame":0.1,"trust":-0.1,"sentiment":-0.15,"fatigue":0.15}

        elif activity == "Collab":
            overlap = random.random()
            if overlap > 0.5:
                effect = {"fame":0.15,"trust":0.08,"sentiment":0.05,"fatigue":0.1}
            else:
                effect = {"fame":0.1,"trust":-0.05,"sentiment":-0.1,"fatigue":0.1}

        elif activity == "Thuê Mentor (5M)":
            st.session_state.cash -= 5_000_000
            effect = {"fame":0.02,"trust":0.03,"sentiment":0.1,"fatigue":0.02}

        elif activity == "Scandal PR":
            effect = {"fame":0.2,"trust":-0.2,"sentiment":-0.3,"fatigue":0.2}

        else:
            effect = {"fame":0,"trust":0.02,"sentiment":0.1,"fatigue":-0.1}

        # Update state
        for key in effect:
            setattr(st.session_state, key,
                    max(0, getattr(st.session_state, key) + effect[key]))

        st.session_state.day += 1

        st.session_state.history_pre.append({
            "day": st.session_state.day,
            "cash": st.session_state.cash,
            "fame": st.session_state.fame,
            "trust": st.session_state.trust,
            "sentiment": st.session_state.sentiment,
            "fatigue": st.session_state.fatigue
        })

        if st.session_state.day >= 14:
            st.session_state.phase = "rating"

# ============================================
# PHASE 2 – RATING
# ============================================

if st.session_state.phase == "rating":

    st.subheader("🏁 Nhập điểm giám khảo")

    narrative = st.slider("Narrative",0.0,1.0,0.7)
    visual = st.slider("Visual",0.0,1.0,0.7)
    emotion = st.slider("Emotion",0.0,1.0,0.7)
    technical = st.slider("Technical",0.0,1.0,0.7)
    market_fit = st.slider("Market Fit",0.0,1.0,0.7)
    originality = st.slider("Originality",0.0,1.0,0.7)

    if st.button("Chuyển sang mô phỏng thị trường"):
        st.session_state.rating = {
            "narrative": narrative,
            "visual": visual,
            "emotion": emotion,
            "technical": technical,
            "market_fit": market_fit,
            "originality": originality
        }
        st.session_state.phase = "post"

# ============================================
# PHASE 3 – POST RELEASE LOOP (60 DAYS)
# ============================================

if st.session_state.phase == "post":

    st.subheader("📈 Mô phỏng 60 ngày thị trường")

    rating = st.session_state.rating
    capital = st.session_state.cash
    trust = st.session_state.trust
    fame = st.session_state.fame
    sentiment = st.session_state.sentiment
    fatigue = st.session_state.fatigue

    sponsor_unlocked = False

    for day in range(60):

        fluctuation = np.random.normal(1,0.08)
        decay = 0.98

        attention = 200_000 * trust * (1+fame) * fluctuation * (1-fatigue)
        ctr = 0.04 + 0.02*rating["visual"]
        retention = 0.5 + 0.3*rating["narrative"] + 0.2*rating["emotion"]

        views = attention * ctr
        engagement = views * retention
        streaming = views * 500
        merch = engagement * 0.02 * 100_000

        sponsor = 0
        if not sponsor_unlocked and retention > 0.7 and sentiment > 0.6:
            sponsor_unlocked = True
            sponsor = 20_000_000

        revenue = streaming + merch + sponsor
        capital += revenue

        trust *= decay
        fame *= decay
        fatigue = min(0.5, fatigue + 0.01)

        st.session_state.history_post.append({
            "day": day,
            "capital": capital,
            "views": views,
            "retention": retention,
            "streaming": streaming,
            "merch": merch,
            "sponsor": sponsor,
            "trust": trust,
            "fame": fame,
            "fatigue": fatigue
        })

    df = pd.DataFrame(st.session_state.history_post)

    # ============================================
    # VISUALIZATION (12 GRAPHS)
    # ============================================

    charts = {
        "Capital": df["capital"],
        "Views": df["views"],
        "Retention": df["retention"],
        "Streaming": df["streaming"],
        "Merch": df["merch"],
        "Sponsor": df["sponsor"],
        "Trust": df["trust"],
        "Fame": df["fame"],
        "Fatigue": df["fatigue"]
    }

    for title, data in charts.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data, mode="lines"))
        fig.update_layout(title=title, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    st.metric("Vốn cuối cùng", f"{int(capital):,} VND")

    # Monte Carlo
    outcomes = []
    for _ in range(300):
        sim = capital * np.random.normal(1,0.1)
        outcomes.append(sim)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=outcomes))
    fig.update_layout(title="Monte Carlo Risk Distribution", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
# ===============================
# PRE-PHASE ANALYTICS
# ===============================

if len(st.session_state.history_pre) > 0:

    df_pre = pd.DataFrame(st.session_state.history_pre)

    st.subheader("📊 Phân tích giai đoạn chuẩn bị")

    # 1️⃣ Line – Cash
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_pre["day"], y=df_pre["cash"], mode="lines+markers"))
    fig1.update_layout(title="Vốn theo ngày", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Area – Fame
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_pre["day"],
        y=df_pre["fame"],
        fill='tozeroy'
    ))
    fig2.update_layout(title="Tăng trưởng Fame", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Bar – Trust
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=df_pre["day"], y=df_pre["trust"]))
    fig3.update_layout(title="Trust theo ngày", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Scatter – Sentiment vs Fame
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df_pre["fame"],
        y=df_pre["sentiment"],
        mode="markers",
        marker=dict(size=15)
    ))
    fig4.update_layout(title="Fame vs Sentiment", template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ Heatmap – Fatigue
    fig5 = go.Figure(data=go.Heatmap(
        z=[df_pre["fatigue"]],
        x=df_pre["day"],
        y=["Fatigue"],
        colorscale="Reds"
    ))
    fig5.update_layout(title="Heatmap Fatigue", template="plotly_dark")
    st.plotly_chart(fig5, use_container_width=True)

    # 6️⃣ Box Plot – Biến động Sentiment
    fig6 = go.Figure()
    fig6.add_trace(go.Box(y=df_pre["sentiment"]))
    fig6.update_layout(title="Biến động Sentiment", template="plotly_dark")
    st.plotly_chart(fig6, use_container_width=True)

    # 7️⃣ Gauge – Trust
    fig7 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.trust,
        gauge={'axis': {'range': [0, 1]}}
    ))
    fig7.update_layout(title="Mức độ tin tưởng hiện tại", template="plotly_dark")
    st.plotly_chart(fig7, use_container_width=True)

    # 8️⃣ Bubble – Fame vs Cash
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(
        x=df_pre["fame"],
        y=df_pre["cash"],
        mode="markers",
        marker=dict(size=df_pre["sentiment"]*40)
    ))
    fig8.update_layout(title="Fame vs Vốn (size = Sentiment)", template="plotly_dark")
    st.plotly_chart(fig8, use_container_width=True)

    # 9️⃣ Histogram – Fame distribution
    fig9 = go.Figure()
    fig9.add_trace(go.Histogram(x=df_pre["fame"]))
    fig9.update_layout(title="Phân phối Fame", template="plotly_dark")
    st.plotly_chart(fig9, use_container_width=True)

    # 🔟 Radar – Tổng trạng thái hiện tại
    radar_values = [
        st.session_state.fame,
        st.session_state.trust,
        st.session_state.sentiment,
        1 - st.session_state.fatigue
    ]

    fig10 = go.Figure()
    fig10.add_trace(go.Scatterpolar(
        r=radar_values,
        theta=["Fame", "Trust", "Sentiment", "Energy"],
        fill='toself'
    ))
    fig10.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        title="Radar trạng thái đội",
        template="plotly_dark"
    )
    st.plotly_chart(fig10, use_container_width=True)
