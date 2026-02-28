import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import pandas as pd

st.set_page_config(layout="wide", page_title="AMA Industry Simulation", initial_sidebar_state="expanded")

# ============================================
# GENRE & AUDIENCE DATABASE
# ============================================

GENRES = {
    "Indie Chill": {
        "authenticity_weight": 0.8,
        "visual_weight": 0.5,
        "commercial_penalty": 0.3,
        "ticket_conversion": 0.05
    },
    "Rap Underground": {
        "authenticity_weight": 0.9,
        "visual_weight": 0.6,
        "commercial_penalty": 0.2,
        "ticket_conversion": 0.07
    },
    "Commercial Pop": {
        "authenticity_weight": 0.4,
        "visual_weight": 0.9,
        "commercial_penalty": 0.1,
        "ticket_conversion": 0.08
    },
    "Bolero Contemporary": {
        "authenticity_weight": 0.7,
        "visual_weight": 0.3,
        "commercial_penalty": 0.05,
        "ticket_conversion": 0.1
    }
}

FAME_LEVELS = {
    "Unknown": 0.1,
    "Local Buzz": 0.3,
    "Regional": 0.6
}

TARGET_GOAL = 120_000_000

# ============================================
# INIT STATE
# ============================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.cash = 100_000_000
    
    st.session_state.genre = random.choice(list(GENRES.keys()))
    st.session_state.fame_label = random.choice(list(FAME_LEVELS.keys()))
    st.session_state.fame = FAME_LEVELS[st.session_state.fame_label]
    
    st.session_state.trust = 0.3
    st.session_state.brand = 0.2
    
    st.session_state.history = []

# ============================================
# HEADER
# ============================================

st.title("🎬 AMA Creative Economy – Industry Simulation")

colA, colB, colC = st.columns(3)
colA.metric("Cash", f"{int(st.session_state.cash):,} VND")
colB.metric("Genre", st.session_state.genre)
colC.metric("Starting Fame", st.session_state.fame_label)

st.divider()

# ============================================
# DECISION PHASE
# ============================================

st.header(f"📊 Round {st.session_state.round} – Strategic Decision")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Creative")
    production = st.selectbox("Production", ["Low (10M)", "Medium (25M)", "High (40M)"])
    authenticity_focus = st.slider("Authenticity Focus", 0.0, 1.0, 0.5)

with col2:
    st.subheader("Marketing")
    ads = st.selectbox("Ads Budget", ["Low (5M)", "Medium (15M)", "High (30M)"])
    influencer = st.checkbox("Influencer (20M)")

with col3:
    st.subheader("Live Strategy")
    live_event = st.selectbox("Live Activity", ["None", "Free Session", "Ticket Showcase"])

# ============================================
# COST CALCULATION
# ============================================

cost_map = {
    "Low (10M)": 10_000_000,
    "Medium (25M)": 25_000_000,
    "High (40M)": 40_000_000,
    "Low (5M)": 5_000_000,
    "Medium (15M)": 15_000_000,
    "High (30M)": 30_000_000
}

total_cost = cost_map[production] + cost_map[ads]

if influencer:
    total_cost += 20_000_000

if live_event == "Ticket Showcase":
    total_cost += 10_000_000

st.metric("Total Investment This Round", f"{int(total_cost):,} VND")

# ============================================
# RUN ROUND
# ============================================

if st.button("🔒 Lock & Run Market"):

    if total_cost > st.session_state.cash:
        st.error("Not enough capital.")
    else:
        st.session_state.cash -= total_cost

        genre_profile = GENRES[st.session_state.genre]

        # Creative score
        quality = 0.5 + (cost_map[production] / 40_000_000) * 0.3
        authenticity = authenticity_focus * genre_profile["authenticity_weight"]

        # Marketing impact
        ad_boost = np.log1p(cost_map[ads] / 10_000_000)

        # Base impressions
        attention_pool = 150_000
        impressions = attention_pool * st.session_state.trust
        impressions += ad_boost * 5000
        impressions += st.session_state.fame * 5000

        # CTR & retention behavior
        ctr = 0.03 + 0.05 * genre_profile["visual_weight"] + 0.02 * st.session_state.fame
        retention = 0.4 + 0.4 * quality

        if authenticity_focus < 0.3:
            retention -= genre_profile["commercial_penalty"]

        views = impressions * ctr
        streaming_revenue = views * 500

        # Live revenue
        live_revenue = 0
        if live_event == "Free Session":
            live_revenue = 5_000_000 * genre_profile["ticket_conversion"]
        elif live_event == "Ticket Showcase":
            live_revenue = 20_000_000 * genre_profile["ticket_conversion"]

        total_revenue = streaming_revenue + live_revenue
        st.session_state.cash += total_revenue

        # Update fame & trust
        performance = ctr * retention
        st.session_state.trust += 0.05 * (performance - 0.05)
        st.session_state.trust = max(0.1, min(1.0, st.session_state.trust))

        if performance > 0.06:
            st.session_state.fame += 0.05

        # Save history
        st.session_state.history.append({
            "views": views,
            "revenue": total_revenue,
            "cash": st.session_state.cash
        })

        st.session_state.round += 1

        st.success("Round Completed!")

# ============================================
# DASHBOARD
# ============================================

if len(st.session_state.history) > 0:

    df = pd.DataFrame(st.session_state.history)

    st.subheader("📈 Performance Dashboard")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df["views"], mode="lines+markers", name="Views"))
    fig.add_trace(go.Scatter(y=df["revenue"], mode="lines+markers", name="Revenue"))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    if st.session_state.cash >= TARGET_GOAL:
        st.success("🎉 Target Achieved! You reached 120,000,000 VND.")

# ============================================
# RESET
# ============================================

if st.button("Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
