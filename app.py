import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

# ============================================
# INITIAL STATE
# ============================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.cash = 100_000_000
    st.session_state.fame = 0.2
    st.session_state.trust = 0.3
    st.session_state.fatigue = 0.0
    st.session_state.sentiment = 0.5
    st.session_state.day = 0

    st.session_state.history = {
        "cash": [],
        "fame": [],
        "trust": [],
        "views": [],
        "retention": [],
        "sentiment": [],
        "fatigue": [],
        "merch": [],
        "sponsor": [],
        "engagement": []
    }

# ============================================
# CORE ENGINE
# ============================================

def simulate_day(activity_effect):

    base_market = 200_000
    
    fluctuation = np.random.normal(1, 0.1)
    fatigue_penalty = 1 - st.session_state.fatigue

    impressions = base_market * st.session_state.trust * fluctuation
    ctr = 0.04 + 0.02 * st.session_state.fame
    views = impressions * ctr

    retention = 0.5 + 0.2 * st.session_state.sentiment
    retention *= fatigue_penalty

    engagement = views * retention

    merch = engagement * 0.02 * 100_000
    sponsor = 0

    if engagement > 50000 and st.session_state.sentiment > 0.6:
        sponsor = 10_000_000

    revenue = views * 500 + merch + sponsor

    # Apply activity effect
    st.session_state.fame += activity_effect["fame"]
    st.session_state.trust += activity_effect["trust"]
    st.session_state.sentiment += activity_effect["sentiment"]
    st.session_state.fatigue += activity_effect["fatigue"]

    st.session_state.fatigue = min(0.5, max(0, st.session_state.fatigue))
    st.session_state.sentiment = min(1, max(0, st.session_state.sentiment))
    st.session_state.trust = min(1.5, max(0.1, st.session_state.trust))
    st.session_state.fame = min(2, max(0, st.session_state.fame))

    st.session_state.cash += revenue

    st.session_state.day += 1

    # Save history
    st.session_state.history["cash"].append(st.session_state.cash)
    st.session_state.history["fame"].append(st.session_state.fame)
    st.session_state.history["trust"].append(st.session_state.trust)
    st.session_state.history["views"].append(views)
    st.session_state.history["retention"].append(retention)
    st.session_state.history["sentiment"].append(st.session_state.sentiment)
    st.session_state.history["fatigue"].append(st.session_state.fatigue)
    st.session_state.history["merch"].append(merch)
    st.session_state.history["sponsor"].append(sponsor)
    st.session_state.history["engagement"].append(engagement)


# ============================================
# DASHBOARD
# ============================================

st.title("🎬 AMA Industry Simulation – Loop Model")

col1, col2, col3 = st.columns(3)
col1.metric("Tiền", f"{int(st.session_state.cash):,} VND")
col2.metric("Fame", round(st.session_state.fame,2))
col3.metric("Trust", round(st.session_state.trust,2))

st.write("Ngày:", st.session_state.day)

st.divider()

# ============================================
# ACTIVITY PAGES
# ============================================

activity = st.selectbox("Chọn hoạt động", [
    "Minishow (15M)",
    "Chạy Ads (10M)",
    "Collab (miễn phí)",
    "Thuê Mentor (5M)",
    "Nghỉ ngơi (giảm fatigue)"
])

if st.button("Thực hiện hoạt động"):

    if activity == "Minishow (15M)":
        st.session_state.cash -= 15_000_000
        effect = {"fame":0.1, "trust":0.05, "sentiment":0.1, "fatigue":0.1}

    elif activity == "Chạy Ads (10M)":
        st.session_state.cash -= 10_000_000
        effect = {"fame":0.05, "trust":0.1, "sentiment":0.02, "fatigue":0.05}

    elif activity == "Collab (miễn phí)":
        effect = {"fame":0.15, "trust":0.08, "sentiment":0.05, "fatigue":0.1}

    elif activity == "Thuê Mentor (5M)":
        st.session_state.cash -= 5_000_000
        effect = {"fame":0.02, "trust":0.03, "sentiment":0.1, "fatigue":0.02}

    else:
        effect = {"fame":0, "trust":0, "sentiment":0.05, "fatigue":-0.1}

    simulate_day(effect)

# ============================================
# 10 GRAPHS
# ============================================

if st.session_state.day > 0:

    df = pd.DataFrame(st.session_state.history)

    graphs = [
        ("Tiền", df["cash"]),
        ("Fame", df["fame"]),
        ("Trust", df["trust"]),
        ("Views", df["views"]),
        ("Retention", df["retention"]),
        ("Sentiment", df["sentiment"]),
        ("Fatigue", df["fatigue"]),
        ("Merch Revenue", df["merch"]),
        ("Sponsor Revenue", df["sponsor"]),
        ("Engagement", df["engagement"]),
    ]

    for title, data in graphs:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data, mode="lines+markers"))
        fig.update_layout(title=title, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
